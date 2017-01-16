"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.pid_datum import PIDDatum
from scs_dfe.gas.sensor import Sensor


# TODO: we need to know if this is ppb or ppm

# --------------------------------------------------------------------------------------------------------------------

class PID(Sensor):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_type, gas_name, adc_gain):
        """
        Constructor
        """
        Sensor.__init__(self, sensor_type, gas_name, adc_gain)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self, afe, temp, index):
        wrk = afe.sample_raw_wrk(index, self.adc_gain)

        return PIDDatum(wrk)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PID:{sensor_type:%s, gas_name:%s, adc_gain:0x%04x, calib:%s}" % \
                        (self.sensor_type, self.gas_name, self.adc_gain, self.calib)
