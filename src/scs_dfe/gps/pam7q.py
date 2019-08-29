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

from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.nmea.gpgll import GPGLL
from scs_core.position.nmea.gpgsa import GPGSA
from scs_core.position.nmea.gpgsv import GPGSV
from scs_core.position.nmea.gprmc import GPRMC
from scs_core.position.nmea.gpvtg import GPVTG
from scs_core.position.nmea.nmea_report import NMEAReport

from scs_dfe.interface.component.io import IO

from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class PAM7Q(object):
    """
    u-blox 7 GPS Antenna Module
    """

    SOURCE =                    "PAM7Q"

    START_MESSAGE_IDS =         GPRMC.MESSAGE_IDS

    __BAUD_RATE =               9600

    __BOOT_DELAY =              0.500           # seconds

    __EOL =                     "\r\n"

    __SERIAL_LOCK_TIMEOUT =     3.0
    __SERIAL_COMMS_TIMEOUT =    1.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, load_switch_active_high, uart):
        self.__io = IO(load_switch_active_high)
        self.__serial = HostSerial(uart, self.__BAUD_RATE, False)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__io.gps_power = True
        time.sleep(self.__BOOT_DELAY)


    def power_off(self):
        self.__io.gps_power = False


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        self.__serial.open(self.__SERIAL_LOCK_TIMEOUT, self.__SERIAL_COMMS_TIMEOUT)


    def close(self):
        self.__serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def report(self, message_class):
        for i in range(11):
            try:
                line = self.__serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT)
                r = NMEAReport.construct(line)

                if r.str(0) in message_class.MESSAGE_IDS:
                    return message_class.construct(r)

            except (IndexError, UnicodeDecodeError, ValueError):
                continue

        return None


    # noinspection PyListCreation
    def report_all(self):
        # reports...
        reports = []
        for i in range(20):
            try:
                r = NMEAReport.construct(self.__serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT))
                reports.append(r)

            except (UnicodeDecodeError, ValueError):
                continue

        # start...
        start = None
        for start in range(len(reports)):
            if reports[start].str(0) in PAM7Q.START_MESSAGE_IDS:
                break

        if start is None:
            return []

        # sentences...
        sentences = []

        # GPRMC...
        sentences.append(GPRMC.construct(reports[start]))

        # GPVTG...
        sentences.append(GPVTG.construct(reports[start + 1]))

        # GPGGA...
        sentences.append(GPGGA.construct(reports[start + 2]))

        # GPGSA...
        sentences.append(GPGSA.construct(reports[start + 3]))

        report = None         # prevents post-loop warning

        # GPGSVs...
        for report in reports[start + 4:]:
            if report.str(0) in GPGSV.MESSAGE_IDS:
                break

        sentences.append(GPGSV.construct(report))

        # GPGLL...
        for report in reports[start + 5:]:
            if report.str(0) in GPGLL.MESSAGE_IDS:
                break

        sentences.append(GPGLL.construct(report))

        return sentences


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PAM7Q:{io:%s, serial:%s}" % (self.__io, self.__serial)
