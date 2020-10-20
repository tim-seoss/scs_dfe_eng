"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false,
"inf": "/home/scs/SCS/pipes/lambda-model-pmx-s1.uds", "exg": []}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_dfe.particulate.opc_n2.opc_n2 import OPCN2
from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3
from scs_dfe.particulate.opc_r1.opc_r1 import OPCR1

from scs_dfe.particulate.sps_30.sps_30 import SPS30

try:
    from scs_exegesis.particulate.exegete_catalogue import ExegeteCatalogue
except ImportError:
    from scs_core.exegesis.particulate.exegete_catalogue import ExegeteCatalogue


# --------------------------------------------------------------------------------------------------------------------

class OPCConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "opc_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')
        sample_period = jdict.get('sample-period')
        restart_on_zeroes = jdict.get('restart-on-zeroes', True)
        power_saving = jdict.get('power-saving')

        bus = jdict.get('bus')
        address = jdict.get('address')

        inference = jdict.get('inf')
        exegete_names = jdict.get('exg', [])

        return OPCConf(model, sample_period, restart_on_zeroes, power_saving, bus, address, inference, exegete_names)


    @classmethod
    def is_valid_model(cls, model):
        return model in (OPCN2.source(), OPCN3.source(), OPCR1.source(), SPS30.source())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, restart_on_zeroes, power_saving, bus, address, inference, exegete_names):
        """
        Constructor
        """
        self.__model = model                                        # string
        self.__sample_period = int(sample_period)                   # int
        self.__restart_on_zeroes = bool(restart_on_zeroes)          # bool
        self.__power_saving = bool(power_saving)                    # bool

        self.__bus = bus                                            # int
        self.__address = address                                    # int

        self.__inference = inference                                # string
        self.__exegete_names = set(exegete_names)                   # set of string


    # ----------------------------------------------------------------------------------------------------------------

    def incompatible_exegetes(self):
        incompatibles = []

        for name in self.exegete_names:
            try:
                exegete = ExegeteCatalogue.standard(name)

            except NotImplementedError:
                incompatibles.append(name)
                continue

            if exegete.opc() != self.model:
                incompatibles.append(name)

        return incompatibles


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

    def add_exegete(self, exegete):
        self.__exegete_names.add(exegete)


    def discard_exegete(self, exegete):
        self.__exegete_names.discard(exegete)                   # does nothing if exegete not present


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


    @property
    def inference(self):
        return self.__inference


    @property
    def exegete_names(self):
        return sorted(self.__exegete_names)


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

        jdict['inf'] = self.inference
        jdict['exg'] = self.exegete_names

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCConf:{model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, bus:%s, address:%s, " \
               "inference:%s, exegete_names:%s}" %  \
               (self.model, self.sample_period, self.restart_on_zeroes, self.power_saving, self.bus, self.address,
                self.inference, self.exegete_names)
