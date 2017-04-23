"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.ads1115 import ADS1115
from scs_dfe.gas.pid_datum import PIDDatum
from scs_dfe.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class PID(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.SENSORS[cls.CODE_VOC_PPM] = PID(cls.CODE_VOC_PPM,  'VOC',  ADS1115.GAIN_4p096)
        cls.SENSORS[cls.CODE_VOC_PPB] = PID(cls.CODE_VOC_PPB,  'VOC',  ADS1115.GAIN_4p096)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_type, gas_name, adc_gain)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, index, no2_sample=None):
        wrk = afe.sample_raw_wrk(index, self.adc_gain)

        # TODO handle PID calib and baseline for cnc

        return PIDDatum(wrk)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PID:{sensor_code:%s, gas_name:%s, adc_gain:0x%04x, calib:%s, baseline:%s}" % \
                        (self.sensor_code, self.gas_name, self.adc_gain, self.calib, self.baseline)
