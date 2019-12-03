"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.u-blox.com/en/product/pam-7q-module

example sentence sets:
$GPGGA,113111.00,5049.38388,N,00007.37172,W,1,04,2.48,35.9,M,45.4,M,,*7B
$GPGSA,A,3,07,19,06,23,,,,,,,,,4.22,2.48,3.42*05
$GPGSV,2,1,07,06,66,247,39,07,24,164,47,09,,,34,17,04,214,39*40
$GPGSV,2,2,07,19,15,227,50,23,57,066,32,24,,,31*76
$GPGLL,5049.38388,N,00007.37172,W,113111.00,A,A*7E
$GPRMC,113112.00,A,5049.38381,N,00007.37173,W,0.017,,201119,,,A*60
$GPVTG,,T,,M,0.017,N,0.032,K,A*24

$GPGGA,113112.00,5049.38381,N,00007.37173,W,1,04,2.48,36.5,M,45.4,M,,*7F
$GPGSA,A,3,07,19,06,23,,,,,,,,,4.22,2.48,3.41*06
$GPGSV,2,1,08,06,66,247,39,07,24,164,47,09,,,33,17,04,214,39*48
$GPGSV,2,2,08,19,15,227,50,23,57,066,33,24,,,30,26,,,29*76
$GPGLL,5049.38381,N,00007.37173,W,113112.00,A,A*75
$GPRMC,113113.00,A,5049.38380,N,00007.37174,W,0.060,,201119,,,A*67
$GPVTG,,T,,M,0.060,N,0.111,K,A*24
"""

# import sys

from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.nmea.gpgll import GPGLL
from scs_core.position.nmea.gpgsa import GPGSA
from scs_core.position.nmea.gpgsv import GPGSV
from scs_core.position.nmea.gprmc import GPRMC
from scs_core.position.nmea.gpvtg import GPVTG
from scs_core.position.nmea.nmea_report import NMEAReport

from scs_dfe.gps.gps import GPS


# --------------------------------------------------------------------------------------------------------------------

class PAM7Q(GPS):
    """
    u-blox 7 GPS Antenna Module
    """

    SOURCE =                    "PAM7Q"

    START_MESSAGE_IDS =         GPRMC.MESSAGE_IDS

    __BAUD_RATE =               9600

    __BOOT_DELAY =              0.500           # seconds

    __EOL =                     "\r\n"

    __SERIAL_LOCK_TIMEOUT =     20.0
    __SERIAL_COMMS_TIMEOUT =     1.0

    __MAX_MESSAGE_SET_SIZE =    12              # max message set size (add extra for broken message on start of scan)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def baud_rate(cls):
        return cls.__BAUD_RATE


    @classmethod
    def boot_time(cls):
        return cls.__BOOT_DELAY


    @classmethod
    def serial_lock_timeout(cls):
        return cls.__SERIAL_LOCK_TIMEOUT


    @classmethod
    def serial_comms_timeout(cls):
        return cls.__SERIAL_COMMS_TIMEOUT


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, uart):
        super().__init__(interface, uart)


    # ----------------------------------------------------------------------------------------------------------------

    def report(self, message_class):
        for i in range(self.__MAX_MESSAGE_SET_SIZE + 2):
            try:
                line = self._serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT)
                # print(line, file=sys.stderr)
                # sys.stderr.flush()

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
        for i in range((self.__MAX_MESSAGE_SET_SIZE * 2) + 2):
            try:
                line = self._serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT)
                # print(line, file=sys.stderr)
                # sys.stderr.flush()

                r = NMEAReport.construct(line)
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
