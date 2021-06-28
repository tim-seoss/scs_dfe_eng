"""
Created on 10 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Integrated Electrochem Interface (ISI)

Warning: If an Ox sensor is present, the NO2 sensor must have a lower sensor number (SN) than the Ox sensor,
otherwise the NO2 cross-sensitivity concentration will not be found.
"""

import time

from scs_core.data.str import Str
from scs_core.gas.isi.isi_datum import ISIDatum

from scs_dfe.gas.isi.elc_dsi_t1_f16k import ElcDSIt1f16K
from scs_dfe.gas.sensor_interface import SensorInterface


# TODO: rename as Gas Sensor Interface
# TODO: use config to specify which type of DSI is being used
# TODO: ISI requires multiple DSIt1 instances to support multiple sensors

# --------------------------------------------------------------------------------------------------------------------

class ISI(SensorInterface):
    """
    South Coast Science integrated sensor interface, using DSI gas sensors
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
        self.__sensors = sensors                                        # array of Sensor
        self.__adc = ElcDSIt1f16K(ElcDSIt1f16K.DEFAULT_ADDR)            # DSI


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
                no2_sample = ISI.__no2_sample(samples)

            # sample...
            sample = sensor.sample(self, sht_datum.temp, sensor_index, no2_sample)

            samples.append((sensor.gas_name, sample))

        return ISIDatum(*samples)


    def sample_station(self, sn, sht_datum):
        # gas...
        index = sn - 1

        sensor = self.__sensors[index]

        if sensor is None:
            return ISIDatum()

        # cross-sensitivity sample...
        if sensor.has_no2_cross_sensitivity():
            no2_index, no2_sensor = self.__no2_sensor()
            no2_sample = no2_sensor.sample(self, sht_datum.temp, no2_index)
        else:
            no2_sample = None

        # sample...
        sample = sensor.sample(self, sht_datum.temp, index, no2_sample)

        return ISIDatum((sensor.gas_name, sample))


    def null_datum(self):
        samples = []

        for sensor_index in range(len(self.__sensors)):
            sensor = self.__sensors[sensor_index]

            if sensor is None:
                continue

            samples.append((sensor.gas_name, sensor.null_datum()))

        return ISIDatum(*samples)


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
        sensors = Str.collection(self.__sensors)

        return "ISI:{sensors:%s, adc:%s}" %  (sensors, self.__adc)
