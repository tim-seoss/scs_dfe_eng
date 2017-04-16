"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.a4_datum import A4Datum
from scs_dfe.gas.ads1115 import ADS1115
from scs_dfe.gas.sensor import Sensor
from scs_dfe.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

class A4(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.SENSORS[cls.CODE_CO] =  A4(cls.CODE_CO,     'CO',   ADS1115.GAIN_2p048)
        cls.SENSORS[cls.CODE_H2S] = A4(cls.CODE_H2S,    'H2S',  ADS1115.GAIN_2p048)
        cls.SENSORS[cls.CODE_NO] =  A4(cls.CODE_NO,     'NO',   ADS1115.GAIN_2p048)
        cls.SENSORS[cls.CODE_NO2] = A4(cls.CODE_NO2,    'NO2',  ADS1115.GAIN_2p048)
        cls.SENSORS[cls.CODE_OX] =  A4(cls.CODE_OX,     'Ox',   ADS1115.GAIN_2p048)
        cls.SENSORS[cls.CODE_SO2] = A4(cls.CODE_SO2,    'SO2',  ADS1115.GAIN_2p048)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_code, gas_name, adc_gain):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_code, gas_name, adc_gain)

        self.__tc = TempComp.find(sensor_code)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, index):
        we_v, ae_v = afe.sample_raw_wrk_aux(index, self.adc_gain)

        return A4Datum.construct(self.calib, self.baseline, self.__tc, temp, we_v, ae_v)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4:{sensor_code:%s, gas_name:%s, adc_gain:0x%04x, calib:%s, baseline:%s, tc:%s}" % \
                        (self.sensor_code, self.gas_name, self.adc_gain, self.calib, self.baseline, self.__tc)
