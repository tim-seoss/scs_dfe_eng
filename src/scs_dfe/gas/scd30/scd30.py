"""
Created on 7 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NB: 1 kPa = 10 mBar

https://www.sensirion.com/en/download-center/carbon-dioxide-sensors-co2/co2-sensor/
https://github.com/Sensirion/embedded-scd/releases/tag/2.1.0
"""

import time

from scs_core.data.datum import Decode, Encode
from scs_core.gas.scd30.scd30_datum import SCD30Datum

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class SCD30(object):
    """
    classdocs
    """

    DEFAULT_I2C_ADDR =                      0x61

    DEFAULT_AMBIENT_PRESSURE =              101.3                   # kPa

    MIN_SAMPLING_INTERVAL =                 2                       # seconds
    MAX_SAMPLING_INTERVAL =                 1800                    # seconds

    MIN_FORCED_CALIB =                      400                     # ppm
    MAX_FORCED_CALIB =                      2000                    # ppm

    MIN_PRESSURE =                          70.0                    # kPa
    MAX_PRESSURE =                          140.0                   # kPa

    # ----------------------------------------------------------------------------------------------------------------

    __CMD_START_PERIODIC_MEASUREMENT =      0x0010
    __CMD_STOP_PERIODIC_MEASUREMENT =       0x0104
    __CMD_GET_DATA_READY =                  0x0202
    __CMD_READ_MEASUREMENT =                0x0300
    __CMD_MEASUREMENT_INTERVAL =            0x4600
    __CMD_TEMPERATURE_OFFSET =              0x5403
    __CMD_ALTITUDE =                        0x5102
    __CMD_AUTO_SELF_CALIBRATION =           0x5306
    __CMD_FORCED_RECALIBRATION =            0x5204
    __CMD_READ_SERIAL_NUMBER =              0xd033
    __CMD_READ_FIRMWARE_VERSION =           0xd100
    __CMD_RESET =                           0xd304

    __SERIAL_NUM_WORDS =                    16
    __CMD_DELAY =                           0.004
    __WRITE_DELAY =                         0.2

    __CRC8_POLYNOMIAL =                     0x31
    __CRC8_INIT =                           0xff
    __CRC8_LEN =                            1

    __LOCK_TIMEOUT =                        2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def null_datum(cls):
        return SCD30Datum(None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):           # TODO: remove addr
        """
        Constructor
        """
        self.__addr = addr
        self.__ambient_pressure_kpa = None


    # ----------------------------------------------------------------------------------------------------------------
    # sample...

    def sample(self):
        while not self.get_data_ready():
            time.sleep(0.1)

        return self.read_measurement()


    def get_data_ready(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_GET_DATA_READY)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        return bool(Decode.int(words[0], '>'))


    def read_measurement(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_READ_MEASUREMENT)
            words = self.__read_words(6)

        finally:
            self.release_lock()

        co2 = Decode.float(words[0] + words[1], '>')
        temp = Decode.float(words[2] + words[3], '>')
        humid = Decode.float(words[4] + words[5], '>')

        return SCD30Datum(co2, temp, humid)


    # ----------------------------------------------------------------------------------------------------------------
    # period...

    def start_periodic_measurement(self, ambient_pressure_kpa=None):
        if ambient_pressure_kpa and not (self.MIN_PRESSURE <= ambient_pressure_kpa <= self.MAX_PRESSURE):
            raise ValueError(ambient_pressure_kpa)

        ambient_pressure_mbar = 0 if ambient_pressure_kpa is None else int(ambient_pressure_kpa * 10.0)

        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_START_PERIODIC_MEASUREMENT, arg=ambient_pressure_mbar)

            self.__ambient_pressure_kpa = ambient_pressure_kpa

        finally:
            self.release_lock()


    def stop_periodic_measurement(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_STOP_PERIODIC_MEASUREMENT)

        finally:
            self.release_lock()


    def get_measurement_interval(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_MEASUREMENT_INTERVAL)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        return Decode.int(words[0], '>')


    def set_measurement_interval(self, interval):
        if not (self.MIN_SAMPLING_INTERVAL <= interval <= self.MAX_SAMPLING_INTERVAL):
            raise ValueError(interval)

        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_MEASUREMENT_INTERVAL, arg=interval)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # temperature_offset...

    def get_temperature_offset(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_TEMPERATURE_OFFSET)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        return Decode.int(words[0], '>') / 100


    def set_temperature_offset(self, temp_offset):
        int_offset = int(round(temp_offset * 100))

        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_TEMPERATURE_OFFSET, arg=int_offset)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # altitude...

    def get_altitude(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_ALTITUDE)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        return Decode.int(words[0], '>')


    def set_altitude(self, altitude):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_ALTITUDE, arg=altitude)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # auto_self_calib...

    def get_auto_self_calib(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_AUTO_SELF_CALIBRATION)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        return bool(Decode.int(words[0], '>'))


    def set_auto_self_calib(self, on):
        auto_self_calib = 1 if on else 0

        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_AUTO_SELF_CALIBRATION, arg=auto_self_calib)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # forced_calib...

    def get_forced_calib(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_FORCED_RECALIBRATION)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        return Decode.int(words[0], '>')


    def set_forced_calib(self, concentration_ppm):
        if not (self.MIN_FORCED_CALIB <= concentration_ppm <= self.MAX_FORCED_CALIB):
            raise ValueError(concentration_ppm)

        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_FORCED_RECALIBRATION, arg=concentration_ppm)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # reset...

    def reset(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_RESET)
            time.sleep(self.__WRITE_DELAY)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # sensor...

    def get_serial_no(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_READ_SERIAL_NUMBER)
            words = self.__read_words(16)

        finally:
            self.release_lock()

        return ''.join([chr(byte) for word in words for byte in word])


    def get_firmware_version(self):
        try:
            self.obtain_lock()
            self.__cmd(self.__CMD_READ_FIRMWARE_VERSION)
            words = self.__read_words(1)

        finally:
            self.release_lock()

        major = words[0][0]
        minor = words[0][1]

        return major, minor


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return self.__class__.__name__ + "-" + ("0x%02x" % self.addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd, arg=None):
        if arg:
            values = list(Encode.int(arg, '>'))
            values.append(self.__crc(values))
        else:
            values = ()

        try:
            I2C.start_tx(self.addr)
            I2C.write_addr16(cmd, *values)
        finally:
            I2C.end_tx()

        delay = self.__CMD_DELAY if arg is None else self.__WRITE_DELAY
        time.sleep(delay)


    def __read_words(self, word_count):
        char_count = word_count * 3
        words = []

        chars = self.__read(char_count)

        # print(["0x%02x" % char for char in chars])

        for i in range(0, char_count, 3):
            word = chars[i:i + 2]
            crc = chars[i + 2]

            if not self.__crc_check(word, crc):
                raise ValueError(chars)

            words.append(word)

        return words


    def __read(self, char_count):
        try:
            I2C.start_tx(self.addr)
            return I2C.read(char_count)
        finally:
            I2C.end_tx()


    def __crc_check(self, word, crc):
        return crc == self.__crc(word)


    def __crc(self, word):
        crc = self.__CRC8_INIT

        for byte in word:
            crc ^= byte
            for _ in range(8):
                crc = 0xff & ((crc << 1) ^ self.__CRC8_POLYNOMIAL if crc & 0x80 else (crc << 1))

        return crc


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    @property
    def ambient_pressure_kpa(self):
        return self.__ambient_pressure_kpa


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SCD30:{addr:0x%02x, ambient_pressure_kpa:%s}" % (self.addr, self.ambient_pressure_kpa)
