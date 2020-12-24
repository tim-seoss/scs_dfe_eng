#!/usr/bin/env python3

"""
Created on 16 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import tzlocal

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.rtc_datetime import RTCDatetime

from scs_dfe.time.ds1338 import DS1338

from scs_host.bus.i2c import SensorI2C


# --------------------------------------------------------------------------------------------------------------------

set_time = False


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now().utc()
print(now)
print("-")

rtc_datetime = RTCDatetime.construct_from_localized_datetime(now)
print(rtc_datetime)
print("-")

try:
    SensorI2C.open()

    # clock...
    DS1338.init()

    if set_time:
        DS1338.set_time(rtc_datetime)

    rtc_datetime = DS1338.get_time()
    print("rtc_datetime: %s" % rtc_datetime)

    localized_datetime = rtc_datetime.as_localized_datetime(tzlocal.get_localzone())
    print(localized_datetime)
    print("-")

    control = DS1338.get_ctrl()
    print("control: 0x%02x" % control)
    print("-")

    # RAM...
    addr = 1
    val = 0x45
    DS1338.write(addr, val)
    read = DS1338.read(addr)

    print("ram[%d]: 0x%02x" % (addr, read))
    print("-")

finally:
    SensorI2C.close()
