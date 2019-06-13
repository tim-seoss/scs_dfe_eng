#!/usr/bin/env python3

"""
Created on 12 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.board.rpz_header_t1_f1 import RPzHeaderT1F1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

header = RPzHeaderT1F1(RPzHeaderT1F1.DEFAULT_ADDR)
print(header)


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ident = header.version_ident()
    print("ident: [%s]" % ident)

    tag = header.version_tag()
    print("tag: [%s]" % tag)

    print("-")

    v_batt = header.read_batt_v()
    print("v_batt: %0.1f V" % v_batt)

    c_current = header.read_current_count()
    print("c_current: %d" % c_current)

    print("-")

    while True:
        button_pressed = header.button_pressed()

        if button_pressed:
            print("button pressed")
            break

        time.sleep(1)

finally:
    I2C.close()
