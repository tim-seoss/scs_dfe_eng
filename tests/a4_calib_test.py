#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.a4_calib import A4Calib


# --------------------------------------------------------------------------------------------------------------------

serial_number = 123456789
sensor_type = 'CO-A4'

weELC = 275
weCAL = -8
weTOT = 278

aeELC = 273
aeCAL = -3
aeTOT = 270

weSENS = 0.321
weXSENS = None


# --------------------------------------------------------------------------------------------------------------------

calib = A4Calib(serial_number, sensor_type, weELC, weCAL, weTOT, aeELC, aeCAL, aeTOT, weSENS, weXSENS)
print(calib)
print("-")
