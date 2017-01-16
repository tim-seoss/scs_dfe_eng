"""
Created on 30 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod

from scs_core.data.json import JSONable

from scs_dfe.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class SensorCalib(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type):
        """
        Constructor
        """
        self.__serial_number = serial_number
        self.__sensor_type = sensor_type                  # TODO: remove spaces?


    # ----------------------------------------------------------------------------------------------------------------

    def sensor(self, conf_sensor_type):                   # TODO: resolve conf and calib sensor types!
        if conf_sensor_type is None:
            return None

        sensor = Sensor.find(conf_sensor_type)
        sensor.calib = self

        return sensor


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__serial_number


    @property
    def sensor_type(self):
        return self.__sensor_type

