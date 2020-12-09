"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract system interface
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Interface(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def status(self):
        pass


    @abstractmethod
    def null_datum(self):
        pass

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def gas_sensors(self, host):
        pass


    @abstractmethod
    def pt1000(self, host):
        pass


    @abstractmethod
    def pt1000_adc(self, gain, rate):
        pass

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def led(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def power_gases(self, enable):                  # switches digital component only
        pass


    @abstractmethod
    def power_gps(self, enable):
        pass


    @abstractmethod
    def power_modem(self, enable):
        pass


    @abstractmethod
    def power_ndir(self, enable):
        pass


    @abstractmethod
    def power_opc(self, enable):
        pass
