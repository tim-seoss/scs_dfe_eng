#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.osio.config.project_topic import ProjectTopic

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calib = AFECalib.load_from_host(Host)
print(calib)
print("-")

gas_names = calib.gas_names()
print(gas_names)
print("-")

schema = ProjectTopic.find_gas_schema(gas_names)
print(schema)
print("-")

print(JSONify.dumps(schema))
