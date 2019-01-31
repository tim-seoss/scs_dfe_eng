"""
Created on 23 Jan 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from abc import abstractmethod

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class OPC(object):
    """
    classdocs
    """

    __DEFAULT_BOOT_TIME =           8.0         # Seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, cls.lock_timeout())


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def lock_timeout(cls):
        pass


    @classmethod
    @abstractmethod
    def boot_time(cls):
        return cls.__DEFAULT_BOOT_TIME


    @classmethod
    @abstractmethod
    def power_cycle_time(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, spi_bus, spi_device, spi_mode, spi_clock):
        """
        Constructor
        """
        self._io = IO()
        self._spi = SPI(spi_bus, spi_device, spi_mode, spi_clock)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        initial_power_state = self._io.opc_power

        self._io.opc_power = IO.LOW

        if initial_power_state == IO.HIGH:          # initial_power_state is None if there is no power control facility
            time.sleep(self.boot_time())


    def power_off(self):
        self._io.opc_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def operations_on(self):
        pass


    @abstractmethod
    def operations_off(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def sample(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def firmware(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{io:%s, spi:%s}" % (self._io, self._spi)
