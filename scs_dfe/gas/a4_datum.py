"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)c
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
    def construct(cls, calib, baseline, tc, temp, we_v, ae_v):
        if calib is None or tc is None:
            return A4Datum(we_v, ae_v)

        # print("calib: %s" % calib)

        # print("-")
        # print(tc)
        # print("-")

        # print("we_v:%0.6f, ae_v:%0.6f" % (we_v, ae_v))

        we_t = we_v - (float(calib.we_elc_mv) / 1000.0)
        ae_t = ae_v - (float(calib.ae_elc_mv) / 1000.0)

        # print("we_t:%0.6f, ae_t:%0.6f" % (we_t, ae_t))

        we_c = tc.correct(calib, temp, we_t, ae_t)

        if we_c is None:
            return A4Datum(we_v, ae_v)

        cnc = (we_c * 1000.0) / calib.we_sens_mv

        cnc = cnc + baseline.offset

        # print("we_c:%0.6f, cnc:%0.6f" % (we_c, cnc))
        # print("-")

        return A4Datum(we_v, ae_v, we_c, cnc)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, we_v, ae_v, we_c=None, cnc=None):
        """
        Constructor
        """
        self.__we_v = Datum.float(we_v, 6)        # uncorrected working electrode voltage
        self.__ae_v = Datum.float(ae_v, 6)        # uncorrected auxiliary electrode voltage

        self.__we_c = Datum.float(we_c, 6)        # corrected working electrode voltage
        self.__cnc = Datum.float(cnc, 1)          # gas concentration                            ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['weV'] = self.we_v
        jdict['aeV'] = self.ae_v

        jdict['weC'] = self.we_c                 # may be None
        jdict['cnc'] = self.cnc                  # may be None

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_v(self):
        return self.__we_v


    @property
    def ae_v(self):
        return self.__ae_v


    @property
    def we_c(self):
        return self.__we_c


    @property
    def cnc(self):
        return self.__cnc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Datum:{we_v:%0.6f, ae_v:%0.6f, we_c:%s, cnc:%s}" % (self.we_v, self.ae_v, self.we_c, self.cnc)
