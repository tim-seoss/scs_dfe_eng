"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A digital front-end (DFE) sensor interface
"""

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.afe.pt1000_calib import Pt1000Calib

from scs_dfe.gas.afe.afe import AFE
from scs_dfe.gas.afe.mcp342x import MCP342X
from scs_dfe.gas.afe.pt1000 import Pt1000
from scs_dfe.gas.isi.isi import ISI

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

    __IO_ACTIVE_HIGH = False

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __pt1000_addr_str(addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pt1000_addr=None):
        """
        Constructor
        """
        self.__pt1000_addr = pt1000_addr                                # int

        self._temp_sensor = None
        self._io = IO(self.__IO_ACTIVE_HIGH)


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        if self._temp_sensor is None:
            self._temp_sensor = MCP9808(True)

        return self._temp_sensor.sample()


    def null_datum(self):
        return MCP9808.null_datum()


    # ----------------------------------------------------------------------------------------------------------------

    def gas_sensors(self, host):
        # Pt1000...
        pt1000 = self.pt1000(host)

        # sensors...
        afe_calib = AFECalib.load(host)

        if afe_calib is None:
            return None

        afe_baseline = AFEBaseline.load(host, skeleton=True)
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

    def led(self):
        return IOLED()


    # ----------------------------------------------------------------------------------------------------------------

    def power_gases(self, on):                  # switches digital component only
        pass


    def power_gps(self, on):
        self._io.gps_power = on


    def power_modem(self, on):
        pass


    def power_ndir(self, on):
        self._io.ndir_power = on


    def power_opc(self, on):
        self._io.opc_power = on


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        addr_str = self.__pt1000_addr_str(self.__pt1000_addr)

        return "DFE:{pt1000_addr:%s, temp_sensor:%s, io:%s}" %  (addr_str, self._temp_sensor, self._io)


# --------------------------------------------------------------------------------------------------------------------

class ISIDFE(DFE):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def gas_sensors(self, host):
        # sensors...
        afe_calib = AFECalib.load(host)

        if afe_calib is None:
            return None

        afe_baseline = AFEBaseline.load(host, skeleton=True)
        sensors = afe_calib.sensors(afe_baseline)

        return ISI(sensors)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ISIDFE:{temp_sensor:%s, io:%s}" %  (self._temp_sensor, self._io)
