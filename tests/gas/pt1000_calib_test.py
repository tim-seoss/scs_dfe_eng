#!/usr/bin/env python3

"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.gas.pt1000 import Pt1000

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

v20 = 0.295


# --------------------------------------------------------------------------------------------------------------------

calib = Pt1000Calib.load_from_host(Host)
print(calib)
print("=")


# --------------------------------------------------------------------------------------------------------------------

calib = Pt1000Calib(None, v20)
print(calib)
print("-")

jstr = JSONify.dumps(calib)
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

calib = Pt1000Calib.construct_from_jdict(jdict)
print(calib)
print("=")

pt1000 = Pt1000(calib)
print(pt1000)
print("-")

calib.save(Host)

