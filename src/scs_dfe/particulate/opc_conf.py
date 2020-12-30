"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false}
"""

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable

from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_dfe.particulate.opc_n2.opc_n2 import OPCN2
from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3
from scs_dfe.particulate.opc_r1.opc_r1 import OPCR1

from scs_dfe.particulate.sps_30.sps_30 import SPS30


# --------------------------------------------------------------------------------------------------------------------

class OPCConf(MultiPersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "opc_conf.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.conf_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None):
        if not jdict:
            return None

        model = jdict.get('model')
        sample_period = jdict.get('sample-period')
        restart_on_zeroes = jdict.get('restart-on-zeroes', True)
        power_saving = jdict.get('power-saving')

        bus = jdict.get('bus')
        address = jdict.get('address')

        return cls(model, sample_period, restart_on_zeroes, power_saving, bus, address, name=name)


    @classmethod
    def is_valid_model(cls, model):
        return model in (OPCN2.source(), OPCN3.source(), OPCR1.source(), SPS30.source())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, restart_on_zeroes, power_saving, bus, address, name=None):
        """
        Constructor
        """
        super().__init__(name)

        self.__model = model                                        # string
        self.__sample_period = int(sample_period)                   # int
        self.__restart_on_zeroes = bool(restart_on_zeroes)          # bool
        self.__power_saving = bool(power_saving)                    # bool

        self.__bus = bus                                            # int
        self.__address = address                                    # int


    # ----------------------------------------------------------------------------------------------------------------

    def opc_monitor(self, interface, host):
        opc = self.opc(interface, host)

        return OPCMonitor(opc, self)


    def opc(self, interface, host):
        if self.model == OPCN2.source():
            return OPCN2(interface, self.opc_bus(host), self.opc_address(host))

        elif self.model == OPCN3.source():
            return OPCN3(interface, self.opc_bus(host), self.opc_address(host))

        elif self.model == OPCR1.source():
            return OPCR1(interface, self.opc_bus(host), self.opc_address(host))

        elif self.model == SPS30.source():
            return SPS30(interface, self.opc_bus(host), SPS30.DEFAULT_ADDR)

        raise ValueError('unknown model: %s' % self.model)


    def uses_spi(self):
        if self.model == OPCN2.source():
            return OPCN2.uses_spi()

        elif self.model == OPCN3.source():
            return OPCN3.uses_spi()

        elif self.model == OPCR1.source():
            return OPCR1.uses_spi()

        elif self.model == SPS30.source():
            return SPS30.uses_spi()

        raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def opc_bus(self, host):
        try:
            return int(self.__bus)

        except TypeError:
            return host.opc_spi_bus()


    def opc_address(self, host):
        try:
            return int(self.__address)

        except TypeError:
            return host.opc_spi_device()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def sample_period(self):
        return self.__sample_period


    @property
    def power_saving(self):
        return self.__power_saving


    @property
    def restart_on_zeroes(self):
        return self.__restart_on_zeroes


    @property
    def bus(self):
        return self.__bus


    @property
    def address(self):
        return self.__address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['sample-period'] = self.sample_period
        jdict['restart-on-zeroes'] = self.restart_on_zeroes
        jdict['power-saving'] = self.power_saving

        if self.__bus is not None:
            jdict['bus'] = self.bus

        if self.__address is not None:
            jdict['address'] = self.address

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCConf:{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "bus:%s, address:%s}" %  \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.bus, self.address)
