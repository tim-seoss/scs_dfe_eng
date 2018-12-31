"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.data.average import Average

from scs_core.position.gpgga import GPGGA
from scs_core.position.gps_location import GPSLocation

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

class GPSMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gps, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__gps = gps
        self.__sample_interval = conf.sample_interval
        self.__averaging = Average(conf.tally)


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__gps.power_on()
            self.__gps.open()

            self.__averaging.reset()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__gps.close()

        except KeyboardInterrupt:
            pass


    def run(self):
        try:
            timer = IntervalTimer(self.__sample_interval)

            while timer.true():
                gga = self.__gps.report(GPGGA)
                position = GPSLocation.construct(gga)

                if position is None or position.quality < 1:
                    continue

                self.__averaging.append(position)
                average = self.__averaging.compute()

                # report...
                with self._lock:
                    average.as_list(self._value)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def sample(self):
        with self._lock:
            value = self._value

        return GPSLocation.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSMonitor:{value:%s, sample_interval:%s, averaging:%s, gps:%s}" % \
               (self._value, self.__sample_interval, self.__averaging, self.__gps)
