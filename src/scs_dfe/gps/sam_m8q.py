"""
Created on 31 Jan 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.u-blox.com/en/product/sam-m8q-module

example sentence sets:
$GNGGA,104821.00,5049.40135,N,00007.38444,W,2,09,1.01,24.2,M,45.4,M,,0000*66
$GNGSA,A,3,31,22,09,17,19,23,06,07,,,,,1.48,1.01,1.08*1D
$GNGSA,A,3,69,,,,,,,,,,,,1.48,1.01,1.08*17
$GPGSV,4,1,15,01,04,145,10,02,21,312,,03,42,089,09,04,67,197,23*7B
$GPGSV,4,2,15,06,59,290,19,07,06,169,20,09,66,203,15,17,22,224,30*72
$GPGSV,4,3,15,19,31,241,27,22,22,097,12,23,74,092,11,25,00,344,*72
$GPGSV,4,4,15,31,08,027,10,36,25,141,,49,32,173,27*49
$GLGSV,3,1,09,68,36,057,,69,75,334,23,70,25,259,,77,16,019,*6E
$GLGSV,3,2,09,78,24,073,,79,07,121,,83,06,176,,84,53,215,*6A
$GLGSV,3,3,09,85,43,314,*50
$GNGLL,5049.40135,N,00007.38444,W,104821.00,A,D*6D
$GNTXT,01,01,01,More than 100 frame errors, UART RX was disabled*70
$GNRMC,104822.00,A,5049.40155,N,00007.38453,W,0.105,,201119,,,D*79
$GNVTG,,T,,M,0.105,N,0.194,K,D*30

$GNGGA,104822.00,5049.40155,N,00007.38453,W,2,09,1.97,23.8,M,45.4,M,,0000*67
$GNGSA,A,3,03,22,09,17,19,23,06,07,,,,,3.13,1.97,2.44*14
$GNGSA,A,3,69,,,,,,,,,,,,3.13,1.97,2.44*1F
$GPGSV,4,1,15,01,04,145,12,02,21,312,,03,42,089,10,04,67,197,23*71
$GPGSV,4,2,15,06,59,290,20,07,06,169,20,09,66,203,15,17,22,224,30*78
$GPGSV,4,3,15,19,31,241,27,22,22,097,13,23,74,092,13,25,00,344,*71
$GPGSV,4,4,15,31,08,027,07,36,25,141,,49,32,173,28*40
$GLGSV,3,1,09,68,36,057,,69,75,334,23,70,25,259,,77,16,019,*6E
$GLGSV,3,2,09,78,24,073,,79,07,121,,83,06,176,,84,53,215,*6A
$GLGSV,3,3,09,85,43,314,*50
$GNGLL,5049.40155,N,00007.38453,W,104822.00,A,D*6E
$GNRMC,104823.00,A,5049.40180,N,00007.38497,W,0.237,,201119,,,D*7A
$GNVTG,,T,,M,0.237,N,0.439,K,D*30
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

class SAMM8Q(GPS):
    """
    u-blox SAM M8Q GPS Antenna Module
    """

    SOURCE =                    "SAM8Q"

    START_MESSAGE_IDS =         GPRMC.MESSAGE_IDS

    __BAUD_RATE =               9600

    __BOOT_DELAY =              0.500           # seconds

    __EOL =                     "\r\n"

    __SERIAL_LOCK_TIMEOUT =     20.0
    __SERIAL_COMMS_TIMEOUT =     1.0

    __MAX_MESSAGE_SET_SIZE =    14              # message set size (add extra for broken message on start of scan)


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
            if reports[start].str(0) in SAMM8Q.START_MESSAGE_IDS:
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

        if report.str(0) in GPGSV.MESSAGE_IDS:
            sentences.append(GPGSV.construct(report))

        # GPGLL...
        for report in reports[start + 5:]:
            if report.str(0) in GPGLL.MESSAGE_IDS:
                break

        if report.str(0) in GPGLL.MESSAGE_IDS:
            sentences.append(GPGLL.construct(report))

        return sentences


    def line(self):
        return self._serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT)
