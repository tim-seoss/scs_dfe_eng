"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Firmware report:
OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS
"""

import time

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.datum import Datum

from scs_core.climate.sht_datum import SHTDatum
from scs_core.data.modbus_crc import ModbusCRC
from scs_core.particulate.opc_datum import OPCDatum

from scs_dfe.board.io import IO
from scs_dfe.climate.sht31 import SHT31
from scs_dfe.particulate.opc_n3.opc_status import OPCStatus

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class OPCN3(object):
    """
    classdocs
    """
    SOURCE =                            'N3'

    MIN_SAMPLE_PERIOD =                  5.0       # seconds
    MAX_SAMPLE_PERIOD =                 10.0       # seconds
    DEFAULT_SAMPLE_PERIOD =             10.0       # seconds

    POWER_CYCLE_TIME =                  10.0       # seconds

    # ----------------------------------------------------------------------------------------------------------------

    __BOOT_TIME =                       5.0       # seconds
    __LASER_START_TIME =                1.0       # seconds
    __FAN_START_TIME =                  5.0       # seconds
    __FAN_STOP_TIME =                   2.0       # seconds

    __CMD_POWER =                       0x03
    __CMD_LASER_ON =                    0x07
    __CMD_LASER_OFF =                   0x06
    __CMD_FAN_ON =                      0x03
    __CMD_FAN_OFF =                     0x02

    __CMD_READ_HISTOGRAM =              0x30

    __CMD_GET_FIRMWARE =                0x3f
    __CMD_GET_VERSION =                 0x12
    __CMD_GET_SERIAL =                  0x10
    __CMD_GET_STATUS =                  0x13

    __CMD_RESET =                       0x06

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1

    __DELAY_CMD =                       0.010
    __DELAY_TRANSFER =                  0.010

    __LOCK_TIMEOUT =                    6.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, cls.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, spi_bus, spi_device):
        """
        Constructor
        """
        self.__io = IO()
        self.__spi = SPI(spi_bus, spi_device, OPCN3.__SPI_MODE, OPCN3.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        initial_power_state = self.__io.opc_power

        self.__io.opc_power = IO.LOW

        if initial_power_state == IO.HIGH:      # initial_power_state is None if there is no power control facility
            time.sleep(self.__BOOT_TIME)


    def power_off(self):
        self.__io.opc_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------

    def operations_on(self):
        try:
            self.obtain_lock()

            # laser...
            for _ in range(2):
                self.__cmd_power(self.__CMD_LASER_ON)

            # fan...
            for _ in range(2):
                self.__cmd_power(self.__CMD_FAN_ON)

        finally:
            time.sleep(self.__FAN_START_TIME)
            self.release_lock()


    def operations_off(self):
        try:
            self.obtain_lock()

            # laser...
            for _ in range(2):
                self.__cmd_power(self.__CMD_LASER_OFF)

            # fan...
            for _ in range(2):
                self.__cmd_power(self.__CMD_FAN_OFF)

        finally:
            time.sleep(self.__FAN_STOP_TIME)
            self.release_lock()


    def reset(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__cmd(self.__CMD_RESET)

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__cmd(self.__CMD_READ_HISTOGRAM)
            chars = self.__read_bytes(86)

            # checksum...
            chk = Datum.decode_unsigned_int(chars[84:86])
            crc = ModbusCRC.compute(chars[:84])

            if chk != crc:
                raise ValueError("bad checksum")

            # bins...
            bins = [Datum.decode_unsigned_int(chars[i:i + 2]) for i in range(0, 48, 2)]

            # bin MToFs...
            bin_1_mtof = chars[48]
            bin_3_mtof = chars[49]
            bin_5_mtof = chars[50]
            bin_7_mtof = chars[51]

            # period...
            raw_period = Datum.decode_unsigned_int(chars[52:54])
            period = round(float(raw_period) / 100.0, 3)

            # temperature & humidity
            raw_temp = Datum.decode_unsigned_int(chars[56:58])
            raw_humid = Datum.decode_unsigned_int(chars[58:60])

            sht = SHTDatum(SHT31.humid(raw_humid), SHT31.temp(raw_temp))

            # PMx...
            try:
                pm1 = Datum.decode_float(chars[60:64])
            except TypeError:
                pm1 = None

            try:
                pm2p5 = Datum.decode_float(chars[64:68])
            except TypeError:
                pm2p5 = None

            try:
                pm10 = Datum.decode_float(chars[68:72])
            except TypeError:
                pm10 = None

            # unused fields...
            # flo = Datum.decode_unsigned_int(chars[54:56])
            # rcg = Datum.decode_unsigned_int(chars[72:74])
            # rcl = Datum.decode_unsigned_int(chars[74:76])
            # rcr = Datum.decode_unsigned_int(chars[76:78])
            # rco = Datum.decode_unsigned_int(chars[78:80])
            # frc = Datum.decode_unsigned_int(chars[80:82])
            # lst = Datum.decode_unsigned_int(chars[82:84])

            now = LocalizedDatetime.now()

            return OPCDatum(self.SOURCE, now, pm1, pm2p5, pm10, period, bins,
                            bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof, sht)

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def firmware(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__cmd(self.__CMD_GET_FIRMWARE)
            chars = self.__read_bytes(60)

            # report...
            report = ''.join(chr(byte) for byte in chars)

            return report.strip('\0\xff')       # \0 - Raspberry Pi, \xff - BeagleBone

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    def version(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__cmd(self.__CMD_GET_VERSION)

            # report...
            major = int(self.__read_byte())
            minor = int(self.__read_byte())

            return major, minor

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    def serial_no(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__cmd(self.__CMD_GET_SERIAL)
            chars = self.__read_bytes(60)

            # report...
            report = ''.join(chr(byte) for byte in chars)
            pieces = report.split(' ')

            if len(pieces) < 2:
                return None, None

            return pieces[0], pieces[1]             # type, number

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    def status(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__cmd(self.__CMD_GET_STATUS)
            chars = self.__read_bytes(6)

            # report...
            status = OPCStatus.construct(chars)

            return status

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd_power(self, cmd):
        try:
            self.__spi.open()

            self.__spi.xfer([self.__CMD_POWER, cmd])
            time.sleep(self.__DELAY_CMD)

        finally:
            self.__spi.close()


    def __cmd(self, cmd):
        self.__spi.xfer([cmd])
        time.sleep(self.__DELAY_CMD)

        self.__spi.xfer([cmd])


    def __read_bytes(self, count):
        return [self.__read_byte() for _ in range(count)]


    def __read_byte(self):
        time.sleep(self.__DELAY_TRANSFER)
        chars = self.__spi.read_bytes(1)

        return chars[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCN3:{io:%s, spi:%s}" % (self.__io, self.__spi)
