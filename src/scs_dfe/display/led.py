"""
Created on 20 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.board.io import IO


# --------------------------------------------------------------------------------------------------------------------


class LED(object):
    """
    classdocs
    """
    STATES = {'0': 0x00, 'R': 0x01, 'A': 0x03, 'G': 0x02}

    __RED_MASK = 0x01
    __GREEN_MASK = 0x02


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_colour(cls, colour):
        return colour in cls.STATES


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
        if not self.is_valid_colour(colour):
            raise ValueError(colour)

        state = LED.STATES[colour]

        self.__io.led_red = IO.HIGH if state & LED.__RED_MASK else IO.LOW
        self.__io.led_green = IO.HIGH if state & LED.__GREEN_MASK else IO.LOW


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LED:{io:%s}" % self.__io
