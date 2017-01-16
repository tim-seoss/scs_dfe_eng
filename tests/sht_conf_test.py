#!/usr/bin/env python3

'''
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.climate.sht_conf import SHTConf
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

int_addr = 0x45
print("ext: 0x%02x - %d" % (int_addr, int_addr))
print("-")

ext_addr = 0x44
print("ext: 0x%02x - %d" % (ext_addr, ext_addr))
print("-")

conf = SHTConf(int_addr, ext_addr)
print(conf)
print("-")

conf.save(Host)

conf = SHTConf.load(Host)
print(conf)
print("-")
