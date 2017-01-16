#!/usr/bin/env python3

'''
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.climate.sht_datum import SHTDatum

from scs_core.common.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

sht = SHTDatum(54.3, 23.4)
print(sht)
print("-")

jstr = JSONify.dumps(sht)
print(jstr)
print("-")
