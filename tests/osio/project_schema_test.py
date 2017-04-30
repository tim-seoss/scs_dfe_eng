#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.gas.afe_calib import AFECalib
from scs_core.osio.config.project_topic import ProjectTopic
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calib = AFECalib.load_from_host(Host)
print(calib)
print("-")

gas_names = calib.gas_names()
print(gas_names)
print("-")

topic = ProjectTopic.find_gases_topic(gas_names)
print(topic)
print("-")

print(JSONify.dumps(topic))
