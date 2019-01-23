"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Firmware report:
OPC-N2 FirmwareVer=OPC-018.1..............................BD
"""

import time

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.datum import Decode

from scs_core.particulate.opc_datum import OPCDatum

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class OPCN2(object):
    """
    classdocs
    """
    SOURCE =                            'N2'

    MIN_SAMPLE_PERIOD =                  5.0        # seconds
    MAX_SAMPLE_PERIOD =                 10.0        # seconds
    DEFAULT_SAMPLE_PERIOD =             10.0        # seconds

    POWER_CYCLE_TIME =                  10.0        # seconds

    # ----------------------------------------------------------------------------------------------------------------

    __BOOT_TIME =                        5.0        # seconds
    __START_TIME =                       5.0        # seconds
    __STOP_TIME =                        2.0        # seconds

    __FAN_UP_TIME =                     10
    __FAN_DOWN_TIME =                   2

    __CMD_POWER =                       0x03
    __CMD_POWER_ON =                    0x00        # 0x03, 0x00
    __CMD_POWER_OFF =                   0x01        # 0x03, 0x01

    __CMD_CHECK_STATUS =                0xcf
    __CMD_READ_HISTOGRAM =              0x30
    __CMD_GET_FIRMWARE =                0x3f

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
        self.__spi = SPI(spi_bus, spi_device, self.__SPI_MODE, self.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        initial_power_state = self.__io.opc_power

        self.__io.opc_power = IO.LOW

        if initial_power_state == IO.HIGH:      # initial_power is None if there is no power control facility
            time.sleep(self.__BOOT_TIME)


    def power_off(self):
        self.__io.opc_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------

    def operations_on(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # start...
            self.__spi.xfer([self.__CMD_POWER, self.__CMD_POWER_ON])

            time.sleep(self.__START_TIME)

        finally:
            self.__spi.close()
            self.release_lock()


    def operations_off(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__spi.xfer([self.__CMD_POWER, self.__CMD_POWER_OFF])

            time.sleep(self.__STOP_TIME)

        finally:
            self.__spi.close()
            self.release_lock()



    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__spi.xfer([self.__CMD_READ_HISTOGRAM])
            time.sleep(self.__DELAY_CMD)

            chars = self.__read_bytes(62)
            time.sleep(self.__DELAY_TRANSFER)

            # time...
            rec = LocalizedDatetime.now()

            # bins...
            bins = [Decode.unsigned_int(chars[i:i + 2]) for i in range(0, 32, 2)]

            # bin MToFs...
            bin_1_mtof = chars[32]
            bin_3_mtof = chars[33]
            bin_5_mtof = chars[34]
            bin_7_mtof = chars[35]

            # period...
            period = Decode.float(chars[44:48])

            # checksum...
            chk = Decode.unsigned_int(chars[48:50])

            if chk != sum(bins) % 65535:
                raise ValueError("bad checksum")

            # PMx...
            try:
                pm1 = Decode.float(chars[50:54])
            except TypeError:
                pm1 = None

            try:
                pm2p5 = Decode.float(chars[54:58])
            except TypeError:
                pm2p5 = None

            try:
                pm10 = Decode.float(chars[58:62])
            except TypeError:
                pm10 = None

            return OPCDatum(self.SOURCE, rec, pm1, pm2p5, pm10, period, bins,
                            bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof)

        finally:
            self.__spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def firmware(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # command...
            self.__spi.xfer([self.__CMD_GET_FIRMWARE])
            time.sleep(self.__DELAY_CMD)

            chars = self.__read_bytes(60)

            time.sleep(self.__DELAY_TRANSFER)

            # report...
            report = ''.join(chr(byte) for byte in chars)

            return report.strip('\0\xff')       # \0 - Raspberry Pi, \xff - BeagleBone

        finally:
            self.__spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __read_bytes(self, count):
        return [self.__read_byte() for _ in range(count)]


    def __read_byte(self):
        time.sleep(self.__DELAY_TRANSFER)
        read_bytes = self.__spi.read_bytes(1)

        return read_bytes[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCN2:{io:%s, spi:%s}" % (self.__io, self.__spi)
