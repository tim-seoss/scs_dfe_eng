"""
Created on 2 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from abc import ABC

from scs_core.particulate.opc_datum import OPCDatum

from scs_dfe.board.io import IO
from scs_dfe.particulate.opc import OPC

from scs_host.bus.spi import SPI


# --------------------------------------------------------------------------------------------------------------------

class AlphasenseOPC(OPC, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def uses_spi(cls):
        return True


    @classmethod
    def datum_class(cls):
        return OPCDatum.__class__


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

    def clean(self):
        pass


    def set_cleaning_interval(self, interval):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def data_ready(self):
        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lock_name(self):
        return self.__class__.__name__


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{io:%s, spi:%s}" % (self._io, self._spi)
