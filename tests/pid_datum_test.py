#!/usr/bin/env python3

'''
Created on 19 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_core.data.json import JSONify

from scs_dfe.gas.pid_datum import PIDDatum


# --------------------------------------------------------------------------------------------------------------------

pid = PIDDatum(0.123456, 23)
print(pid)
print("-")

jstr = JSONify.dumps(pid)
print(jstr)
print("-")
