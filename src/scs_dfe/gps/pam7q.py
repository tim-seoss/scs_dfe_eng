"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.u-blox.com/en/product/pam-7q-module

example sentences:
$GPRMC,103228.00,A,5049.37823,N,00007.37872,W,0.104,,301216,,,D*64
$GPVTG,,T,,M,0.104,N,0.193,K,D*28
$GPGGA,103228.00,5049.37823,N,00007.37872,W,2,07,1.85,34.0,M,45.4,M,,0000*75
$GPGSA,A,3,23,17,03,09,01,22,19,,,,,,2.96,1.85,2.30*06
$GPGSV,4,1,13,01,15,142,36,02,12,312,21,03,46,084,33,06,46,301,*70
$GPGSV,4,2,13,09,49,206,46,12,01,319,,17,32,235,43,19,38,254,35*74
$GPGSV,4,3,13,22,31,090,29,23,74,115,35,25,03,355,,31,14,034,20*78
$GPGSV,4,4,13,33,30,200,42*4C
$GPGLL,5049.37823,N,00007.37872,W,103228.00,A,D*7F

$GPRMC,152926.00,A,5049.36953,N,00007.38514,W,0.018,,301216,,,D*6C
$GPVTG,,T,,M,0.018,N,0.033,K,D*2F
$GPGGA,152926.00,5049.36953,N,00007.38514,W,2,07,1.37,23.2,M,45.4,M,,0000*7C
$GPGSA,A,3,30,13,28,20,05,15,07,,,,,,2.71,1.37,2.34*09
$GPGSV,3,1,12,05,61,203,40,07,26,057,31,08,05,050,,09,00,101,*7D
$GPGSV,3,2,12,13,58,287,22,15,26,285,35,20,41,297,29,21,13,321,*71
$GPGSV,3,3,12,27,04,013,13,28,39,126,37,30,60,068,26,33,30,200,44*74
$GPGLL,5049.36953,N,00007.38514,W,152926.00,A,D*7B
"""

import time

from scs_core.position.gpgga import GPGGA
from scs_core.position.gpgll import GPGLL
from scs_core.position.gpgsa import GPGSA
from scs_core.position.gpgsv import GPGSV
from scs_core.position.gprmc import GPRMC
from scs_core.position.gpvtg import GPVTG
from scs_core.position.nmea_sentence import NMEASentence

from scs_dfe.board.io import IO

from scs_host.sys.host_serial import HostSerial


# TODO: add specialised object for message collection

# --------------------------------------------------------------------------------------------------------------------

class PAM7Q(object):
    """
    u-blox 7 GPS Antenna Module
    """

    START_MESSAGE_ID =          GPRMC.MESSAGE_ID

    __BAUD_RATE =               9600

    __BOOT_DELAY =              0.500           # seconds

    __SERIAL_LOCK_TIMEOUT =     3.0
    __SERIAL_COMMS_TIMEOUT =    1.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uart):
        self.__io = IO()
        self.__serial = HostSerial(uart, self.__BAUD_RATE, False)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__io.gps_power = IO.LOW
        time.sleep(self.__BOOT_DELAY)


    def power_off(self):
        self.__io.gps_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        self.__serial.open(self.__SERIAL_LOCK_TIMEOUT, self.__SERIAL_COMMS_TIMEOUT)


    def close(self):
        self.__serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def report(self, message_class):
        for i in range(11):
            try:
                line = self.__serial.read_line("\r\n", self.__SERIAL_COMMS_TIMEOUT)
                s = NMEASentence.construct(line)

                if s.str(0) == message_class.MESSAGE_ID:
                    return message_class.construct(s)

            except (UnicodeDecodeError, ValueError):
                continue

        return None


    # noinspection PyListCreation
    def report_all(self):
        # text...
        sentences = []
        for i in range(20):
            try:
                s = NMEASentence.construct(self.__serial.read_line("\r\n", self.__SERIAL_COMMS_TIMEOUT))
                sentences.append(s)

            except (UnicodeDecodeError, ValueError):
                continue

        # start...
        start = None
        for start in range(len(sentences)):
            if sentences[start].str(0) == PAM7Q.START_MESSAGE_ID:
                break

        if start is None:
            return []

        # messages...
        messages = []

        # GPRMC...
        messages.append(GPRMC.construct(sentences[start]))

        # GPVTG...
        messages.append(GPVTG.construct(sentences[start + 1]))

        # GPGGA...
        messages.append(GPGGA.construct(sentences[start + 2]))

        # GPGSA...
        messages.append(GPGSA.construct(sentences[start + 3]))

        sentence = None         # prevents post-loop warning

        # GPGSVs...
        for sentence in sentences[start + 4:]:
            if sentence.str(0) != GPGSV.MESSAGE_ID:
                break

            messages.append(GPGSV.construct(sentence))

        # GPGLL...
        messages.append(GPGLL.construct(sentence))

        return messages


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PAM7Q:{io:%s, serial:%s}" % (self.__io, self.__serial)
