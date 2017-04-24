#!/usr/bin/env python3

"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.gas.pid_calib import PIDCalib


# --------------------------------------------------------------------------------------------------------------------

serial_number = "143456789"
sensor_type = "PIDNH"

pidELC = 275
pidSENS = 0.321


# --------------------------------------------------------------------------------------------------------------------

calib = PIDCalib(serial_number, sensor_type, pidELC, pidSENS)
print(calib)
print("-")

jstr = JSONify.dumps(calib)
print(jstr)
print("-")
