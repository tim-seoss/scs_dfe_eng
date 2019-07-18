"""
Created on 10 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Integrated Electrochem Interface (IEI)

Warning: If an Ox sensor is present, the NO2 sensor must have a lower sensor number (SN) than the Ox sensor,
otherwise the NO2 cross-sensitivity concentration will not be found.
"""

import time

from scs_core.gas.iei_datum import IEIDatum

from scs_dfe.gas.dsi_t1_f1 import DSIt1f1
from scs_dfe.gas.electrochem_interface import ElectrochemInterface


# TODO: IEI requires multiple DSIt1f1 instances to support multiple sensors

# --------------------------------------------------------------------------------------------------------------------

class IEI(ElectrochemInterface):
    """
    South Coast Science integrated electrochem interface using DSIt1f1
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __no2_sample(cls, samples):
        for sample in samples:
            if sample[0] == 'NO2':
                return sample[1]

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensors):
        """
        Constructor
        """
        self.__sensors = sensors
        self.__adc = DSIt1f1(DSIt1f1.DEFAULT_ADDR)


    # ----------------------------------------------------------------------------------------------------------------
    # business methods...

    def sample(self, sht_datum):
        # gases...
        samples = []
        no2_sample = None

        for sensor_index in range(len(self.__sensors)):
            sensor = self.__sensors[sensor_index]

            if sensor is None:
                continue

            # cross-sensitivity sample...
            if sensor.has_no2_cross_sensitivity():
                no2_sample = IEI.__no2_sample(samples)

            # sample...
            sample = sensor.sample(self, sht_datum.temp, sensor_index, no2_sample)

            samples.append((sensor.gas_name, sample))

        return IEIDatum(*samples)


    def sample_station(self, sn, sht_datum):
        # gas...
        index = sn - 1

        sensor = self.__sensors[index]

        if sensor is None:
            return IEIDatum()

        # cross-sensitivity sample...
        if sensor.has_no2_cross_sensitivity():
            no2_index, no2_sensor = self.__no2_sensor()
            no2_sample = no2_sensor.sample(self, sht_datum.temp, no2_index)
        else:
            no2_sample = None

        # sample...
        sample = sensor.sample(self, sht_datum.temp, index, no2_sample)

        return IEIDatum((sensor.gas_name, sample))


    def null_datum(self):
        samples = []

        for sensor_index in range(len(self.__sensors)):
            sensor = self.__sensors[sensor_index]

            if sensor is None:
                continue

            samples.append((sensor.gas_name, sensor.null_datum()))

        return IEIDatum(*samples)


    # ----------------------------------------------------------------------------------------------------------------
    # electrochem callbacks...

    def sample_raw_wrk_aux(self, sensor_index, gain_index):
        self.__adc.start_conversion()
        time.sleep(self.__adc.CONVERSION_TIME)

        return self.__adc.read_conversion_voltage()


    # noinspection PyUnusedLocal
    def sample_raw_wrk(self, sensor_index, gain_index):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __no2_sensor(self):
        for index in range(len(self.__sensors)):
            if self.__sensors[index].gas_name == 'NO2':
                return index, self.__sensors[index]

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        sensors = '[' + ', '.join(str(sensor) for sensor in self.__sensors) + ']'

        return "IEI:{sensors:%s, adc:%s}" %  (sensors, self.__adc)
