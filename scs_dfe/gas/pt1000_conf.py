"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

the I2C address of the Pt1000 ADC

example document:
{"addr": "0x68"}        - Alpha Pi Eng, Alpha BB Eng without RTC
{"addr": "0x69"}        - Alpha BB Eng with RTC
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.gas.mcp342x import MCP342X


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Conf(PersistentJSONable):
    """
    classdocs
    """

    DEFAULT_ADDR = 0x68             # the address used when there is no conf file


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "pt1000_conf.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return Pt1000Conf(cls.DEFAULT_ADDR)

        addr_str = jdict.get('addr')

        int_addr = None if addr_str is None else int(addr_str, 0)

        return Pt1000Conf(int_addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr          # int       I2C address of Pt1000 ADC


    # ----------------------------------------------------------------------------------------------------------------

    def adc(self, gain, rate):
        if self.addr is None:
            return None

        return MCP342X(self.addr, gain, rate)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['addr'] = Pt1000Conf.__addr_str(self.__addr)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Pt1000Conf:{addr:%s}" % Pt1000Conf.__addr_str(self.addr)
