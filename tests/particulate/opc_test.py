#!/usr/bin/env python3

"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_dfe.board.pca8574 import PCA8574
from scs_dfe.particulate.opc_n2 import OPCN2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

opc = None

try:
    I2C.open(Host.I2C_SENSORS)
    io = PCA8574(0x3f)
    print(io)

    io.write(0xf8)

    opc = OPCN2()
    opc.on()

    version = opc.firmware()
    print(version)

    time.sleep(5)
    opc.sample()         # first report is always zero

    for i in range(100):
        time.sleep(5)

        print("%d:" % i)
        datum = opc.sample()
        print(datum)
        print("-")

except KeyboardInterrupt as ex:
    print("opc_test: " + type(ex).__name__, file=sys.stderr)

finally:
    I2C.close()

    if opc:
        time.sleep(1)
        opc.off()
