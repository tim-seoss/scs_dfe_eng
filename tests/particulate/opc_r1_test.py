#!/usr/bin/env python3

"""
Created on 22 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.particulate.opc_r1.opc_r1 import OPCR1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

opc = None

try:
    I2C.open(Host.I2C_SENSORS)

    opc = OPCR1(Host.opc_spi_bus(), Host.opc_spi_device())
    print(opc)
    print("-")

    opc.power_on()

    firmware = opc.firmware()
    print(firmware)

    # status = opc.status()
    # print("status:%s" % status)

    print("on...")
    opc.operations_on()

    print("waiting...")
    time.sleep(5)

    '''
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
    '''

    print("off...")
    opc.operations_off()
    time.sleep(5)

    # status = opc.status()
    # print("status:%s" % status)

    opc.power_off()

except KeyboardInterrupt:
    print("opc_r1_test: KeyboardInterrupt", file=sys.stderr)

finally:
    I2C.close()
