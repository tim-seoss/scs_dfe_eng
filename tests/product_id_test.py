#!/usr/bin/env python3

'''
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.board.product_id import ProductID

from scs_core.common.json import JSONify

 
# --------------------------------------------------------------------------------------------------------------------

product_id = ProductID()
print(product_id)
print("-")

jstr = JSONify.dumps(product_id)
print(jstr)
print("-")

