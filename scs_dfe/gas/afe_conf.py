"""
Created on 17 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"type": "810-0022-01", "sn1": "NO2-A43F", "sn2": "OX-A431", "sn3": "NO-A4", "sn4": "CO-A4"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class AFEConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "afe_conf.json"

    @classmethod
    def filename(cls, host):
        return host.SCS_CONF + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        afe_type = jdict.get('type')

        sensor_types = []
        for key in sorted(jdict.keys()):
            if key[:2] == "sn":
                sensor_types.append(jdict[key])

        return AFEConf(afe_type, sensor_types)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, afe_type, sensor_types):
        """
        Constructor
        """
        self.__afe_type = afe_type
        self.__sensor_types = sensor_types          # array of string


    def __len__(self):
        return len(self.__sensor_types)


    # ----------------------------------------------------------------------------------------------------------------

    def sensors(self):
        afe_calib = AFECalib.load(Host)

        if afe_calib.afe_type != self.afe_type:
            raise ValueError("AFEConf.sensors: calibration AFE type does not match configuration AFE type: %s" % afe_calib)

        if len(self) != len(afe_calib):
            raise ValueError("AFEConf.sensors: calibration sensors do not match configuration sensors: %s" % afe_calib)

        # TODO: further tests to validate conf and calib match

        sensors = []
        for i in range(len(self.__sensor_types)):
            calib = afe_calib.sensor_calib(i)
            sensor = None if calib is None else calib.sensor(self.__sensor_types[i])

            sensors.append(sensor)

        return sensors


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['type'] = self.afe_type

        for i in range(len(self.__sensor_types)):
            jdict['sn' + str(i + 1)] = self.__sensor_types[i]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def afe_type(self):
        return self.__afe_type


    def sensor_type(self, sn):
        return self.__sensor_types[sn - 1]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AFEConf:{afe_type:%s, sensor_types:%s}" % (self.afe_type, self.__sensor_types)
