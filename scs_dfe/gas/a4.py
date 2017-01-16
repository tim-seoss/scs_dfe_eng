"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.a4_datum import A4Datum
from scs_dfe.gas.sensor import Sensor
from scs_dfe.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

class A4(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_type, gas_name, adc_gain)

        self.__tc = TempComp.find(sensor_type)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, index):
        we_v, ae_v = afe.sample_raw_wrk_aux(index, self.adc_gain)

        return A4Datum.construct(self.calib, self.__tc, temp, we_v, ae_v)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4:{sensor_type:%s, gas_name:%s, adc_gain:0x%04x, calib:%s, tc:%s}" % \
                        (self.sensor_type, self.gas_name, self.adc_gain, self.calib, self.__tc)
