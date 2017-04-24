#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import datetime

from scs_core.data.json import JSONify
from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline


# --------------------------------------------------------------------------------------------------------------------

baseline = AFEBaseline.construct_from_jdict(None)
print(baseline)
print("-")

now = datetime.datetime.now()
baseline = AFEBaseline([SensorBaseline(now.date(), 111), SensorBaseline(now.date(), 222),
                        SensorBaseline(now.date(), 333), SensorBaseline(now.date(), 444)])
print(baseline)
print("-")

jstr = JSONify.dumps(baseline)
print(jstr)
print("-")
