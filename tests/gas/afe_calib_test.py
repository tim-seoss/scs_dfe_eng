#!/usr/bin/env python3

"""
Created on 29 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calib = AFECalib.load_from_host(Host)
print(calib)
print("-")

pt1000_calib = calib.pt100_calib
print(pt1000_calib)
print("-")

sensor_types = calib.sensor_types()
print("sensor_types:%s" % sensor_types)
print("-")

jstr = JSONify.dumps(calib)
print(jstr)
print("-")

