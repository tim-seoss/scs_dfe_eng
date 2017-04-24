#!/usr/bin/env python3

"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.sensor import Sensor

from scs_core.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

sensor_type = Sensor.CODE_CO
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.CODE_H2S
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.CODE_NO
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.CODE_NO2
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.CODE_OX
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")


sensor_type = Sensor.CODE_SO2
print(sensor_type)

tc = TempComp.find(sensor_type)
print(tc)
print("-")

# --------------------------------------------------------------------------------------------------------------------

temp = -30.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))

comp = tc.cf_t(temp)
print("comp:%0.2f" % comp)
print("-")

temp = 25.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))

comp = tc.cf_t(temp)
print("comp:%0.2f" % comp)
print("-")

temp = 50.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))

comp = tc.cf_t(temp)
print("comp:%0.2f" % comp)
print("-")

temp = 60.0
print("temp:%0.1f" % temp)
print("in range:%s" % TempComp.in_range(temp))
print("-")
