#!/usr/bin/env python3

"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.sensor import Sensor
from scs_dfe.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

sensor_type = Sensor.CO_A4
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.H2S_A4
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.NO_A4
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.NO2_A4
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.OX_A4
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.SO2_A4
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")

# --------------------------------------------------------------------------------------------------------------------

temp = -30.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))

comp = tc.cfT(temp)
print("comp:%0.2f" % comp)
print("-")

temp = 25.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))

comp = tc.cfT(temp)
print("comp:%0.2f" % comp)
print("-")

temp = 50.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))

comp = tc.cfT(temp)
print("comp:%0.2f" % comp)
print("-")

temp = 60.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))
print("-")
