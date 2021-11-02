#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline


# --------------------------------------------------------------------------------------------------------------------

baseline = AFEBaseline.construct_from_jdict(None)
print(baseline)
print("-")

now = LocalizedDatetime.now().utc()

baseline = AFEBaseline([
    SensorBaseline(now, 111),
    SensorBaseline(now, 222),
    SensorBaseline(now, 333),
    SensorBaseline(now, 444)])

print(baseline)
print("-")

jstr = JSONify.dumps(baseline)
print(jstr)
print("-")
