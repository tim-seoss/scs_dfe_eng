"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false}
"""

from scs_core.particulate.opc_conf import OPCConf as AbstractOPCConf

from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_dfe.particulate.opc_n2.opc_n2 import OPCN2
from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3
from scs_dfe.particulate.opc_r1.opc_r1 import OPCR1

from scs_dfe.particulate.sps_30.sps_30 import SPS30


# --------------------------------------------------------------------------------------------------------------------

class OPCConf(AbstractOPCConf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_model(cls, model):
        return model in (OPCN2.source(), OPCN3.source(), OPCR1.source(), SPS30.source())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, restart_on_zeroes, power_saving, dev_path, name=None):
        """
        Constructor
        """
        super().__init__(model, sample_period, restart_on_zeroes, power_saving, dev_path, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def opc_monitor(self, interface, host):
        opc = self.opc(interface, host)

        return OPCMonitor(opc, self)


    def opc(self, interface, host):
        if self.model == OPCN2.source():
            return OPCN2(interface, self.opc_dev_path(host))

        elif self.model == OPCN3.source():
            return OPCN3(interface, self.opc_dev_path(host))

        elif self.model == OPCR1.source():
            return OPCR1(interface, self.opc_dev_path(host))

        # FIXME SPS30 is i2c so should probably pass dev_path (e.g. /dev/i2c-X) ?
        #elif self.model == SPS30.source():
        #    return SPS30(interface, self.opc_dev_path(host), SPS30.DEFAULT_ADDR)

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

    def __str__(self, *args, **kwargs):
        return "OPCConf(dfe):{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "bus:%s, address:%s}" %  \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.dev_path)
