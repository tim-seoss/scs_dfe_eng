#!/usr/bin/env python3

"""
Created on 29 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.gas.afe_baseline import AFEBaseline
from scs_dfe.gas.afe_calib import AFECalib

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

afe_baseline = AFEBaseline.load_from_host(Host)
print(afe_baseline)
print("-")

calib = AFECalib.load_from_host(Host)
print(calib)
print("-")

pt1000_calib = calib.pt1000_calib
print(pt1000_calib)
print("-")


for i in range(len(calib)):
    print(calib.sensor_calib(i))
    print("-")

for sensor in calib.sensors(afe_baseline):
    print(sensor)
    print("-")


jstr = JSONify.dumps(calib)
print(jstr)
print("-")
