"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.mcp342x import MCP342X


# --------------------------------------------------------------------------------------------------------------------

class MCP3425(MCP342X):
    """
    Microchip Technology MCP3425 ADC
    """

    ADDR =              0x68

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gain, rate):
        """
        initialise ADC with given gain and rate
        """
        MCP342X.__init__(self, MCP3425.ADDR, gain, rate)
