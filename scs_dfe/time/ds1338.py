"""
Created on 16 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Time is always stored as UTC.
"""

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class DS1338(object):
    """
    Maxim Integrated DS1338 serial real-time clock
    """

    CENTURY =               2000

    __ADDR =                0x68

    __REG_SECONDS =         0x00
    __REG_MINUTES =         0x01
    __REG_HOURS =           0x02
    __REG_DAY =             0x03
    __REG_DATE =            0x04
    __REG_MONTH =           0x05
    __REG_YEAR =            0x06
    __REG_CONTROL =         0x07

    __REG_RAM =             0x08

    __MASK_CLOCK_HALT =     0x80        # ---- 1000 0000

    __MASK_SQW_EN =         0x10        # ---- 0001 0000
    __MASK_OSC_STOPPED =    0x20        # ---- 0010 0000


    # ----------------------------------------------------------------------------------------------------------------
    # clock...

    @classmethod
    def set(cls, year, month, date, day, hours, minutes, seconds):
        bcd = cls.__as_bcd(seconds)
        cls.__write_reg(cls.__REG_SECONDS, bcd)

        bcd = cls.__as_bcd(minutes)
        cls.__write_reg(cls.__REG_MINUTES, bcd)

        bcd = cls.__as_bcd(hours)
        cls.__write_reg(cls.__REG_HOURS, bcd)

        bcd = cls.__as_bcd(day)
        cls.__write_reg(cls.__REG_DAY, bcd)

        bcd = cls.__as_bcd(date)
        cls.__write_reg(cls.__REG_DATE, bcd)

        bcd = cls.__as_bcd(month)
        cls.__write_reg(cls.__REG_MONTH, bcd)

        bcd = cls.__as_bcd(year % 100)
        cls.__write_reg(cls.__REG_YEAR, bcd)


    @classmethod
    def square_wave(cls, enabled):
        val = cls.__read_reg(cls.__REG_CONTROL)
        val = val | cls.__MASK_SQW_EN if enabled else val & ~cls.__MASK_SQW_EN

        print("val: 0x%02x" % val)

        cls.__write_reg(cls.__REG_CONTROL, val)


    @classmethod
    def dump(cls):
        val = cls.__read_reg(cls.__REG_SECONDS)
        print("seconds: 0x%02x" % val)
        print("seconds: %d" % cls.__as_decimal(val))
        print("seconds: 0x%02x" % cls.__as_bcd(cls.__as_decimal(val)))

        val = cls.__read_reg(cls.__REG_MINUTES)
        print("minutes: 0x%02x" % val)

        val = cls.__read_reg(cls.__REG_HOURS)
        print("  hours: 0x%02x" % val)

        val = cls.__read_reg(cls.__REG_DAY)
        print("    day: 0x%02x" % val)

        val = cls.__read_reg(cls.__REG_DATE)
        print("   date: 0x%02x" % val)

        val = cls.__read_reg(cls.__REG_MONTH)
        print("  month: 0x%02x" % val)

        val = cls.__read_reg(cls.__REG_YEAR)
        print("   year: 0x%02x" % val)

        val = cls.__read_reg(cls.__REG_CONTROL)
        print("control: 0x%02x" % val)


    # ----------------------------------------------------------------------------------------------------------------
    # RAM...

    @classmethod
    def write(cls, addr, val):
        cls.__write_reg(cls.__REG_RAM + addr, val)


    @classmethod
    def read(cls, addr):
        return cls.__read_reg(cls.__REG_RAM + addr)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_reg(cls, addr):
        try:
            I2C.start_tx(cls.__ADDR)
            val = I2C.read_cmd(addr, 1)
        finally:
            I2C.end_tx()

        return val


    @classmethod
    def __write_reg(cls, addr, val):
        try:
            I2C.start_tx(cls.__ADDR)
            I2C.write(addr, val)
        finally:
            I2C.end_tx()


    @classmethod
    def __as_decimal(cls, bcd):
        msb = bcd >> 4
        lsb = bcd & 0x0f

        return msb * 10 + lsb


    @classmethod
    def __as_bcd(cls, decimal):
        msb = decimal // 10
        lsb = decimal % 10

        return msb << 4 | lsb
