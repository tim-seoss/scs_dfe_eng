"""
Created on 16 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract OPCube controller
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
    def version_ident(self):
        pass


    @abstractmethod
    def version_tag(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def read_temperature(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def led(self):
        pass


    def power_all(self, on):
        self.power_gases(on)
        self.power_gps(on)
        self.power_ndir(on)
        self.power_opc(on)
        self.power_modem(on)


    @abstractmethod
    def power_gases(self, on):
        pass


    @abstractmethod
    def power_gps(self, on):
        pass


    @abstractmethod
    def power_ndir(self, on):
        pass


    @abstractmethod
    def power_opc(self, on):
        pass


    @abstractmethod
    def power_modem(self, on):
        pass
