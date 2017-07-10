"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.particulate.opc_datum import OPCDatum

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# TODO: separate sample period from reporting interval
# TODO: should be able to start and stop the OPC on very long intervals

# --------------------------------------------------------------------------------------------------------------------

class OPCMonitor(SynchronisedProcess):
    """
    classdocs
    """

    DEFAULT_SAMPLING_PERIOD =        10.0        # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opc, sample_period):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__opc = opc
        self.__sample_period = sample_period


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        self.on()

        try:
            timer = IntervalTimer(self.__sample_period)

            while timer.true():
                datum = self.__opc.sample()

                with self._lock:
                    datum.as_list(self._value)

        except KeyboardInterrupt:
            pass

        finally:
            self.off()


    # ----------------------------------------------------------------------------------------------------------------

    def reset(self):
        pass


    def sample(self):
        return OPCDatum.construct_from_jdict(OrderedDict(self.value))


    # ----------------------------------------------------------------------------------------------------------------

    def on(self):
        try:
            self.__opc.power_on()
            self.__opc.operations_on()
            time.sleep(5)

        except KeyboardInterrupt:
            pass


    def off(self):
        try:
            self.__opc.operations_off()
            self.__opc.power_off()
            time.sleep(1)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCMonitor:{sample:%s, opc:%s, sample_period:%s}" % \
               (self.sample(), self.__opc, self.__sample_period)
