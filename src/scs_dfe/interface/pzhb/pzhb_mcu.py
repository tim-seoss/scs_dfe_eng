"""
Created on 21 Aug 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract Pi Zero Header Breakout MCU
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class PZHBMCU(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def host_shutdown_initiated(self):
        pass


    @abstractmethod
    def button_enable(self):
        pass


    @abstractmethod
    def button_pressed(self):
        pass


    @abstractmethod
    def read_batt_v(self):
        pass


    @abstractmethod
    def read_current_count(self):
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


    def power_all(self, enable):
        self.power_gases(enable)
        self.power_gps(enable)
        self.power_ndir(enable)
        self.power_opc(enable)
        self.power_modem(enable)


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
