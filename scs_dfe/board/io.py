"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.board.pca8574 import PCA8574

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class IO(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """
    HIGH = True
    LOW = False

    FILENAME =        "dfe_io.json"


    __MASK_GPS =        0x01            # 0000 0001
    __MASK_OPC =        0x02            # 0000 0010
    __MASK_NDIR =       0x04            # 0000 0100

    __MASK_LED_RED =    0x40            # 0100 0000
    __MASK_LED_GREEN =  0x80            # 1000 0000

    __ADDR =            0x3f

    __LOCK =            "DFE_IO"
    __LOCK_TIMEOUT =    2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return cls.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__device = PCA8574.construct(IO.__ADDR, IO.FILENAME)      # device is none if it can't be accessed


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gps_power(self):
        return self.__get_state(IO.__MASK_GPS)


    @gps_power.setter
    def gps_power(self, level):
        self.__set_state(IO.__MASK_GPS, level)


    @property
    def opc_power(self):
        return self.__get_state(IO.__MASK_OPC)


    @opc_power.setter
    def opc_power(self, level):
        self.__set_state(IO.__MASK_OPC, level)


    @property
    def ndir_power(self):
        return self.__get_state(IO.__MASK_NDIR)


    @ndir_power.setter
    def ndir_power(self, level):
        self.__set_state(IO.__MASK_NDIR, level)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def led_red(self):
        return self.__get_state(IO.__MASK_LED_RED)


    @led_red.setter
    def led_red(self, level):
        self.__set_state(IO.__MASK_LED_RED, level)


    @property
    def led_green(self):
        return self.__get_state(IO.__MASK_LED_GREEN)


    @led_green.setter
    def led_green(self, level):
        self.__set_state(IO.__MASK_LED_GREEN, level)


    # ----------------------------------------------------------------------------------------------------------------

    def __get_state(self, mask):
        if self.__device is None:
            return None

        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT, False)

        try:
            byte = self.__device.state.byte

            return bool(byte & mask)

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    def __set_state(self, mask, level):
        if self.__device is None:
            return

        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT, False)

        try:
            byte = self.__device.state.byte

            if level:
                byte |= mask
            else:
                byte &= ~mask

            self.__device.write(byte)
            self.__device.state = byte

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IO:{device:%s}" % self.__device
