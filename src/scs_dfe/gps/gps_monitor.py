"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.data.average import Average

from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.gps_datum import GPSDatum

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
        # default report...
        datum = GPSDatum.construct_null()

        with self._lock:
            datum.as_list(self._value)

        # sample...
        try:
            timer = IntervalTimer(self.__sample_interval)

            while timer.true():
                # position...
                gga = self.__gps.report(GPGGA)
                datum = GPSDatum.construct_from_gga(gga)

                if datum is None:
                    continue

                # average...
                if datum.quality > 0:
                    self.__averaging.append(datum)          # only append valid positional fixes

                average = self.__averaging.compute()

                if average is None:
                    average = datum                         # provide current datum when there is no average

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

        return GPSDatum.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSMonitor:{value:%s, sample_interval:%s, averaging:%s, gps:%s}" % \
               (self._value, self.__sample_interval, self.__averaging, self.__gps)
