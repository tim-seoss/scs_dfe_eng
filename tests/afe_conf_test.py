#!/usr/bin/env python3

'''
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import json

from scs_dfe.gas.afe_conf import AFEConf

from scs_dfe.gas.sensor import Sensor

from scs_host.sys.host import Host

from scs_core.common.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

afe_type = "810-0022-01"
print(afe_type)
print("-")

sensor_types = [Sensor.OX_A431, Sensor.NO2_A43F, Sensor.NO_A4, Sensor.CO_A4]
print(sensor_types)
print("-")

conf = AFEConf(afe_type, sensor_types)
print(conf)
print("=")

conf.save(Host)

conf = AFEConf.load(Host)
print(conf)
print("=")

jstr = JSONify.dumps(conf)
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

conf = AFEConf.construct_from_jdict(jdict)
print(conf)
print("-")

sensors = conf.sensors()
print('\n\n'.join([str(sensor) for sensor in sensors]))
print("-")
