#!/usr/bin/env python3

"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.gas.afe.mcp3421 import MCP3421

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

temp = None

try:
    I2C.Sensors.open()

    temp = MCP3421(MCP3421.GAIN_4, MCP3421.RATE_15)     # 16 bits
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
