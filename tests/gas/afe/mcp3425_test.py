#!/usr/bin/env python3

"""
Created on 5 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.gas.afe.mcp3425 import MCP3425

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

temp = None

try:
    I2C.Sensors.open()

    temp = MCP3425(MCP3425.GAIN_4, MCP3425.RATE_15)     # 16 bits
    print(temp)

    temp.start_conversion()
    time.sleep(temp.tconv)

    v = temp.read_conversion()
    print("v:%0.6f" % v)

    c = (v - 0.325) * 1000 + 20     # V = 0.297(V20C) + 0.0010 * (T - T20C), sensitivity is 1.0 mV/ K
    print("c:%0.6f" % c)
    print("-")

    v = temp.convert()
    print("v:%0.6f" % v)

    c = (v - 0.325) * 1000 + 20     # V = 0.297(V20C) + 0.0010 * (T - T20C), sensitivity is 1.0 mV/ K
    print("c:%0.6f" % c)

finally:
    if temp:
        temp.release_lock()

    I2C.Sensors.close()
