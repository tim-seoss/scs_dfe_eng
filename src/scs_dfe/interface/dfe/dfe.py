"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A digital front-end (DFE) sensor interface
"""

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.mcp342x import MCP342X
from scs_dfe.gas.pt1000 import Pt1000

from scs_dfe.interface.component.io import IO
from scs_dfe.interface.component.mcp9808 import MCP9808
from scs_dfe.interface.interface import Interface

from scs_dfe.led.io_led import IOLED


# --------------------------------------------------------------------------------------------------------------------

class DFE(Interface):
    """
    classdocs
    """

    DEFAULT_PT1000_ADDR = 0x68

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __pt1000_addr_str(addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pt1000_addr):
        """
        Constructor
        """
        self.__pt1000_addr = pt1000_addr                                # int

        self.__temp_sensor = None
        self.__io = IO(False)


    # ----------------------------------------------------------------------------------------------------------------

    def led(self):
        return IOLED()


    def peripheral_power(self, enable):
        pass                                    # TODO: implement peripheral_power(..)


    def temp(self):
        if self.__temp_sensor is None:
            self.__temp_sensor = MCP9808(True)

        return self.__temp_sensor.sample()


    def null_datum(self):
        return MCP9808.null_datum()


    # ----------------------------------------------------------------------------------------------------------------

    def gas_sensors(self, host):
        # Pt1000...
        pt1000 = self.pt1000(host)

        # sensors...
        afe_calib = AFECalib.load(host)
        afe_baseline = AFEBaseline.load(host)

        sensors = afe_calib.sensors(afe_baseline)

        return AFE(self, pt1000, sensors)


    def pt1000(self, host):
        if self.__pt1000_addr is None:
            return None

        pt1000_calib = Pt1000Calib.load(host)

        return Pt1000(pt1000_calib)


    def pt1000_adc(self, gain, rate):
        if self.__pt1000_addr is None:
            return None

        return MCP342X(self.__pt1000_addr, gain, rate)


    # ----------------------------------------------------------------------------------------------------------------

    def power_gases(self, enable):
        pass


    def power_gps(self, enable):
        self.__io.gps_power = enable


    def power_modem(self, enable):
        pass                                # TODO: implement power_modem


    def power_ndir(self, enable):
        self.__io.ndir_power = enable


    def power_opc(self, enable):
        self.__io.opc_power = enable


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DFE:{pt1000_addr:%s, temp_sensor:%s}" % \
               (self.__pt1000_addr_str(self.__pt1000_addr), self.__temp_sensor)
