#!/usr/bin/env python3

"""
Created on 1 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.network.wpa_supplicant_file import WPASupplicantFile


# --------------------------------------------------------------------------------------------------------------------

file = WPASupplicantFile.read()
print(file)
print("-")

file.remove('Solar')

file.write()
print("=")



# --------------------------------------------------------------------------------------------------------------------

'''
supp = WPASupplicant('Solaris', 'fortnum890121')
print(supp)
print("-")

file.insert(supp)
print(file)
print("-")

content = file.write()
print(content)
print("-")
'''
