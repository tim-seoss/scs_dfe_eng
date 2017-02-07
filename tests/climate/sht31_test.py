#!/usr/bin/env python3

"""
Created on 7 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_dfe.climate.sht_conf import SHTConf
from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

sht_conf = SHTConf.load_from_host(Host)
sht = sht_conf.ext_sht()

sht.reset()

try:
    while True:
        time.sleep(1)
        datum = sht.sample()
        print(datum)

        print("status: 0x%0.4X" % sht.status)
        print("-")

except KeyboardInterrupt:
    print("sh31_test: terminated", file=sys.stderr)

finally:
    I2C.close()
