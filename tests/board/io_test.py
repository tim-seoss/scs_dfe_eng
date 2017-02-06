#!/usr/bin/env python3

"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.board.io import IOState
from scs_dfe.board.io import IO

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    state = IOState.load(Host)
    print(state)

    io = IO()
    print(io)

    print("led RED was:%s" % io.led_red)

    io.led_red = not io.led_red
    print("led RED is:%s" % io.led_red)

    state = IOState.load(Host)
    print(state)

finally:
    I2C.close()

