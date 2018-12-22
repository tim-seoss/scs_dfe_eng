#!/usr/bin/env python3

"""
Created on 22 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.display.led import LED

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    led = LED()
    print(led)
    print("-")

    colour = led.colour
    print("colour: %s" % colour)
    print("-")

    colour = 'G'
    print("valid: %s" % LED.is_valid_colour('G'))

    led.colour = colour
    print("colour: %s" % led.colour)
    print("-")

    time.sleep(1)

    colour = 'R'
    print("valid: %s" % LED.is_valid_colour('G'))

    led.colour = colour
    print("colour: %s" % led.colour)
    print("-")

finally:
    I2C.close()
