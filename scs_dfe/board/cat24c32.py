"""
Created on 5 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

in /boot/config.txt

# RPi...
# Uncomment for i2c-0 & i2c-3 access (EEPROM programming)
# dtparam=i2c_vc=on

dtoverlay i2c-gpio i2c_gpio_sda=0 i2c_gpio_scl=1
"""

import time

from scs_core.sys.eeprom_image import EEPROMImage

from scs_dfe.bus.i2c import I2C

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class CAT24C32(object):
    """
    Semiconductor Components Industries CAT24C32 Serial EEPROM
    """

    SIZE =              0x1000       # 4096 bytes

    __BUFFER_SIZE =     32
    __TWR =             0.005        # seconds


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_addr(cls, addr, count):
        try:
            i2c = I2C.start_tx(Host.DFE_EEPROM_ADDR)

            i2c.write16(addr)
            content = i2c.read(count)

            return EEPROMImage(content)
        finally:
            I2C.end_tx()


    @classmethod
    def __write_addr(cls, addr, values):       # max 32 values
        try:
            i2c = I2C.start_tx(Host.DFE_EEPROM_ADDR)

            i2c.write_addr(addr, *values)
            time.sleep(cls.__TWR)
        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        initialise with current EEPROM contents
        """
        self.__image = self.__read_addr(0, CAT24C32.SIZE)


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, image):
        # verify...
        if len(image) != CAT24C32.SIZE:
            raise ValueError("CAT24C32.write: image has incorrect length.")

        addr = 0

        # write...
        while addr < len(image.content):
            values = image.content[addr: addr + CAT24C32.__BUFFER_SIZE]

            self.__write_addr(addr, values)

            addr += CAT24C32.__BUFFER_SIZE

        # reload...
        self.__image = self.__read_addr(0, CAT24C32.SIZE)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def image(self):
        return self.__image


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CAT24C32:{image:%s}" % self.image
