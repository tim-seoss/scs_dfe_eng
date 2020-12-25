"""
Created on 19 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Two-Channel I2C-Bus Switch With Interrupt Logic and Reset
https://www.ti.com/product/PCA9543A
"""

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class PCA9543A(object):
    """
    classdocs
    """

    ___I2C_ADDR = 0x70

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__addr = self.___I2C_ADDR


    # ----------------------------------------------------------------------------------------------------------------

    def enable(self, ch0, ch1):
        ch0_en = 0x01 if ch0 else 0x00
        ch1_en = 0x02 if ch1 else 0x00
        ctrl = ch1_en | ch0_en

        try:
            I2C.Sensors.start_tx(self.__addr)
            I2C.Sensors.write(ctrl)
        finally:
            I2C.Sensors.end_tx()


    def read(self):
        try:
            I2C.Sensors.start_tx(self.__addr)
            ctrl = I2C.Sensors.read(1)
        finally:
            I2C.Sensors.end_tx()

        return ctrl


    def reset(self):
        self.enable(False, False)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PCA9543A:{addr:0x%02x, ctrl:0x%02x}" % (self.__addr, self.read())
