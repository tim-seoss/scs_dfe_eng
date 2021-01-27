"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which sensor interface board is present, if any

example JSON:
{"model": "DFE", "inf": "/home/scs/SCS/pipes/lambda-model-gas-s1.uds"}
"""

from scs_core.interface.interface_conf import InterfaceConf as AbstractInterfaceConf
from scs_dfe.interface.dfe.dfe import DFE

from scs_dfe.interface.opcube.opcube import OPCube
from scs_dfe.interface.opcube.opcube_mcu_t1 import OPCubeMCUt1

from scs_dfe.interface.pzhb.pzhb import PZHB
from scs_dfe.interface.pzhb.pzhb_mcu_t0 import PZHBMCUt0
from scs_dfe.interface.pzhb.pzhb_mcu_t1_f1 import PZHBMCUt1f1
from scs_dfe.interface.pzhb.pzhb_mcu_t2_f1 import PZHBMCUt2f1
from scs_dfe.interface.pzhb.pzhb_mcu_t3_f1 import PZHBMCUt3f1


# --------------------------------------------------------------------------------------------------------------------

class InterfaceConf(AbstractInterfaceConf):
    """
    classdocs
    """

    DEFAULT_MODEL = 'DFE'           # provides backwards compatibility

    __MODELS = [
        'DFE',                      # Alpha Pi Eng, ignoring Pt1000
        'DFE/0x68',                 # Alpha Pi Eng, Alpha BB Eng without RTC
        'DFE/0x69',                 # Alpha BB Eng with RTC
        'OPCubeT1',                 # OPCube controller (type 1)
        'PZHBt0',                   # Pi Zero Header Breakout (no microcontroller)
        'PZHBt1',                   # Pi Zero Header Breakout (type 1)
        'PZHBt2',                   # Pi Zero Header Breakout (type 2)
        'PZHBt3'                    # Pi Zero Header Breakout (type 3)
    ]

    @classmethod
    def models(cls):
        return cls.__MODELS


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return cls(cls.DEFAULT_MODEL)

        model = jdict.get('model')

        return cls(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        super().__init__(model)


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

        if self.model == 'OPCubeT1':
            return OPCube(OPCubeMCUt1(OPCubeMCUt1.DEFAULT_ADDR))

        if self.model == 'PZHBt0':
            return PZHB(PZHBMCUt0())

        if self.model == 'PZHB' or self.model == 'PZHBt1':
            return PZHB(PZHBMCUt1f1(PZHBMCUt1f1.DEFAULT_ADDR))

        if self.model == 'PZHBt2':
            return PZHB(PZHBMCUt2f1(PZHBMCUt2f1.DEFAULT_ADDR))

        if self.model == 'PZHBt3':
            return PZHB(PZHBMCUt3f1(PZHBMCUt3f1.DEFAULT_ADDR))

        raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "InterfaceConf(dfe):{model:%s}" % self.model
