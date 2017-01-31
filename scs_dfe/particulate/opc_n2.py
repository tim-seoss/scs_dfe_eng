"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

    __CMD_POWER                        0x03
    __CMD_POWER_ON                     0x00        //    0x03, 0x00
"""

import struct
import time

from scs_dfe.particulate.opc_datum import OPCDatum

from scs_host.lock.lock import Lock
from scs_host.sys.host_spi import HostSPI


# TODO: unreliable start-up - command timing problem?

# --------------------------------------------------------------------------------------------------------------------

class OPCN2(object):
    """
    classdocs
    """

    __FLOW_RATE_VERSION =               16

    __START_TIME =                      5

    __FAN_UP_TIME =                     10
    __FAN_DOWN_TIME =                   2

    __PERIOD_CONVERSION =               45360       # should be 12000 (1/12MHz * 1000), but found by experiment

    __CMD_POWER =                       0x03
    __CMD_POWER_ON =                    0x00        # 0x03, 0x00
    __CMD_POWER_OFF =                   0x01        # 0x03, 0x01

    __CMD_CHECK_STATUS =                0xcf
    __CMD_READ_HISTOGRAM =              0x30
    __CMD_GET_FIRMWARE_VERSION =        0x3f

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1

    __CMD_DELAY =                       0.01
    __TRANSFER_DELAY =                  0.00002

    __LOCK_TIMEOUT =                    6.0


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __pack_int(byte_values):
        packed = struct.unpack('h', struct.pack('BB', byte_values[0], byte_values[1]))
        return packed[0]


    @staticmethod
    def __pack_float(byte_values):
        packed = struct.unpack('f', struct.pack('BBBB', byte_values[0], byte_values[1], byte_values[2], byte_values[3]))
        return packed[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__spi = HostSPI(0, OPCN2.__SPI_MODE, OPCN2.__SPI_CLOCK)
        # self.__spi = BBIOSPI(0, OPCN2.__SPI_MODE, OPCN2.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def on(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            # start...
            self.__spi.xfer([OPCN2.__CMD_POWER, OPCN2.__CMD_POWER_ON])
            time.sleep(OPCN2.__START_TIME)

            # clear histogram...
            self.__spi.xfer([OPCN2.__CMD_READ_HISTOGRAM])
            time.sleep(OPCN2.__CMD_DELAY)

            for _ in range(62):
                self.__read_byte()

        finally:
            time.sleep(OPCN2.__CMD_DELAY)

            self.__spi.close()
            self.release_lock()


    def off(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__spi.xfer([OPCN2.__CMD_POWER, OPCN2.__CMD_POWER_OFF])

        finally:
            time.sleep(OPCN2.__CMD_DELAY)

            self.__spi.close()
            self.release_lock()


    def sample(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__spi.xfer([OPCN2.__CMD_READ_HISTOGRAM])
            time.sleep(OPCN2.__CMD_DELAY)

            # bins...
            bins = [None] * 16

            for i in range(16):
                bins[i] = self.__read_int()

            # bin MToFs...
            bin_1_mtof = self.__read_byte()
            bin_3_mtof = self.__read_byte()
            bin_5_mtof = self.__read_byte()
            bin_7_mtof = self.__read_byte()

            # flow rate...
            self.__spi.read_bytes(4)

            # temperature
            self.__spi.read_bytes(4)

            # period...
            period = self.__read_float()

            # checksum...
            self.__read_int()

            # PMx...
            pm1 = self.__read_float()
            pm2p5 = self.__read_float()
            pm10 = self.__read_float()

            return OPCDatum(pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof)

        finally:
            time.sleep(OPCN2.__CMD_DELAY)

            self.__spi.close()
            self.release_lock()


    def firmware(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__spi.xfer([OPCN2.__CMD_GET_FIRMWARE_VERSION])
            time.sleep(OPCN2.__CMD_DELAY)

            read_bytes = []

            for _ in range(60):
                time.sleep(OPCN2.__TRANSFER_DELAY)
                read_bytes.extend(self.__spi.read_bytes(1))

            report = '' . join(chr(b) for b in read_bytes)

            return report.strip('\0\xff')       # \0 - Raspberry Pi, \xff - BeagleBone

        finally:
            time.sleep(OPCN2.__CMD_DELAY)

            self.__spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(OPCN2.__name__, OPCN2.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(OPCN2.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __read_byte(self):
        time.sleep(OPCN2.__TRANSFER_DELAY)
        read_bytes = self.__spi.read_bytes(1)

        return read_bytes[0]


    def __read_int(self):
        read_bytes = []

        for _ in range(2):
            time.sleep(OPCN2.__TRANSFER_DELAY)
            read_bytes.extend(self.__spi.read_bytes(1))

        return OPCN2.__pack_int(read_bytes)


    def __read_float(self):
        read_bytes = []

        for _ in range(4):
            time.sleep(OPCN2.__TRANSFER_DELAY)
            read_bytes.extend(self.__spi.read_bytes(1))

        return OPCN2.__pack_float(read_bytes)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCN2:{spi:%s}" % self.__spi
