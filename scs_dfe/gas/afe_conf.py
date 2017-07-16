"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not a Pt1000 temperature sensor is present on the AFE

example JSON:
{"pt1000-present": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.pt1000_calib import Pt1000Calib
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.pt1000_conf import Pt1000Conf


# --------------------------------------------------------------------------------------------------------------------

class AFEConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "afe_conf.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return AFEConf(True)

        pt1000_present = jdict.get('pt1000-present')

        return AFEConf(pt1000_present)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pt1000_present):
        """
        Constructor
        """
        self.__pt1000_present = bool(pt1000_present)


    # ----------------------------------------------------------------------------------------------------------------

    def afe(self, host):
        # Pt1000...
        pt1000_conf = Pt1000Conf.load_from_host(host)
        pt1000 = self.pt1000(host)

        # sensors...
        afe_calib = AFECalib.load_from_host(host)
        afe_baseline = AFEBaseline.load_from_host(host)

        sensors = afe_calib.sensors(afe_baseline)

        return AFE(pt1000_conf, pt1000, sensors)


    def pt1000(self, host):
        if not self.pt1000_present:
            return None

        pt1000_calib = Pt1000Calib.load_from_host(host)

        return Pt1000(pt1000_calib)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pt1000_present(self):
        return self.__pt1000_present


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pt1000-present'] = self.pt1000_present

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AFEConf:{pt1000_present:%s}" %  self.pt1000_present
