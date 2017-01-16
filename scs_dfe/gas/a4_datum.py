"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class A4Datum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, calib, tc, temp, weV, aeV):
        if calib is None or tc is None:
            return A4Datum(weV, aeV)

        # print("-")
        # print(tc)
        # print("-")

        # print("weV:%0.6f, aeV:%0.6f" % (weV, aeV))

        weT = weV - (calib.weELC / 1000.0)
        aeT = aeV - (calib.aeELC / 1000.0)

        # print("weT:%0.6f, aeT:%0.6f" % (weT, aeT))

        weC = tc.correct(calib, temp, weT, aeT)

        if weC is None:
            return A4Datum(weV, aeV)

        cnc = (weC * 1000.0) / calib.weSENS

        # print("weC:%0.6f, cnc:%0.6f" % (weC, cnc))
        # print("-")

        return A4Datum(weV, aeV, weC, cnc)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, weV, aeV, weC=None, cnc=None):
        """
        Constructor
        """
        self.__weV = Datum.float(weV, 6)        # uncorrected working electrode voltage
        self.__aeV = Datum.float(aeV, 6)        # uncorrected auxiliary electrode voltage

        self.__weC = Datum.float(weC, 6)        # corrected working electrode voltage
        self.__cnc = Datum.float(cnc, 1)        # gas concentration                            ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.weV
        jdict['aeV'] = self.aeV

        jdict['weC'] = self.weC                 # may be None
        jdict['cnc'] = self.cnc                 # may be None

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def weV(self):
        return self.__weV


    @property
    def aeV(self):
        return self.__aeV


    @property
    def weC(self):
        return self.__weC


    @property
    def cnc(self):
        return self.__cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Datum:{weV:%0.6f, aeV:%0.6f, weC:%s, cnc:%s}" % (self.weV, self.aeV, self.weC, self.cnc)
