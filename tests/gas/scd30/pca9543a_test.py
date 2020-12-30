#!/usr/bin/env python3

"""
Created on 20 Nov 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.scd30.pca9543a import PCA9543A

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    selector = PCA9543A()
    print(selector)
    print("-")

    # ----------------------------------------------------------------------------------------------------------------
    # selector...

    selector.enable(True, False)
    print(selector)

    selector.enable(False, True)
    print(selector)

    selector.reset()
    print(selector)

finally:
    I2C.Sensors.close()
