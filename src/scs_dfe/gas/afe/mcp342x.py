"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import struct
import time

from scs_host.bus.i2c import SensorI2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class MCP342X(object):
    """
    Microchip Technology MCP3421 or MCP3425 ADCs
    """

    GAIN_1 =            0x00        # ---- --00
    GAIN_2 =            0x01        # ---- --01     (default)
    GAIN_4 =            0x02        # ---- --10
    GAIN_8 =            0x03        # ---- --11

    RATE_15 =           0x08        # ---- 10--     16 bit
    RATE_60 =           0x04        # ---- 01--     14 bit
    RATE_240 =          0x00        # ---- 00--     12 bit      (default)


    # ----------------------------------------------------------------------------------------------------------------

    __START =           0x80        # 1--- ----

    __MODE_CONT =       0x10        # ---1 ----
    __MODE_SINGLE =     0x00        # ---0 ----     (default)

    __GAIN =            None
    __TCONV =           None


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =    2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.__GAIN = {
                        MCP342X.GAIN_1:     1.0,
                        MCP342X.GAIN_2:     2.0,
                        MCP342X.GAIN_4:     4.0,
                        MCP342X.GAIN_8:     8.0,
                    }

        cls.__TCONV = {
                        MCP342X.RATE_15:    0.080,
                        MCP342X.RATE_60:    0.020,
                        MCP342X.RATE_240:   0.005
                    }


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr, gain, rate):
        """
        initialise ADC with given gain and rate
        """
        # fields...
        self.__addr = addr
        self.__gain = gain
        self.__rate = rate

        self.__config = MCP342X.__MODE_SINGLE | self.__rate | self.__gain

        # write config...
        try:
            self.obtain_lock()
            self.__write(self.__config)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def start_conversion(self):
        """
        start single-shot conversion
        """
        start = MCP342X.__START | self.__config

        self.obtain_lock()
        self.__write(start)


    def read_conversion(self):
        """
        read most recent conversion
        returned value is voltage
        """
        try:
            SensorI2C.start_tx(self.addr)
            v, config = self.__read()

        finally:
            SensorI2C.end_tx()
            self.release_lock()

        if config & MCP342X.__START:
            raise ValueError(self.__class__.__name__ + ":read_conversion: conversion not ready.")

        return v


    def convert(self):
        """
        start single-shot conversion, wait for ready, then read
        warning: creates high level of I2C traffic
        returned value is voltage
        """
        self.start_conversion()

        try:
            SensorI2C.start_tx(self.addr)

            while True:
                v, config = self.__read()

                if not (config & MCP342X.__START):
                    break

                time.sleep(MCP342X.RATE_240)

        finally:
            SensorI2C.end_tx()
            self.release_lock()

        return v


    # ----------------------------------------------------------------------------------------------------------------

    def __read(self):
        # get data...
        msb, lsb, config = SensorI2C.read(3)

        unsigned = (msb << 8) | lsb

        # render voltage...
        signed = struct.unpack('h', struct.pack('H', unsigned))

        v = (signed[0] / 32767.5) * 2.048 / MCP342X.__GAIN[self.__gain]

        return v, config


    def __write(self, config):
        try:
            SensorI2C.start_tx(self.addr)
            SensorI2C.write(config)

        finally:
            SensorI2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__class__.__name__, MCP342X.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__class__.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    @property
    def gain(self):
        return self.__gain


    @property
    def rate(self):
        return self.__rate


    @property
    def tconv(self):
        return MCP342X.__TCONV[self.__rate]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{addr:0x%02x, gain:0x%0.4x, rate:0x%0.4x, config:0x%0.4x}" % \
                                         (self.addr, self.gain, self.rate, self.__config)
