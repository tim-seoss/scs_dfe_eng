"""
Created on 16 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An OPCube controller
"""

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_dfe.gas.isi.isi import ISI

from scs_dfe.interface.interface import Interface
from scs_dfe.interface.interface_status import InterfaceStatus


# --------------------------------------------------------------------------------------------------------------------

class OPCube(Interface):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mcu):
        """
        Constructor
        """
        self.__mcu = mcu                            # OPCubeMCU


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        return InterfaceStatus(self.__mcu.read_temperature())


    def null_datum(self):
        return InterfaceStatus(None)


    # ----------------------------------------------------------------------------------------------------------------

    def gas_sensors(self, host):
        # sensors...
        afe_calib = AFECalib.load(host)
        afe_baseline = AFEBaseline.load(host, skeleton=True)

        if afe_calib is None:
            return None

        sensors = afe_calib.sensors(afe_baseline)

        return ISI(sensors)


    def pt1000(self, host):
        return None


    def pt1000_adc(self, gain, rate):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def led(self):
        return self.__mcu.led()


    # ----------------------------------------------------------------------------------------------------------------

    def power_gases(self, on):
        return self.__mcu.power_gases(on)


    def power_gps(self, on):
        return self.__mcu.power_gps(on)


    def power_modem(self, on):
        return self.__mcu.power_modem(on)


    def power_ndir(self, on):
        return self.__mcu.power_ndir(on)


    def power_opc(self, on):
        return self.__mcu.power_opc(on)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCube:{mcu:%s}" % self.__mcu
