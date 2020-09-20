#!/usr/bin/env python3

"""
Created on 16 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.interface.opcube.opcube_mcu_t1 import OPCubeMCUt1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

# --------------------------------------------------------------------------------------------------------------------
# resources...

controller = OPCubeMCUt1(OPCubeMCUt1.DEFAULT_ADDR)
print("controller: %s" % controller)

conf = SHTConf.load(Host)
sht = conf.ext_sht()
print("sht: %s" % sht)
print("-")


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ident = controller.version_ident()
    print("ident: [%s]" % ident)

    tag = controller.version_tag()
    print("tag: [%s]" % tag)

    print("-")

    climate = sht.sample()
    print("climate: %s" % climate)

    temperature = controller.read_temperature()
    print("temperature: %s" % temperature)

    temperature_count = controller.read_temperature_count()
    print("temperature_count: %s" % temperature_count)

    t30 = controller.read_t30()
    print("t30: %s" % t30)

    t130 = controller.read_t130()
    print("t130: %s" % t130)

    print("-")

    print("LED...")
    on1 = True
    on2 = False

    for _ in range(10):
        controller.led1(on1)
        controller.led2(on2)
        on1 = not on1
        on2 = not on2

        time.sleep(0.5)

    print("switch...")
    switch_state = controller.switch_state()
    print("switch state: %s" % switch_state)

    while True:
        time.sleep(0.1)
        switch_state = controller.switch_state()

        if not switch_state:
            break

    print("switch state: %s" % switch_state)

except KeyboardInterrupt:
    print()

finally:
    I2C.close()
