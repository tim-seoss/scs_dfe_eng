#!/usr/bin/env python3

"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

# --------------------------------------------------------------------------------------------------------------------

opc = None

try:
    I2C.open(Host.I2C_SENSORS)

    opc = OPCN3(Host.opc_spi_bus(), Host.opc_spi_device())
    print(opc)
    print("-")

    opc.power_on()
    time.sleep(5)

    firmware = opc.firmware()
    print(firmware)

    status = opc.status()
    print("status:%s" % status)

    print("on...")
    opc.operations_on()

    version = opc.version()
    print("major:[%d] minor:[%d]" % version)

    serial = opc.serial_no()
    print("type:[%s] number:[%s]" % serial)

    status = opc.status()
    print("status:%s" % status)

    timer = IntervalTimer(10.0)

    while timer.true():
        datum = opc.sample()

        print(JSONify.dumps(datum))
        sys.stdout.flush()

        # opc.reset()

except KeyboardInterrupt:
    print("opc_n3_test: KeyboardInterrupt", file=sys.stderr)

finally:
    if opc:
        print("off...")
        opc.operations_off()

        status = opc.status()
        print("status:%s" % status)

        # opc.power_off()

    I2C.close()
