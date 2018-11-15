#!/usr/bin/env python3

"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_dfe.particulate.opc_n3 import OPCN3

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

io = None
opc = None

try:
    I2C.open(Host.I2C_SENSORS)

    opc = OPCN3(Host.opc_spi_bus(), Host.opc_spi_device())
    print(opc)
    print("-")

    sys.stdout.flush()

    opc.power_on()

    '''
    firmware = opc.firmware()
    print("firmware:[%s]" % firmware)
    print("-")

    sys.stdout.flush()

    version = opc.firmware_version()
    print("major:[%d] minor:[%d]" % version)
    print("-")

    sys.stdout.flush()


    sys.stdout.flush()
    '''

    version = opc.firmware()
    print(version)

    opc.laser_on()
    time.sleep(0.020)

    opc.fan_on()
    time.sleep(6.000)

    # time.sleep(5)
    # opc.sample()         # first report is always zero
    #
    # for i in range(100):
    #     time.sleep(5)
    #
    #     print("%d:" % i)
    #     datum = opc.sample()
    #     print(datum)
    #     print("-")

    serial = opc.serial_no()
    print("type:[%s] number:[%s]" % serial)
    print("-")

except KeyboardInterrupt:
    print("opc_n3_test: KeyboardInterrupt", file=sys.stderr)

finally:
    if opc:
        # opc.operations_off()
        opc.power_off()
        pass

    I2C.close()


