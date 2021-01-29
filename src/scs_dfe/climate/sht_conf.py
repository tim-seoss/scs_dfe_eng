"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

the I2C addresses of the internal (in A4 pot) and external (exposed to air) SHTs

example JSON:
{"int": "0x44", "ext": "0x45"}
"""

from scs_core.climate.sht_conf import SHTConf as AbstractSHTConf
from scs_dfe.climate.sht31 import SHT31


# --------------------------------------------------------------------------------------------------------------------

class SHTConf(AbstractSHTConf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, int_addr, ext_addr):
        """
        Constructor
        """
        super().__init__(int_addr, ext_addr)


    # ----------------------------------------------------------------------------------------------------------------

    def int_sht(self):
        if self.int_addr is None:
            return None

        return SHT31(self.int_addr)


    def ext_sht(self):
        if self.ext_addr is None:
            return None

        return SHT31(self.ext_addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SHTConf(dfe):{int_addr:%s, ext_addr:%s}" %  \
               (SHTConf.__addr_str(self.int_addr), SHTConf.__addr_str(self.ext_addr))
