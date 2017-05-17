#!/usr/bin/env python3

"""
Created on 16 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_dfe.time.ds1338 import DS1338

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()
print(now)
print("-")

datetime = now.datetime

print("year: %d" % datetime.year)
print("month: %d" % datetime.month)
print("day: %d" % datetime.day)
print("weekday: %s" % datetime.isoweekday())
print("-")

print("hour: %s" % datetime.hour)
print("minute: %s" % datetime.minute)
print("second: %s" % datetime.second)
print("-")

try:
    I2C.open(Host.I2C_SENSORS)

    # DS1338.sqwe(False)
    # time.sleep(1)
    #
    # DS1338.set(2017, 5, 17, 4, 9, 3, 55)
    # DS1338.set(2000, 1, 1, 1, 00, 00, 00)

    # time.sleep(1)
    DS1338.dump()
    print("-")

    addr = 1
    val = 0x34
    DS1338.write(addr, val)
    read = DS1338.read(addr)

    print("ram[%d]: 0x%02x" % (addr, read))

finally:
    I2C.close()
