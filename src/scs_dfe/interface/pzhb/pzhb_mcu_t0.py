"""
Created on 1 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Raspberry Pi Zero Header Breakout board (PZHB) with no STMicro controller
"""

from scs_dfe.interface.pzhb.pzhb_mcu import PZHBMCU


# --------------------------------------------------------------------------------------------------------------------

class PZHBMCUt0(PZHBMCU):
    """
    Constructor
    """

    # ----------------------------------------------------------------------------------------------------------------

    def host_shutdown_initiated(self):
        pass


    def button_enable(self):
        pass


    def button_pressed(self):
        return False


    def read_batt_v(self):
        return None


    def read_current_count(self):
        return None


    def version_ident(self):
        return None


    def version_tag(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def led(self):
        return None


    def power_gases(self, enable):
        pass


    def power_gps(self, enable):
        pass


    def power_modem(self, enable):
        pass


    def power_ndir(self, enable):
        pass


    def power_opc(self, enable):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def led1(self, on):
        pass


    def led2(self, on):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PZHBMCUt0:{}"
