#!/usr/bin/env python3

'''
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.particulate.pmx_datum import PMxDatum

from scs_dfe.particulate.opc_datum import OPCDatum
from scs_core.common.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

opc = OPCDatum(11, 22, 33, 9.1, [1,2,3,4,5,6,7,8,9], 11.1, 22.2, 33.3, 44.4)
print(opc)
print("-")

jstr = JSONify.dumps(opc)
print(jstr)
print("-")

# cast to PMxDatum...
opc.__class__ = PMxDatum
print(opc)
print("-")
