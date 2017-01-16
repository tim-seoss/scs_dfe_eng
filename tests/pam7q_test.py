#!/usr/bin/env python3

'''
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_core.location.gpgga import GPGGA
from scs_core.location.gpgll import GPGLL
from scs_core.location.gpgsa import GPGSA
from scs_core.location.gpgsv import GPGSV
from scs_core.location.gprmc import GPRMC
from scs_core.location.gpvtg import GPVTG

from scs_dfe.gps.pam7q import PAM7Q


# --------------------------------------------------------------------------------------------------------------------

gps = PAM7Q()
print(gps)
print("-")
try:
    # ----------------------------------------------------------------------------------------------------------------

    print("open...")

    gps.open()
    print(gps)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    print("report...")

    msg = gps.report(GPGGA)
    print(msg)
    print("-")

    msg = gps.report(GPGLL)
    print(msg)
    print("-")

    msg = gps.report(GPGSV)
    print(msg)
    print("-")

    msg = gps.report(GPGSA)
    print(msg)
    print("-")

    gpmrc = gps.report(GPRMC)
    print(gpmrc)
    print("-")

    msg = gps.report(GPVTG)
    print(msg)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    print("report all...")

    msgs = gps.report_all()

    for msg in msgs:
        print(msg)
        print("-")

    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    if gpmrc is not None:
        print("position: %s, %s  time: %s" % (gpmrc.loc.deg_lat(), gpmrc.loc.deg_lng(), gpmrc.datetime.as_iso8601()))
        print("=")


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: test location class

    print("=")



except KeyboardInterrupt as ex:
    print("pamq7_test: " + type(ex).__name__)


    # ----------------------------------------------------------------------------------------------------------------

finally:
    print("close...")

    gps.close()
    print(gps)
    print("=")
