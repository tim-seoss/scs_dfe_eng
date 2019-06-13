"""
Created on 12 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/south-coast-science/scs_rpz_header_t1_f1
"""

from scs_core.data.datum import Decode

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class RPzHeaderT1F1(object):
    """
    South Coast Science DSI t1 f1 microcontroller
    """

    DEFAULT_ADDR =          0x76


    # ----------------------------------------------------------------------------------------------------------------

    __RESPONSE_ACK =        1
    __RESPONSE_NACK =       2

    __LOCK_TIMEOUT =        2.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr


    # ----------------------------------------------------------------------------------------------------------------

    def button_pressed(self):
        response = self.__cmd(ord('p'), 1)

        button_pressed = response == 1

        return button_pressed


    def read_batt_v(self):
        response = self.__cmd(ord('b'), 2)

        c_batt = Decode.unsigned_int(response[0:2], '<')

        v_batt = 2.0 * 3.3 * c_batt / 4095

        return v_batt


    def read_current_count(self):
        response = self.__cmd(ord('c'), 2)

        c_current = Decode.unsigned_int(response[0:2], '<')

        return c_current


    def version_ident(self):
        response = self.__cmd(ord('i'), 40)

        return ''.join([chr(byte) for byte in response]).strip()


    def version_tag(self):
        response = self.__cmd(ord('t'), 11)

        return ''.join([chr(byte) for byte in response]).strip()


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd, response_size):
        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            return I2C.read_cmd(cmd, response_size)

        finally:
            I2C.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


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
        return "RPzHeaderT1F1:{addr:0x%0.2x}" % self.addr
