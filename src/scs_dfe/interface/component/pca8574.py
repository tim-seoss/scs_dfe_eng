"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class PCA8574(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, addr, directory, file):
        device = PCA8574(addr, directory, file)

        device.read()

        return device

        # try:
        #     device.read()
        #     return device
        #
        # except OSError:
        #     return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr, directory, file):
        """
        Constructor
        """
        self.__addr = addr
        self.__directory = directory
        self.__file = file


    # ----------------------------------------------------------------------------------------------------------------

    def read(self):
        try:
            I2C.start_tx(self.__addr)
            byte = I2C.read(1)

        except RuntimeError:
            return None

        finally:
            I2C.end_tx()

        return byte


    def write(self, byte):
        try:
            I2C.start_tx(self.__addr)
            I2C.write(byte)

            print("write:0x%02x" % byte)

        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def state(self):
        return PCA8574State.load_from_file(os.path.join(self.__directory, self.__file))


    @state.setter
    def state(self, byte):
        state = PCA8574State.load_from_file(os.path.join(self.__directory, self.__file))

        state.byte = byte
        state.save_to_file(self.__directory, self.__file)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PCA8574:{addr:0x%02x, directory:%s, file:%s}" % (self.__addr, self.__directory, self.__file)


# --------------------------------------------------------------------------------------------------------------------

class PCA8574State(PersistentJSONable):
    """
    classdocs
    """

    @classmethod
    def persistence_location(cls, _):
        raise NotImplementedError()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        """
        Establish the /tmp/southcoastscience/ root.
        Should be invoked level class load.
        """
        try:
            os.makedirs(Host.tmp_dir())
            os.chmod(Host.tmp_dir(), 0o777)
        except FileExistsError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        byte = int(jdict.get('byte') if jdict else '0xff', 16)

        return PCA8574State(byte)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, byte):
        """
        Constructor
        """
        super().__init__()

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
        binary = bin(self.__byte)

        return "PCA8574State:{byte:%s}" % binary
