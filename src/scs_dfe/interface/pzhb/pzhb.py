"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A Pi Zero Header Breakout system interface
"""

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_dfe.gas.isi.isi import ISI

from scs_dfe.interface.interface import Interface


# --------------------------------------------------------------------------------------------------------------------

class PZHB(Interface):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mcu):
        """
        Constructor
        """
        self.__mcu = mcu                            # PZHBMCU


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        return None


    def null_datum(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def gas_sensor_interface(self, host):
        # sensors...
        afe_calib = AFECalib.load(host)

        if afe_calib is None:
            return None

        afe_baseline = AFEBaseline.load(host, skeleton=True)
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
        return "PZHB:{mcu:%s}" % self.__mcu
