"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which GPS receiver is present, if any

example JSON:
{"model": null}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.gps.gps_monitor import GPSMonitor
from scs_dfe.gps.pam7q import PAM7Q


# TODO: add static / mobile setting - for averaging

# --------------------------------------------------------------------------------------------------------------------

class GPSConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "gps_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')

        return GPSConf(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        super().__init__()

        self.__model = model


    # ----------------------------------------------------------------------------------------------------------------

    def gps_monitor(self, host):
        if self.model is None:
            return None

        if self.model == 'PAM7Q':
            gps = PAM7Q(host.gps_device())
        else:
            raise ValueError('unknown model: %s' % self.model)

        return GPSMonitor(gps)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSConf:{model:%s}" % self.model
