"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which sensor interface board is present, if any

example JSON:
{"model": "DFE"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.interface.dfe.dfe import DFE
from scs_dfe.interface.pzhb.pzhb import PZHB


# --------------------------------------------------------------------------------------------------------------------

class InterfaceConf(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_MODEL = 'DFE'               # TODO: deprecated - provides backwards compatibility

    __MODELS = ['DFE', 'DFE/0x68', 'DFE/0x69', 'PZHB']

    @classmethod
    def models(cls):
        return cls.__MODELS


    __FILENAME = "interface_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return InterfaceConf(cls.DEFAULT_MODEL)

        model = jdict.get('model')

        return InterfaceConf(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        super().__init__()

        self.__model = model


    # ----------------------------------------------------------------------------------------------------------------

    def interface(self):
        if self.model is None:
            return None

        if self.model == 'DFE':
            return DFE(None)

        if self.model == 'DFE/0x68':
            return DFE(0x68)

        if self.model == 'DFE/0x69':
            return DFE(0x69)

        if self.model == 'PZHB':
            return PZHB()

        raise ValueError('unknown model: %s' % self.model)


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
        return "InterfaceConf:{model:%s}" % self.model
