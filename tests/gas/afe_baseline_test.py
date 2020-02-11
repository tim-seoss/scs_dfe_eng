#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline, BaselineEnvironment


# --------------------------------------------------------------------------------------------------------------------

baseline = AFEBaseline.construct_from_jdict(None)
print(baseline)
print("-")

now = LocalizedDatetime.now()
baseline = AFEBaseline([
    SensorBaseline(now, 111, BaselineEnvironment(1.1, 2.2, 3.3)),
    SensorBaseline(now, 222, BaselineEnvironment(11.1, 22.2, 33.3)),
    SensorBaseline(now, 333, BaselineEnvironment(111.1, 222.2, 333.3)),
    SensorBaseline(now, 444, BaselineEnvironment(1111.1, 2222.2, 3333.3))])

print(baseline)
print("-")

jstr = JSONify.dumps(baseline)
print(jstr)
print("-")
