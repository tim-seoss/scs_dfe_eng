#!/usr/bin/env python3

"""
Created on 19 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.pressure.mpl115a2 import MPL115A2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    barometer = MPL115A2()
    print(barometer)

    barometer.init()

    pressure, temperature = barometer.sample()

    print("pressure: %s" % pressure)
    print("temperature: %s" % temperature)

    print(barometer)

finally:
    I2C.close()
