'''
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.gas.pt1000_datum import Pt1000Datum


# --------------------------------------------------------------------------------------------------------------------

class Pt1000(object):
    '''
    classdocs
    '''

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, calib):
        '''
        Constructor
        '''
        self.__calib = calib


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe):
        v = afe.sample_raw_tmp()

        return Pt1000Datum.construct(self.__calib, v)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calib(self):
        return self.__calib


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Pt1000:{calib:%s}" % self.calib
