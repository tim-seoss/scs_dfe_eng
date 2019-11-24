#!/usr/bin/env python3

"""
Created on 23 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.particulate.exegesis.iselut.iselut_n2_v001 import ISELUTN2v1
from scs_core.particulate.exegesis.isecee.isecee_n2_v001 import ISECEEN2v1

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf = OPCConf("N2", 10, False, 0, 1, [ISELUTN2v1.name(), ISECEEN2v1.name()], "ext")
print(conf)
print("-")

print(JSONify.dumps(conf.as_json()))
print("-")

conf.save(Host)
conf = OPCConf.load(Host)
print(conf)
