#!/usr/bin/env python3

"""
Created on 22 Sep 2016

Requires SystemID document.

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.gas.a4_datum import A4Datum
from scs_core.gas.afe_datum import AFEDatum
from scs_core.gas.pid_datum import PIDDatum
from scs_core.gas.pt1000_datum import Pt1000Datum
from scs_core.gas.sensor import Sensor
from scs_core.particulate.pmx_datum import PMxDatum

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

tag = "scs-ap1-0"
print(tag)
print("-")


sensors = (Sensor.find(Sensor.CODE_OX), Sensor.find(Sensor.CODE_NO2), Sensor.find(Sensor.CODE_NO),
           Sensor.find(Sensor.CODE_VOC_PPM))
print(sensors)
print("-")


# --------------------------------------------------------------------------------------------------------------------

pt1 = Pt1000Datum(0.234567, 12.3)
print(pt1)
print("-")

a4_1 = A4Datum(0.123456, 0.654321)
print(a4_1)

a4_2 = A4Datum(1.234567, 6.543210)
print(a4_2)

a4_3 = A4Datum(2.345678, 5.432101)
print(a4_3)

pid = PIDDatum(0.123456, 23)
print(pid)
print("-")

sn1 = sensors[0].gas_name
sn2 = sensors[1].gas_name
sn3 = sensors[2].gas_name
sn4 = sensors[3].gas_name

afe = AFEDatum(pt1, (sn1, a4_1), (sn2, a4_2), (sn3, a4_3), (sn4, pid))
print(afe)
print("-")


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()

pmx = PMxDatum(now, 11, 22, 33)
print(pmx)
print("-")


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()
print(now)
print("-")


# --------------------------------------------------------------------------------------------------------------------

sample = Sample(tag, now, ('afe', afe), ('pmx', pmx))
print(sample)
print("-")

jstr = JSONify.dumps(sample)
print(jstr)
print("-")
