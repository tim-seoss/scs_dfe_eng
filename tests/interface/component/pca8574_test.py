#!/usr/bin/env python3

"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.interface.component.io import IO
from scs_dfe.interface.component.pca8574 import PCA8574
from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    io = PCA8574.construct(IO.ADDR, Host.lock_dir(), "dfe_io.json")
    print(io)

    byte = io.read()
    print("was byte:%02x" % byte)

    io.write(0xf0)

    byte = io.read()
    print("now byte:%02x" % byte)

except KeyboardInterrupt:
    print("pca8574_test: terminated", file=sys.stderr)

finally:
    I2C.close()
