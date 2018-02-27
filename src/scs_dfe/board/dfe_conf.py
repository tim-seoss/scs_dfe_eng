"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

the I2C address of the Pt1000 ADC

example documents:
{"pt1000-addr": "0x68"}        - Alpha Pi Eng, Alpha BB Eng without RTC
{"pt1000-addr": "0x69"}        - Alpha BB Eng with RTC
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.board.mcp9808 import MCP9808

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.mcp342x import MCP342X


# --------------------------------------------------------------------------------------------------------------------

class DFEConf(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_PT1000_ADDR = 0x68


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "dfe_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def board_temp_sensor():
        return MCP9808(True)


    # ----------------------------------------------------------------------------------------------------------------

    def __pt1000_addr_str(addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        pt1000_addr_str = jdict.get('pt1000-addr')

        pt1000_addr = None if pt1000_addr_str is None else int(pt1000_addr_str, 0)

        return DFEConf(pt1000_addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pt1000_addr):
        """
        Constructor
        """
        super().__init__()

        self.__pt1000_addr = pt1000_addr            # int


    # ----------------------------------------------------------------------------------------------------------------

    def afe(self, host):
        # Pt1000...
        pt1000 = self.pt1000(host)

        # sensors...
        afe_calib = AFECalib.load(host)
        afe_baseline = AFEBaseline.load(host)

        sensors = afe_calib.sensors(afe_baseline)

        return AFE(self, pt1000, sensors)


    def pt1000(self, host):
        if self.pt1000_addr is None:
            return None

        pt1000_calib = Pt1000Calib.load(host)

        return Pt1000(pt1000_calib)


    def pt1000_adc(self, gain, rate):
        if self.pt1000_addr is None:
            return None

        return MCP342X(self.pt1000_addr, gain, rate)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pt1000_addr(self):
        return self.__pt1000_addr


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pt1000-addr'] = DFEConf.__pt1000_addr_str(self.__pt1000_addr)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DFEConf:{pt1000_addr:%s}" % DFEConf.__pt1000_addr_str(self.pt1000_addr)
