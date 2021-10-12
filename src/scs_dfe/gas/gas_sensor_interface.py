"""
Created on 7 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract gas sensor interface
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class GasSensorInterface(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # identity...

    @classmethod
    @abstractmethod
    def src(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # business methods...

    @abstractmethod
    def adc_versions(self):
        pass


    @abstractmethod
    def sample(self, sht_datum):
        pass


    @abstractmethod
    def sample_station(self, sn, sht_datum):
        pass


    @abstractmethod
    def null_datum(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # electrochem callbacks...

    @abstractmethod
    def sample_raw_wrk_aux(self, sensor_index, gain_index):
        pass


    @abstractmethod
    def sample_raw_wrk(self, sensor_index, gain_index):
        pass
