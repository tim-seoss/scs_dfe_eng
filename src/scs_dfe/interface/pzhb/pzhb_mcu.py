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
    def peripheral_power(self, enable):
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
