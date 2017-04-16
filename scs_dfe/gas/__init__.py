"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.a4 import A4
from scs_dfe.gas.ads1115 import ADS1115
from scs_dfe.gas.mcp3425 import MCP3425
from scs_dfe.gas.pid import PID
from scs_dfe.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

ADS1115.init()

MCP3425.init()

TempComp.init()     # must be initialised before sensors

A4.init()

PID.init()
