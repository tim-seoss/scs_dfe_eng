"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.particulate.opc_datum import OPCDatum

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_dfe.particulate.opc import OPC

from scs_host.lock.lock_timeout import LockTimeout


# TODO: should be able to start and stop the OPC on very long sampling intervals

# --------------------------------------------------------------------------------------------------------------------

class OPCMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opc: OPC, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__opc = opc
        self.__conf = conf
        self.__first_reading = True


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__opc.power_on()
            self.__opc.operations_on()

            self.__first_reading = True

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            self.__opc.operations_off()
            self.__opc.power_off()

            super().stop()

        except KeyboardInterrupt:
            pass

        except LockTimeout:             # because __power_cycle() may be running!
            pass


    def run(self):
        try:
            timer = IntervalTimer(self.__conf.sample_period)

            while timer.true():
                power_cycle = False

                # sample...
                try:
                    datum = self.__opc.sample()

                    if datum.is_zero() and not self.__first_reading:
                        raise ValueError("zero reading")

                except ValueError as ex:
                    datum = OPCDatum.null_datum()
                    power_cycle = True

                    print("OPCMonitor: %s" % ex, file=sys.stderr)
                    sys.stderr.flush()

                # discard first...
                if self.__first_reading:
                    datum = OPCDatum.null_datum()
                    self.__first_reading = False

                # report...
                with self._lock:
                    datum.as_list(self._value)

                # monitor...
                if power_cycle:
                    self.__power_cycle()

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess special operations...

    def __power_cycle(self):
        print("OPCMonitor: power cycle", file=sys.stderr)
        sys.stderr.flush()

        try:
            # off...
            self.__opc.operations_off()
            self.__opc.power_off()

            time.sleep(self.__opc.power_cycle_time())

            # on...
            self.__opc.power_on()
            self.__opc.operations_on()

            self.__first_reading = True

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def firmware(self):
        return self.__opc.firmware()


    def sample(self):
        with self._lock:
            value = self._value

        return None if value is None else OPCDatum.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCMonitor:{value:%s, opc:%s, conf:%s, first_reading:%s}" % \
               (self._value, self.__opc, self.__conf, self.__first_reading)
