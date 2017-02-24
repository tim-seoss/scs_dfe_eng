"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum

from scs_dfe.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class A4Calib(SensorCalib):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # print("jdict: %s\n" % jdict)

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        weELC = jdict.get('we_electronic_zero_mv')
        weCAL = jdict.get('we_sensor_zero_mv')
        weTOT = jdict.get('we_total_zero_mv')

        aeELC = jdict.get('ae_electronic_zero_mv')
        aeCAL = jdict.get('ae_sensor_zero_mv')
        aeTOT = jdict.get('ae_total_zero_mv')

        weSENS = jdict.get('we_sensitivity_mv_ppb')
        weXSENS = jdict.get('we_cross_sensitivity_ox_no2_mv_ppb')

        return A4Calib(serial_number, sensor_type, weELC, weCAL, weTOT, aeELC, aeCAL, aeTOT, weSENS, weXSENS)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, weELC, weCAL, weTOT, aeELC, aeCAL, aeTOT, weSENS, weXSENS=None):
        """
        Constructor
        """
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__weELC = Datum.int(weELC)                 # WE electronic zero                    mV
        self.__weCAL = Datum.int(weCAL)                 # WE sensor zero at 23 ºC               mV
        self.__weTOT = Datum.int(weTOT)                 # total WE zero                         mV

        self.__aeELC = Datum.int(aeELC)                 # Aux electronic zero                   mV
        self.__aeCAL = Datum.int(aeCAL)                 # Aux sensor zero at 23 ºC              mV
        self.__aeTOT = Datum.int(aeTOT)                 # total Aux zero                        mV

        self.__weSENS = Datum.float(weSENS, 3)          # WE sensitivity                        mV / ppb
        self.__weXSENS = Datum.float(weXSENS, 3)        # WE cross-sensitivity                  mV / ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['we_electronic_zero_mv'] = self.weELC
        jdict['we_sensor_zero_mv'] = self.weCAL
        jdict['we_total_zero_mv'] = self.weTOT

        jdict['ae_electronic_zero_mv'] = self.aeELC
        jdict['ae_sensor_zero_mv'] = self.aeCAL
        jdict['ae_total_zero_mv'] = self.aeTOT

        jdict['we_sensitivity_mv_ppb'] = self.weSENS
        jdict['we_cross_sensitivity_ox_no2_mv_ppb'] = self.weXSENS if self.weXSENS else "n/a"

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def weELC(self):
        return self.__weELC


    @property
    def weCAL(self):
        return self.__weCAL


    @property
    def weTOT(self):
        return self.__weTOT


    @property
    def aeELC(self):
        return self.__aeELC


    @property
    def aeCAL(self):
        return self.__aeCAL


    @property
    def aeTOT(self):
        return self.__aeTOT


    @property
    def weSENS(self):
        return self.__weSENS


    @property
    def weXSENS(self):
        return self.__weXSENS


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calib:{serial_number:%s, sensor_type:%s, weELC:%s, weCAL:%s, weTOT:%s, aeELC:%s, aeCAL:%s, " \
               "aeTOT:%s, weSENS:%s, weXSENS:%s}" % \
                    (self.serial_number, self.sensor_type, self.weELC, self.weCAL, self.weTOT, self.aeELC, self.aeCAL,
                     self.aeTOT, self.weSENS, self.weXSENS)
