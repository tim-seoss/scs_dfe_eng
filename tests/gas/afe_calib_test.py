#!/usr/bin/env python3

"""
Created on 29 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

afe_baseline = AFEBaseline.load(Host)
print(afe_baseline)
print("=")

calib = AFECalib.load(Host)
print(calib)
print("=")

pt1000_calib = calib.pt1000_calib
print(pt1000_calib)
print("=")


for i in range(len(calib)):
    print(calib.sensor_calib(i))
    print("-")

print("=")


for sensor in calib.sensors(afe_baseline):
    print(sensor)
    print("-")

print("=")


gas_names = calib.gas_names()

print("gas_names: %s" % gas_names)

for gas_name in calib.gas_names():
    index = calib.sensor_index(gas_name)
    print("gas_name: %s index: %s" % (gas_name, index))

gas_name = 'XX'
index = calib.sensor_index(gas_name)
print("gas_name: %s index: %s" % (gas_name, index))

print("=")

jstr = JSONify.dumps(calib)
print(jstr)
print("=")
