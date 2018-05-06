"""
Created on 30 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_dfe.display.led import LED
from scs_dfe.display.led_state import LEDState


# --------------------------------------------------------------------------------------------------------------------

class LEDController(SynchronisedProcess):
    """
    classdocs
    """

    __STATE0_PERIOD =   0.8             # seconds
    __STATE1_PERIOD =   0.2             # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__led = LED()


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def run(self):
        try:
            timer = IntervalTimer(self.__STATE0_PERIOD + self.__STATE1_PERIOD)

            while timer.true():
                # values...
                with self._lock:
                    value = self._value

                state = LEDState.construct_from_jdict(OrderedDict(value))

                if state is None or not state.is_valid():
                    continue

                # state 0...
                if state.colour0 != self.__led.colour:
                    self.__led.colour = state.colour0

                time.sleep(self.__STATE0_PERIOD)

                # state 1...
                if state.colour1 != self.__led.colour:
                    self.__led.colour = state.colour1

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # setter for client process...

    def set_state(self, state):
        with self._lock:
            state.as_list(self._value)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LEDController:{value:%s, led:%s}" % (self._value, self.__led)
