"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod

from scs_dfe.gas.ads1115 import ADS1115


# --------------------------------------------------------------------------------------------------------------------

class Sensor(object):
    """
    classdocs
    """
    CODE_CO =       '132'           # CO A4
    CODE_H2S =      '133'           # H2SA4
    CODE_NO =       '130'           # NO A4
    CODE_NO2 =      '212'           # NOGA4
    CODE_OX =       '214'           # OXGA4
    CODE_SO2 =      '134'           # SO2A4

    CODE_VOC_PPM =  '142'           # PIDN1
    CODE_VOC_PPB =  '143'           # PIDNH

    __GAS =     None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        # late imports to prevent circularity
        # TODO: remove late imports
        from scs_dfe.gas.a4 import A4
        from scs_dfe.gas.pid import PID

        cls.__GAS = {
            cls.CODE_CO:         A4(cls.CODE_CO,        'CO',   ADS1115.GAIN_2p048),
            cls.CODE_H2S:        A4(cls.CODE_H2S,       'H2S',  ADS1115.GAIN_2p048),
            cls.CODE_NO:         A4(cls.CODE_NO,        'NO',   ADS1115.GAIN_2p048),
            cls.CODE_NO2:        A4(cls.CODE_NO2,       'NO2',  ADS1115.GAIN_2p048),
            cls.CODE_OX:         A4(cls.CODE_OX,        'Ox',   ADS1115.GAIN_2p048),
            cls.CODE_SO2:        A4(cls.CODE_SO2,       'SO2',  ADS1115.GAIN_2p048),

            cls.CODE_VOC_PPM:    PID(cls.CODE_VOC_PPM,  'VOC',  ADS1115.GAIN_4p096),
            cls.CODE_VOC_PPB:    PID(cls.CODE_VOC_PPB,  'VOC',  ADS1115.GAIN_4p096)
        }


    @classmethod
    def find(cls, serial_number):
        if serial_number is None:
            return None

        for key, sensor in cls.__GAS.items():
            if str(serial_number).startswith(key):
                return sensor

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain, calib=None):
        """
        Constructor
        """
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
