"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: 18 bit conversions are not supported.
"""

from scs_dfe.gas.afe.mcp342x import MCP342X


# --------------------------------------------------------------------------------------------------------------------

class MCP3421(MCP342X):
    """
    Microchip Technology MCP3421 ADC
    """

    ADDR =              0x68            # or 0x69

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gain, rate):
        """
        initialise ADC with given gain and rate
        """
        MCP342X.__init__(self, MCP3421.ADDR, gain, rate)
