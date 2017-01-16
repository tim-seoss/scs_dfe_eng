'''
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from abc import abstractmethod

from scs_dfe.gas.ads1115 import ADS1115


# --------------------------------------------------------------------------------------------------------------------

class Sensor(object):
    '''
    classdocs
    '''

    CO_A4 =     'CO-A4'
    H2S_A4 =    'H2S-A4'
    NO_A4 =     'NO-A4'
    NO2_A43F =  'NO2-A43F'
    OX_A431 =   'OX-A431'
    SO2_A4 =    'SO2-A4'

    PID_A1 =    'PID-A1'
    PID_AH =    'PID-AH'

    __GAS = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        # late imports to prevent circularity
        # TODO: remove late imports
        from scs_dfe.gas.a4 import A4
        from scs_dfe.gas.pid import PID

        cls.__GAS = {
                   cls.CO_A4:       A4(cls.CO_A4,     'CO',     ADS1115.GAIN_2p048),
                   cls.H2S_A4:      A4(cls.H2S_A4,    'H2S',    ADS1115.GAIN_2p048),
                   cls.NO_A4:       A4(cls.NO_A4,     'NO',     ADS1115.GAIN_2p048),
                   cls.NO2_A43F:    A4(cls.NO2_A43F,  'NO2',    ADS1115.GAIN_2p048),
                   cls.OX_A431:     A4(cls.OX_A431,   'Ox',     ADS1115.GAIN_2p048),
                   cls.SO2_A4:      A4(cls.SO2_A4,    'SO2',    ADS1115.GAIN_2p048),

                   cls.PID_A1:      PID(cls.PID_A1,   'VOC',    ADS1115.GAIN_4p096),
                   cls.PID_AH:      PID(cls.PID_AH,   'VOC',    ADS1115.GAIN_4p096)
                }


    @classmethod
    def find(cls, sensor_type):
        if sensor_type is None:
            return None

        if not sensor_type in cls.__GAS:
            raise ValueError("Sensor.find: unrecognised sensor type: %s." % sensor_type)

        return cls.__GAS[sensor_type]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain, calib = None):
        '''
        Constructor
        '''
        self.__sensor_type = sensor_type

        self.__gas_name = gas_name
        self.__adc_gain = adc_gain

        self.__calib = calib


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def sample(self, afe, temp, index):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sensor_type(self):
        return self.__sensor_type


    @property
    def gas_name(self):
        return self.__gas_name


    @property
    def adc_gain(self):
        return self.__adc_gain


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def calib(self):
        return self.__calib


    @calib.setter
    def calib(self, calib):
        self.__calib = calib


# --------------------------------------------------------------------------------------------------------------------

Sensor.init()
