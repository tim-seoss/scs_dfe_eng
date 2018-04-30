"""
Created on 30 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from ctypes import c_char
from multiprocessing import Manager, Value

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_dfe.display.led import LED


# --------------------------------------------------------------------------------------------------------------------

class LEDController(SynchronisedProcess):
    """
    classdocs
    """

    __STATE0_PERIOD =   0.8             # seconds
    __STATE1_PERIOD =   0.2             # seconds

    __INITIAL_STATE =   "0"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__state0 = Value(c_char, self.__INITIAL_STATE.encode())
        self.__state1 = Value(c_char, self.__INITIAL_STATE.encode())

        self.__led = LED()


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def run(self):
        try:
            timer = IntervalTimer(self.__STATE0_PERIOD + self.__STATE1_PERIOD)

            while timer.true():
                # values...
                with self._lock:
                    state0 = self.__state0.value.decode()
                    state1 = self.__state1.value.decode()

                # state0...
                if state0 != self.__led.colour:
                    self.__led.colour = state0

                time.sleep(self.__STATE0_PERIOD)

                # state1...
                if state1 != self.__led.colour:
                    self.__led.colour = state1

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # setter for client process...

    def set_states(self, state0, state1):
        with self._lock:
            self.__state0.value = state0.encode()
            self.__state1.value = state1.encode()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LEDController:{state0:%s, state1:%s, led:%s}" % (self.__state0, self.__state1, self.__led)
