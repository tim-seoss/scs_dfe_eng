"""
Created on 16 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract OPCube controller MCU
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class OPCubeMCU(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def host_shutdown_initiated(self):
        pass


    @abstractmethod
    def switch_state(self):
        pass


    @abstractmethod
    def read_batt_v(self):
        pass


    @abstractmethod
    def version_ident(self):
        pass


    @abstractmethod
    def version_tag(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def led(self):
        pass


    @abstractmethod
    def power_gases(self, enable):
        pass


    @abstractmethod
    def power_gps(self, enable):
        pass


    @abstractmethod
    def power_ndir(self, enable):
        pass


    @abstractmethod
    def power_opc(self, enable):
        pass


    @abstractmethod
    def power_modem(self, enable):
        pass
