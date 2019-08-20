"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract sensor interface
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Interface(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def temp(self):
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

    @property
    @abstractmethod
    def load_switch_active_high(self):          # TODO: return the IO device?
        return None


