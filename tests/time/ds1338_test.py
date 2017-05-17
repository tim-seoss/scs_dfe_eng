#!/usr/bin/env python3

"""
Created on 16 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import tzlocal

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.rtc_datetime import RTCDatetime

from scs_dfe.time.ds1338 import DS1338

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

set_time = False


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()
print(now)
print("-")

rtc_datetime = RTCDatetime.construct_from_localized_datetime(now)
print(rtc_datetime)
print("-")

try:
    I2C.open(Host.I2C_SENSORS)

    # clock...
    DS1338.square_wave(False)

    if set_time:
        DS1338.set_time(rtc_datetime)

    DS1338.dump()
    print("-")

    rtc_datetime = DS1338.get_time()
    print("rtc_datetime: % s" % rtc_datetime)

    localized_datetime = rtc_datetime.as_localized_datetime(tzlocal.get_localzone())
    print(localized_datetime)
    print("-")

    # RAM...
    addr = 1
    val = 0x45
    DS1338.write(addr, val)
    read = DS1338.read(addr)

    print("ram[%d]: 0x%02x" % (addr, read))

finally:
    I2C.close()
