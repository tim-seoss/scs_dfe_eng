"""
Created on 8 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"sample-interval": 2, "temp-offset": 0.0}
"""

from scs_core.gas.scd30.scd30_baseline import SCD30Baseline
from scs_core.gas.scd30.scd30_conf import SCD30Conf as AbstractSCD30Conf

from scs_dfe.gas.scd30.scd30 import SCD30

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class SCD30Conf(AbstractSCD30Conf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample_interval, temperature_offset):
        """
        Constructor
        """
        super().__init__(sample_interval, temperature_offset)


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def scd30():
        baseline = SCD30Baseline.load(Host)

        return SCD30(baseline)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SCD30Conf(dfe):{sample_interval:%s, temperature_offset:%s}" %  \
               (self.sample_interval, self.temperature_offset)
