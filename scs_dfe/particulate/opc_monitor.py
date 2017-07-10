"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

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

    __DEFAULT_INTERVAL =        10.0        # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sample_period=None):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__sample_period = OPCMonitor.__DEFAULT_INTERVAL if sample_period is None else sample_period


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        timer = IntervalTimer(self.sample_period)

        for i in timer.range(5):
            datum = OPCDatum(i, i, i, i, [1, 2, 3], 4, 5, 6, 7)     # TODO: must carry datetime!

            with self._lock:
                datum.as_list(self._value)      # update the synchronised value with the datum's list form

            print(" run: %s" % datum)
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        return OPCDatum.construct_from_jdict(OrderedDict(self.value))   # convert the datum list form to object form


    @property
    def sample_period(self):
        return self.__sample_period


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCMonitor:{sample:%s, sample_period:%s}" % (self.sample(), self.sample_period)
