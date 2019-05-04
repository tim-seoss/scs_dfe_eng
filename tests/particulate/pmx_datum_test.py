#!/usr/bin/env python3

"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.particulate.pmx_datum import PMxDatum


# --------------------------------------------------------------------------------------------------------------------

now = LocalizedDatetime.now()

pmx = PMxDatum(now, 11, 22, None, 33)
print(pmx)
print("-")

jstr = JSONify.dumps(pmx)
print(jstr)
print("-")
