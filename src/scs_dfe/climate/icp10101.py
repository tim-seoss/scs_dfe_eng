"""
Created on 8 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

TDK ICP-10101 digital barometer
https://invensense.tdk.com/download-pdf/icp-10101-datasheet/
"""

import time

from scs_core.climate.icp10101_datum import ICP10101Datum

from scs_core.data.crc import crc8
from scs_core.data.datum import Decode

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class ICP10101(object):
    """
    classdocs
    """
    NAME =                          'ICP'

    DEFAULT_ADDR =                  0x63

    __CONVERSION_TIME =             0.100               # seconds
    __LOCK_TIMEOUT =                1.0                 # seconds

    __CMD_MEASURE_ULN =             0x7866
    __CMD_RESET =                   0x805d
    __CMD_READ_ID =                 0xefc8
    __CMD_OTP_START =               [0xc5, 0x95, 0x00, 0x66, 0x9c]
    __CMD_OTP_READ =                0xc7f7

    __PA_CALIB =                    [45000.0, 80000.0, 105000.0]
    __LUT_LOWER =                   3.5 * (2 ** 20)
    __LUT_UPPER =                   11.5 * (2 ** 20)
    __QUADR_FACTOR =                1.0 / 16777216.0
    __OFFSET_FACTOR =               2048.0

    __T_CONV =                      175.0 / 65536


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def null_datum(cls):
        return ICP10101Datum(None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __conversion_constants(cls, pa, lut):
        c = (lut[0] * lut[1] * (pa[0] - pa[1]) +
             lut[1] * lut[2] * (pa[1] - pa[2]) +
             lut[2] * lut[0] * (pa[2] - pa[0])) / \
            (lut[2] * (pa[0] - pa[1]) +
             lut[0] * (pa[1] - pa[2]) +
             lut[1] * (pa[2] - pa[0]))

        a = (pa[0] * lut[0] - pa[1] * lut[1] - (pa[1] - pa[0]) * c) / (lut[0] - lut[1])

        b = (pa[0] - a) * (lut[0] + c)

        return a, b, c


    @classmethod
    def __crc_check(cls, chars, *indices):
        for index in indices:
            if chars[index] != crc8(chars[index - 2:index]):
                raise ValueError(['0x%02x' % char for char in chars])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr                          # int
        self.__constants = None                     # array of int


    # ----------------------------------------------------------------------------------------------------------------

    def init(self):
        try:
            self.obtain_lock()
            I2C.Sensors.start_tx(self.addr)
            I2C.Sensors.write16(self.__CMD_RESET)

            I2C.Sensors.write(*self.__CMD_OTP_START)

            self.__constants = []
            for _ in range(4):
                chars = I2C.Sensors.read_cmd16(self.__CMD_OTP_READ, 3)
                self.__crc_check(chars, 2)

                self.__constants.append(Decode.int(chars[:2], '>'))

        finally:
            I2C.Sensors.end_tx()
            self.release_lock()


    def sample(self, altitude=None, include_temp=True):
        try:
            self.obtain_lock()
            I2C.Sensors.start_tx(self.addr)

            I2C.Sensors.write16(self.__CMD_MEASURE_ULN)
            time.sleep(self.__CONVERSION_TIME)

            chars = I2C.Sensors.read(9)
            self.__crc_check(chars, 2, 5, 8)

            t_count = chars[0] << 8 ^ chars[1]
            temp = round(self.__temperature(t_count), 1)

            p_count = chars[3] << 16 ^ chars[4] << 8 ^ chars[6]
            actual_press = self.__pressure(t_count, p_count) / 1000.0

            return ICP10101Datum.construct(actual_press, temp, altitude, include_temp=include_temp)

        finally:
            I2C.Sensors.end_tx()
            self.release_lock()


    def id(self):
        try:
            self.obtain_lock()
            I2C.Sensors.start_tx(self.addr)

            chars = I2C.Sensors.read_cmd16(self.__CMD_READ_ID, 3)
            self.__crc_check(chars, 2)

            return chars[1] & 0x3f

        finally:
            I2C.Sensors.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __temperature(cls, t_count):
        return -45.0 + cls.__T_CONV * t_count


    def __pressure(self, t_count, p_count):
        t = t_count - 32768.0

        s1 = self.__LUT_LOWER + float(self.constants[0] * t * t) * self.__QUADR_FACTOR
        s2 = self.__OFFSET_FACTOR * self.constants[3] + float(self.constants[1] * t * t) * self.__QUADR_FACTOR
        s3 = self.__LUT_UPPER + float(self.constants[2] * t * t) * self.__QUADR_FACTOR
        a, b, c = self.__conversion_constants(self.__PA_CALIB, [s1, s2, s3])

        return a + b / (c + p_count)


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__class__.__name__, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__class__.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    @property
    def constants(self):
        return self.__constants


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ICP10101:{addr:0x%02x, constants:%s}" % (self.addr, self.constants)
