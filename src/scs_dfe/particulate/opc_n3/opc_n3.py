"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Firmware report:
OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS
"""

import time

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.datum import Datum

from scs_core.particulate.opc_datum import OPCDatum

from scs_dfe.board.io import IO
from scs_dfe.climate.sht31 import SHT31
from scs_dfe.particulate.opc_n3.opc_status import OPCStatus

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock


# TODO: needs reset function

# TODO: create an abstract base class OPC

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

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1

    __DELAY_CMD =                       0.010
    __DELAY_TRANSFER =                  0.010

    __LOCK_TIMEOUT =                    6.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, OPCN3.__LOCK_TIMEOUT)


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
                self.__cmd_laser_on()

            # fan...
            for _ in range(2):
                self.__cmd_fan_on()

        finally:
            time.sleep(self.__FAN_START_TIME)
            self.release_lock()


    def operations_off(self):
        try:
            self.obtain_lock()

            # laser...
            for _ in range(2):
                self.__cmd_laser_off()

            # fan...
            for _ in range(2):
                self.__cmd_fan_off()

        finally:
            time.sleep(self.__FAN_STOP_TIME)
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def firmware(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__cmd(self.__CMD_GET_FIRMWARE)

            response = []
            for _ in range(60):
                response.append(self.__read_byte())

            return ''.join(chr(byte) for byte in response)

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    def version(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__cmd(self.__CMD_GET_VERSION)

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

            self.__cmd(self.__CMD_GET_SERIAL)

            response = []
            for _ in range(60):
                response.append(self.__read_byte())

            report = ''.join(chr(byte) for byte in response)

            pieces = report.split(' ')

            if len(pieces) < 2:
                return None, None

            return pieces[0], pieces[1]

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    def status(self):
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__cmd(self.__CMD_GET_STATUS)

            response = []
            for _ in range(6):
                response.append(self.__read_byte())

            status = OPCStatus.construct(response)
            print(status)

            return status

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):       # TODO: get data in a one-er, and do crc
        try:
            self.obtain_lock()
            self.__spi.open()

            self.__cmd(self.__CMD_READ_HISTOGRAM)

            # bins...
            bins = [None] * 24

            for i in range(24):
                bins[i] = self.__read_int()

            # bin MToFs...
            bin_1_mtof = self.__read_byte()
            bin_3_mtof = self.__read_byte()
            bin_5_mtof = self.__read_byte()
            bin_7_mtof = self.__read_byte()

            # period...
            raw_period = self.__read_int()
            period = round(float(raw_period) / 100.0, 3)

            # flow rate...
            flow_raw = self.__read_int()
            flow = round(float(flow_raw) / 100.0, 3)

            print("flow: %s" % flow)

            # temperature
            raw_temp = self.__read_int()
            temp = round(SHT31.temp(raw_temp), 1)

            print("temp: %s" % temp)

            # humid...
            raw_humid = self.__read_int()
            humid = round(SHT31.humid(raw_humid), 1)

            print("humid: %s" % humid)

            # PMx...
            try:
                pm1 = self.__read_float()
                # pm1 = 0.0 if pm < 0 else pm
            except TypeError:
                pm1 = None

            try:
                pm2p5 = self.__read_float()
                # pm2p5 = 0.0 if pm < 0 else pm
            except TypeError:
                pm2p5 = None

            try:
                pm10 = self.__read_float()
                # pm10 = 0.0 if pm < 0 else pm
            except TypeError:
                pm10 = None

            rcg = self.__read_int()
            rcl = self.__read_int()
            rcr = self.__read_int()
            rco = self.__read_int()

            frc = self.__read_int()

            ls = self.__read_int()
            print("ls: %s" % ls)

            chk = self.__read_int()
            print("chk: %s" % chk)

            now = LocalizedDatetime.now()

            return OPCDatum(self.SOURCE, now, pm1, pm2p5, pm10, period, bins,
                            bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof)

        finally:
            self.__spi.close()

            time.sleep(self.__DELAY_TRANSFER)
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: replace the following with __cmd_power(..) and adjust __cmd(..) accordingly

    def __cmd_laser_on(self):
        try:
            self.__spi.open()

            self.__spi.xfer([self.__CMD_POWER, self.__CMD_LASER_ON])
            time.sleep(self.__DELAY_CMD)

        finally:
            self.__spi.close()


    def __cmd_laser_off(self):
        try:
            self.__spi.open()

            self.__spi.xfer([self.__CMD_POWER, self.__CMD_LASER_OFF])
            time.sleep(self.__DELAY_CMD)

        finally:
            self.__spi.close()


    def __cmd_fan_on(self):
        try:
            self.__spi.open()

            self.__spi.xfer([self.__CMD_POWER, self.__CMD_FAN_ON])
            time.sleep(self.__DELAY_CMD)

        finally:
            self.__spi.close()


    def __cmd_fan_off(self):
        try:
            self.__spi.open()

            self.__spi.xfer([self.__CMD_POWER, self.__CMD_FAN_OFF])
            time.sleep(self.__DELAY_CMD)

        finally:
            self.__spi.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd):
        self.__spi.xfer([cmd])
        time.sleep(self.__DELAY_CMD)

        self.__spi.xfer([cmd])


    def __read_int(self):
        read_bytes = []

        for _ in range(2):
            read_bytes.append(self.__read_byte())

        return Datum.decode_unsigned_int(read_bytes)


    def __read_float(self):
        read_bytes = []

        for _ in range(4):
            read_bytes.append(self.__read_byte())

        return Datum.decode_float(read_bytes)


    def __read_byte(self):
        time.sleep(self.__DELAY_TRANSFER)
        read_bytes = self.__spi.read_bytes(1)

        return read_bytes[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCN3:{io:%s, spi:%s}" % (self.__io, self.__spi)
