#!/usr/bin/env python3

"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.position.gpgga import GPGGA
from scs_core.position.gpgll import GPGLL
from scs_core.position.gpgsa import GPGSA
from scs_core.position.gpgsv import GPGSV
from scs_core.position.gprmc import GPRMC
from scs_core.position.gpvtg import GPVTG

from scs_core.position.gps_location import GPSLocation

from scs_dfe.gps.pam7q import PAM7Q

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

gps = PAM7Q(Host.gps_device())
print(gps)
print("-")


try:
    # ----------------------------------------------------------------------------------------------------------------

    print("power up...")
    gps.power_on()

    print("open...")
    gps.open()
    print(gps)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    print("report...")

    gga = gps.report(GPGGA)
    print(gga)
    print("-")

    gll = gps.report(GPGLL)
    print(gll)
    print("-")

    gsv = gps.report(GPGSV)
    print(gsv)
    print("-")

    gsa = gps.report(GPGSA)
    print(gsa)
    print("-")

    rmc = gps.report(GPRMC)
    print(rmc)
    print("-")

    vtg = gps.report(GPVTG)
    print(vtg)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    print("report all...")

    msgs = gps.report_all()

    for msg in msgs:
        print(msg)
        print("-")

    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    if rmc is not None:
        print("position: %s, %s  time: %s" % (rmc.loc.deg_lat(), rmc.loc.deg_lng(), rmc.datetime.as_iso8601()))

        location = GPSLocation.construct(gga)
        print(location)

        print("=")


except KeyboardInterrupt:
    print("pamq7_test: KeyboardInterrupt", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------

finally:
    print("close...")
    gps.close()
    print(gps)
    print("=")

    # print("power down...")
    # gps.power_off()

    I2C.close()
