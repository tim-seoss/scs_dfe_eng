#!/usr/bin/env python3

"""
Created on 8 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.climate.icp10101 import ICP10101

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------


try:
    I2C.Sensors.open()

    barometer = ICP10101(ICP10101.DEFAULT_ADDR)
    print(barometer)

    barometer.init()
    print(barometer)

    id = barometer.id()
    print("id: %s" % id)

    datum = barometer.sample()
    print(datum)

    print(JSONify.dumps(datum))

finally:
    I2C.Sensors.close()
