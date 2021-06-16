"""
Created on 27 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Digital Single Interface (DSI) Type 1 on 16K ROM MCU

Compatible with:
https://github.com/south-coast-science/scs_dsi_t2_f1
"""

import time

from scs_core.data.datum import Decode

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class DSIElcT1f16K(object):
    """
    South Coast Science DSI Electrochem Type 1 (16K) microcontroller
    """

    DEFAULT_ADDR =          0x30

    CONVERSION_TIME =       0.1             # seconds

    # ----------------------------------------------------------------------------------------------------------------

    __RESPONSE_ACK =        1
    __RESPONSE_NACK =       2

    __SEND_WAIT_TIME =      0.010               # seconds
    __LOCK_TIMEOUT =        2.0

    __SAMPLE_MAX_VOLTAGE =  3.3
    __SAMPLE_MAX_COUNT =    65535


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr


    # ----------------------------------------------------------------------------------------------------------------

    def start_conversion(self):
        response = self.__cmd(ord('s'), 1)

        if response != self.__RESPONSE_ACK:
            raise RuntimeError("response: %s" % response)


    def read_conversion_count(self):
        response = self.__cmd(ord('c'), 4)

        c_aux = Decode.unsigned_int(response[0:2], '<')     # CS0
        c_wrk = Decode.unsigned_int(response[2:4], '<')     # CS1

        return c_wrk, c_aux


    def read_conversion_voltage(self):
        c_wrk, c_aux = self.read_conversion_count()

        v_wrk = self.__voltage_conversion(c_wrk)
        v_aux = self.__voltage_conversion(c_aux)

        return round(v_wrk, 5), round(v_aux, 5)


    def version_ident(self):
        response = self.__cmd(ord('i'), 40)

        return ''.join([chr(byte) for byte in response]).strip()


    def version_tag(self):
        response = self.__cmd(ord('t'), 11)

        return ''.join([chr(byte) for byte in response]).strip()


    # ----------------------------------------------------------------------------------------------------------------

    def __voltage_conversion(self, count):
        return self.__SAMPLE_MAX_VOLTAGE * count / self.__SAMPLE_MAX_COUNT


    def __cmd(self, cmd, response_size):
        try:
            self.obtain_lock()
            I2C.Sensors.start_tx(self.__addr)

            response = I2C.Sensors.read_cmd(cmd, response_size, self.__SEND_WAIT_TIME)

            time.sleep(self.__SEND_WAIT_TIME)

            return response

        finally:
            I2C.Sensors.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return "%s-0x%02x" % (self.__class__.__name__, self.__addr)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DSIElcT1f16K:{addr:0x%0.2x}" % self.addr
