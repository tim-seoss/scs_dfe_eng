#!/usr/bin/env python3

"""
Created on 19 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.pressure.mpl115a2_calib import MPL115A2Calib

from scs_dfe.pressure.mpl115a2 import MPL115A2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calib = MPL115A2Calib(None, MPL115A2Calib.DEFAULT_C25)

try:
    I2C.open(Host.I2C_SENSORS)

    barometer = MPL115A2(calib)

    barometer.init()
    print(barometer)

    datum = barometer.sample()
    print(datum)

finally:
    I2C.close()
