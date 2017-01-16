'''
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from collections import OrderedDict

from scs_core.data.datum import Datum

from scs_dfe.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class PIDCalib(SensorCalib):
    '''
    classdocs
    '''

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        pidELC = jdict.get('pid_zero_mv')
        pidSENS = jdict.get('pid_sensitivity_mv_ppm')

        return PIDCalib(serial_number, sensor_type, pidELC, pidSENS)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, pidELC, pidSENS):
        '''
        Constructor
        '''
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__pidELC = Datum.int(pidELC)                 # PID electronic zero                   mV
        self.__pidSENS = Datum.float(pidSENS, 3)          # PID sensitivity                       mV / ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['pid_zero_mv'] = self.pidELC
        jdict['pid_sensitivity_mv_ppm'] = self.pidSENS

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pidELC(self):
        return self.__pidELC


    @property
    def pidSENS(self):
        return self.__pidSENS


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalib:{serial_number:%s, sensor_type:%s, pidELC:%d, pidSENS:%0.3f}" % \
                    (self.serial_number, self.sensor_type, self.pidELC, self.pidSENS)
