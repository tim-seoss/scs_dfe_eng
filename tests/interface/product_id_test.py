#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_id import InterfaceID


# --------------------------------------------------------------------------------------------------------------------

product_id = InterfaceID()
print(product_id)
print("-")

jstr = JSONify.dumps(product_id)
print(jstr)
print("-")

