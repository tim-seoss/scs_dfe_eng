"""
Created on 8 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"sample-interval": 2, "temp-offset": 0.0}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable

from scs_dfe.gas.scd30.scd30 import SCD30


# --------------------------------------------------------------------------------------------------------------------

class SCD30Conf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "scd30_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        sample_interval = jdict.get('sample-interval')
        temperature_offset = jdict.get('temp-offset')

        return cls(sample_interval, temperature_offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample_interval, temperature_offset):
        """
        Constructor
        """
        self.__sample_interval = Datum.int(sample_interval)                     # int       seconds
        self.__temperature_offset = Datum.float(temperature_offset, 1)          # float     °C


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def scd30():
        return SCD30(SCD30.DEFAULT_I2C_ADDR)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sample-interval'] = self.sample_interval
        jdict['temp-offset'] = self.temperature_offset

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample_interval(self):
        return self.__sample_interval


    @property
    def temperature_offset(self):
        return self.__temperature_offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SCD30Conf:{sample_interval:%s, temperature_offset:%s}" %  \
               (self.sample_interval, self.temperature_offset)
