"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which GPS receiver is present, if any, plus sample interval and tally.

example JSON:
{"model": "SAM7Q", "sample-interval": 10, "tally": 60}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.gps.gps_monitor import GPSMonitor
from scs_dfe.gps.pam7q import PAM7Q
from scs_dfe.gps.sam_m8q import SAMM8Q


# --------------------------------------------------------------------------------------------------------------------

class GPSConf(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_SAMPLE_INTERVAL =       10          # seconds
    DEFAULT_TALLY =                 60          # 10 minutes


    __FILENAME = "gps_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')

        sample_interval = jdict.get('sample-interval', cls.DEFAULT_SAMPLE_INTERVAL)
        tally = jdict.get('tally', cls.DEFAULT_TALLY)
        report_file = jdict.get('report-file')

        return GPSConf(model, sample_interval, tally, report_file)


    @classmethod
    def is_valid_model(cls, model):
        return model in (PAM7Q.SOURCE, SAMM8Q.SOURCE)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_interval, tally, report_file):
        """
        Constructor
        """
        super().__init__()

        self.__model = model                                        # string

        self.__sample_interval = sample_interval                    # int seconds
        self.__tally = tally                                        # int count
        self.__report_file = report_file                            # string tmp file to store current GPS report


    # ----------------------------------------------------------------------------------------------------------------

    def gps_monitor(self, interface, host):
        gps = self.gps(interface, host)

        return GPSMonitor(gps, self)


    def gps(self, interface, host):
        if self.model is None:
            return None

        if self.model == PAM7Q.SOURCE:
            return PAM7Q(interface, host.gps_device())

        elif self.model == SAMM8Q.SOURCE:
            return SAMM8Q(interface, host.gps_device())

        else:
            raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def sample_interval(self):
        return self.__sample_interval


    @property
    def tally(self):
        return self.__tally


    @property
    def report_file(self):
        return self.__report_file


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model

        jdict['sample-interval'] = self.__sample_interval
        jdict['tally'] = self.__tally
        jdict['report-file'] = self.__report_file

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSConf:{model:%s, sample_interval:%s, tally:%s, report_file:%s}" % \
               (self.model, self.sample_interval, self.tally, self.report_file)
