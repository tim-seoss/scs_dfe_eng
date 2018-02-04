"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.position.gpgga import GPGGA
from scs_core.position.gps_location import GPSLocation

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

class GPSMonitor(SynchronisedProcess):
    """
    classdocs
    """
    __MONITOR_INTERVAL =        10.0             # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gps):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__gps = gps


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        try:
            timer = IntervalTimer(self.__MONITOR_INTERVAL)

            while timer.true():
                gga = self.__gps.report(GPGGA)
                position = GPSLocation.construct(gga)

                if position is None:
                    print("GPSMonitor.run: got None", sys.stderr)
                    continue

                # report...
                with self._lock:
                    position.as_list(self._value)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            self.__gps.power_on()
            self.__gps.open()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__gps.close()

        except KeyboardInterrupt:
            pass


    def sample(self):
        with self._lock:
            value = self._value

        return GPSLocation.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSMonitor:{value:%s, gps:%s}" % (self._value, self.__gps)
