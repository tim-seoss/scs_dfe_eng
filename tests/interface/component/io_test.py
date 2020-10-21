#!/usr/bin/env python3

"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_dfe.interface.component.io import IO
from scs_dfe.interface.component.pca8574 import PCA8574State

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

filename = os.path.join(Host.lock_dir(), "dfe_io.json")

I2C.open(Host.I2C_SENSORS)

try:
    io = IO(None)
    print(io)

    state = PCA8574State.load(filename)
    print(state)

    print("led RED was:%s" % io.led_red)
    print("led GREEN was:%s" % io.led_green)

    io.led_red = not io.led_red
    io.led_green = not io.led_green

    print("led RED is:%s" % io.led_red)
    print("led GREEN is:%s" % io.led_green)

    state = PCA8574State.load(filename)
    print(state)

finally:
    I2C.close()
