#!/usr/bin/env python3

'''
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.gas.afe_conf import AFEConf
from scs_dfe.gas.afe_datum import AFEDatum

from scs_dfe.gas.pid_datum import PIDDatum

from scs_dfe.gas.pt1000_datum import Pt1000Datum

from scs_dfe.gas.a4_datum import A4Datum

from scs_host.sys.host import Host

from scs_core.common.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

conf = AFEConf.load(Host)
print(conf)
print("-")

sensors = conf.sensors()
print('\n\n'.join([str(sensor) for sensor in sensors]))
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

jstr = JSONify.dumps(afe)
print(jstr)
print("-")
