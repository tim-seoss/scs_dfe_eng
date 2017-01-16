#!/usr/bin/env python3

'''
Created on 31 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.network.wpa_supplicant import WPASupplicant


# --------------------------------------------------------------------------------------------------------------------

supp = WPASupplicant('Solaris', 'fortnum', WPASupplicant.KEY_MGMT)
print(supp)
print("-")

entry = supp.as_entry()
print(entry)
print("-")

supp = WPASupplicant.construct_from_entry(entry)
print(supp)
print("-")
