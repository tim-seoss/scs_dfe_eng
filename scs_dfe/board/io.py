"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.board.pca8574 import PCA8574

from scs_host.lock.lock import Lock
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class IO(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """
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
        self.__device = PCA8574(IO.__ADDR)      # device is none if it can't be read


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gps_power(self):
        return self.__get_state(IO.__MASK_GPS)


    @gps_power.setter
    def gps_power(self, on):
        self.__set_state(IO.__MASK_GPS, on)


    @property
    def opc_power(self):
        return self.__get_state(IO.__MASK_OPC)


    @opc_power.setter
    def opc_power(self, on):
        self.__set_state(IO.__MASK_OPC, on)


    @property
    def ndir_power(self):
        return self.__get_state(IO.__MASK_NDIR)


    @ndir_power.setter
    def ndir_power(self, on):
        self.__set_state(IO.__MASK_NDIR, on)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def led_red(self):
        return self.__get_state(IO.__MASK_LED_RED)


    @led_red.setter
    def led_red(self, on):
        self.__set_state(IO.__MASK_LED_RED, on)


    @property
    def led_green(self):
        return self.__get_state(IO.__MASK_LED_GREEN)


    @led_green.setter
    def led_green(self, on):
        self.__set_state(IO.__MASK_LED_GREEN, on)


    # ----------------------------------------------------------------------------------------------------------------

    def __get_state(self, mask):
        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT, False)

        try:
            state = IOState.load(Host)
            byte = state.byte

            return bool(byte & mask)

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    def __set_state(self, mask, on):
        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT, False)

        try:
            state = IOState.load(Host)
            byte = state.byte

            if on:
                byte |= mask
            else:
                byte &= ~mask

            # TODO: if no device, skip...
            self.__device.write(byte)

            state.byte = byte
            state.save(Host)

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IO:{device:%s}" % (self.__device)


# --------------------------------------------------------------------------------------------------------------------

class IOState(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "dfe_io.json"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        """
        Establish the /tmp/southcoastscience/ root.
        Should be invoked on class load.
        """
        try:
            os.makedirs(Host.SCS_TMP)       # TODO: get the file permissions right
        except FileExistsError:
            pass


    @classmethod
    def filename(cls, host):
        return host.SCS_TMP + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        byte = jdict.get('byte') if jdict else '0xff'
        state = int(byte, 16)

        return IOState(state)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, byte):
        """
        Constructor
        """
        self.__byte = byte                  # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['byte'] = "0x%02x" % self.__byte

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def byte(self):
        return self.__byte


    @byte.setter
    def byte(self, byte):
        self.__byte = byte


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IOState:{byte:0x%02x}" % (self.byte)


# --------------------------------------------------------------------------------------------------------------------

IOState.init()
