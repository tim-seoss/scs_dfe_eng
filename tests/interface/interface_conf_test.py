#!/usr/bin/env python3

"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf = InterfaceConf.load(Host)
print(conf)
print("-")

interface = conf.interface()
print(interface)
print("-")

conf.save(Host)
