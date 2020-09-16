#!/usr/bin/env python3

"""
Created on 16 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.interface.opcube.opcube_mcu_t1 import OPCubeMCUt1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

# --------------------------------------------------------------------------------------------------------------------

header = OPCubeMCUt1(OPCubeMCUt1.DEFAULT_ADDR)
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

    print("-")

    print("LED...")
    on = True

    for _ in range(10):
        header.led1(on)
        header.led2(on)
        on = not on
        time.sleep(0.5)

    # exit(0)

    print("button...")

    count = 0

    while True:
        time.sleep(1)

        switch_state = header.switch_state()
        print("switch state: %d" % switch_state)

        count += 1

finally:
    I2C.close()
