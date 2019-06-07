"""
Created on 27 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/south-coast-science/scs_dsi_t1_f1
"""

from scs_core.data.datum import Decode

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class DSIt1f1(object):
    """
    South Coast Science DSI t1 f1 microcontroller
    """
    ADDR_AUX =          0x48


    # ----------------------------------------------------------------------------------------------------------------


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =    2.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr


    # ----------------------------------------------------------------------------------------------------------------

    def start_conversion(self):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            response = I2C.read_cmd(ord('s'), 1)

            if response != 1:        # ACK
                raise RuntimeError("response: %s" % response)

        finally:
            I2C.end_tx()
            self.release_lock()


    def read_conversion_count(self):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            chars = I2C.read_cmd(ord('c'), 4)

            c_aux = Decode.unsigned_int(chars[0:2], '<')     # CS0
            c_wrk = Decode.unsigned_int(chars[2:4], '<')     # CS1

            return c_wrk, c_aux

        finally:
            I2C.end_tx()
            self.release_lock()


    def read_conversion_voltage(self):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            chars = I2C.read_cmd(ord('v'), 8)

            v_aux = Decode.float(chars[0:4], '<')     # CS0
            v_wrk = Decode.float(chars[4:8], '<')     # CS1

            return round(v_wrk, 5), round(v_aux, 5)

        finally:
            I2C.end_tx()
            self.release_lock()


    def version_ident(self):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            chars = I2C.read_cmd(ord('i'), 40)

            ident = ''.join([chr(char) for char in chars]).strip()

            return ident

        finally:
            I2C.end_tx()
            self.release_lock()


    def version_tag(self):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            chars = I2C.read_cmd(ord('t'), 11)

            tag = ''.join([chr(char) for char in chars]).strip()

            return tag

        finally:
            I2C.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def test(self, cmd, response_size):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            return I2C.read_cmd(cmd, response_size)

        finally:
            I2C.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, DSIt1f1.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return self.__class__.__name__ + "-" + ("0x%02x" % self.__addr)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DSIt1f1:{addr:0x%0.2x}" % self.addr
