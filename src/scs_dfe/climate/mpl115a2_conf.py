"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies fixed altitude or "auto" (altitude provided by GPS receiver), or None

example JSON:
{"altitude": "auto"}
"""

from scs_core.climate.mpl115a2_conf import MPL115A2Conf as AbstractMPL115A2Conf
from scs_dfe.climate.mpl115a2 import MPL115A2


# --------------------------------------------------------------------------------------------------------------------

class MPL115A2Conf(AbstractMPL115A2Conf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, altitude):
        """
        Constructor
        """
        super().__init__(altitude)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def mpl115a(cls, calib):
        c25 = None if calib is None else calib.c25

        return MPL115A2(c25)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPL115A2Conf(dfe):{altitude:%s}" %  self.altitude
