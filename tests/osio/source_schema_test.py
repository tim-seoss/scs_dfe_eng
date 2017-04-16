#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.osio.config.source_schema import SourceSchema

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calib = AFECalib.load_from_host(Host)
print(calib)
print("-")

gas_names = calib.gas_names()
print(gas_names)
print("-")

schema = SourceSchema.find(gas_names)
print(schema)
print("-")
