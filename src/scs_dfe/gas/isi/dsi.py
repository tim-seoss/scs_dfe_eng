"""
Created on 27 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an abstract Digital Single Interface (DSI) microcontroller
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class DSI(ABC):
    """
    South Coast Science DSI microcontroller
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def power_sensor(self, on):
        pass


    @abstractmethod
    def start_conversion(self):
        pass


    @abstractmethod
    def read_conversion_count(self):
        pass


    @abstractmethod
    def read_conversion_voltage(self):
        pass


    @abstractmethod
    def version_ident(self):
        pass


    @abstractmethod
    def version_tag(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def obtain_lock(self):
        pass


    @abstractmethod
    def release_lock(self):
        pass
