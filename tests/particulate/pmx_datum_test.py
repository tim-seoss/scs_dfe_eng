#!/usr/bin/env python3

"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.particulate.pmx_datum import PMxDatum


# --------------------------------------------------------------------------------------------------------------------

pmx = PMxDatum(11, 22, 33)
print(pmx)
print("-")

jstr = JSONify.dumps(pmx)
print(jstr)
print("-")
