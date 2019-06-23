#!/usr/bin/env python3

"""
Created on 23 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.particulate.opc_n2.opc_n2 import OPCN2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

opc = None

try:
    I2C.open(Host.I2C_SENSORS)

    opc = OPCN2(False, Host.opc_spi_bus(), Host.opc_spi_device())
    print(opc)
    print("-")

    print("booting...")
    opc.power_on()
    print("-")

    print("firmware...")
    firmware = opc.firmware()
    print(firmware)
    print("-")

    time.sleep(1)

    print("on...")
    opc.operations_on()
    print("-")

    print("running...")
    time.sleep(2)

    timer = IntervalTimer(10.0)

    opc.sample()                    # clear histograms and timer

    checkpoint = time.time()

    for _ in timer.range(10):
        datum = opc.sample()

        now = time.time()
        print("interval: %0.3f" % round(now - checkpoint, 3))
        checkpoint = now

        print(JSONify.dumps(datum))
        print("-")

        sys.stdout.flush()

except KeyboardInterrupt:
    print("opc_n2_test: KeyboardInterrupt", file=sys.stderr)

finally:
    print("off...")
    opc.operations_off()
    print("-")

    print("shutdown...")
    opc.power_off()
    print("-")

    I2C.close()
