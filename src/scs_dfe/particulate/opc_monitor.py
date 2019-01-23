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

from scs_host.lock.lock_timeout import LockTimeout


# TODO: should be able to start and stop the OPC on very long sampling intervals

# --------------------------------------------------------------------------------------------------------------------

class OPCMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opc, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__opc = opc
        self.__conf = conf


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__opc.power_on()
            self.__opc.operations_on()

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
            try:
                self.__opc.sample()
            except ValueError:
                pass

            # first_reading = True
            timer = IntervalTimer(self.__conf.sample_period)

            while timer.true():
                try:
                    datum = self.__opc.sample()

                except ValueError:
                    print("OPCMonitor: CRC check failed", file=sys.stderr)
                    sys.stderr.flush()

                    self.__power_cycle()
                    continue

                # discard first...
                # if first_reading:
                #     datum = OPCDatum.null_datum()

                # report...
                with self._lock:
                    datum.as_list(self._value)

                # if first_reading:
                #     first_reading = False
                #     continue

                # monitor...
                if datum.is_zero():
                    print("OPCMonitor: zero reading", file=sys.stderr)
                    sys.stderr.flush()

                    self.__power_cycle()
                    # first_reading = True

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess special operations...

    def __sample(self):
        try:
            return self.__opc.sample()

        except ValueError:
            print("OPCMonitor: CRC check failed", file=sys.stderr)
            sys.stderr.flush()

            return OPCDatum.null_datum()


    def __power_cycle(self):
        print("OPCMonitor: POWER CYCLE", file=sys.stderr)
        sys.stderr.flush()

        try:
            # off...
            self.__opc.operations_off()
            self.__opc.power_off()

            time.sleep(self.__opc.POWER_CYCLE_TIME)

            # on...
            self.__opc.power_on()
            self.__opc.operations_on()

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
        return "OPCMonitor:{value:%s, opc:%s, conf:%s}" % (self._value, self.__opc, self.__conf)
