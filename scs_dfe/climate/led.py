"""
Created on 20 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.board.io import IO

# TODO: move LED away from climate!

# --------------------------------------------------------------------------------------------------------------------


class LED(object):
    """
    classdocs
    """
    STATES = {'0': 0x00, 'R': 0x01, 'G': 0x02, 'O': 0x03}

    __RED_MASK = 0x01
    __GREEN_MASK = 0x02


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__io = IO()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def colour(self):
        state = 0x00

        if self.__io.led_red == IO.HIGH:
            state |= LED.__RED_MASK

        if self.__io.led_green == IO.HIGH:
            state |= LED.__GREEN_MASK

        for colour, value in LED.STATES.items():
            if value == state:
                return colour

        raise ValueError(state)


    @colour.setter
    def colour(self, colour):
        if colour not in LED.STATES:
            raise ValueError(colour)

        state = LED.STATES[colour]

        self.__io.led_red = IO.HIGH if state & LED.__RED_MASK else IO.LOW
        self.__io.led_green = IO.HIGH if state & LED.__GREEN_MASK else IO.LOW


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LED:{io:%s}" % self.__io
