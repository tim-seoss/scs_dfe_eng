#!/usr/bin/env python3

"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.interface.dfe.dfe import DFE

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

interface = DFE()
print(interface)
print("-")

try:
    I2C.Sensors.open()

    gas_sensors = interface.gas_sensors(Host)
    print(gas_sensors)
    print("-")

    datum = interface.status()
    print(datum)
    print("-")

finally:
    I2C.Sensors.close()
