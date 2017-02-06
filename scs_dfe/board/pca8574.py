"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class PCA8574(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr


    # ----------------------------------------------------------------------------------------------------------------

    def read(self):
        try:
            I2C.start_tx(self.__addr)
            byte = I2C.read(1)
        finally:
            I2C.end_tx()

        return byte


    def write(self, byte):
        try:
            I2C.start_tx(self.__addr)
            I2C.write(byte)
        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PCA8574:{addr:0x%02x}" % self.__addr
