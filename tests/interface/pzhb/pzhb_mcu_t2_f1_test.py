#!/usr/bin/env python3

"""
Created on 21 Aug 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.interface.pzhb.pzhb_mcu_t2_f1 import PZHBMCUt2f1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

header = PZHBMCUt2f1(PZHBMCUt2f1.DEFAULT_ADDR)
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

    print("LED...")
    on = True

    for _ in range(10):
        header.led1(on)
        header.led2(on)
        on = not on
        time.sleep(2)

    # exit(0)

    print("button...")

    header.button_enable()

    count = 0

    while True:
        time.sleep(1)

        button_pressed = header.button_pressed()

        if button_pressed:
            print("button pressed: %d" % count)
            break

        count += 1

finally:
    I2C.close()
