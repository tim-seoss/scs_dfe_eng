#!/usr/bin/env python3

"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.board.io import IO
from scs_dfe.board.pca8574 import PCA8574State

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    io = IO()
    print(io)

    state = PCA8574State.load_from_file(IO.filename())
    print(state)

    print("led RED was:%s" % io.led_red)

    io.gps_power = IO.LOW
    io.opc_power = IO.LOW

    io.led_red = IO.LOW

    print("led RED is:%s" % io.led_red)

    state = PCA8574State.load_from_file(IO.filename())
    print(state)

finally:
    I2C.close()
