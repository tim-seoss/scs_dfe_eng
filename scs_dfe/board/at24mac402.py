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

class AT24MAC402(object):
    """
    Atmel AT24MAC402 2-Kbit Serial EEPROM plus Embedded Unique 128-bit Serial Number
    """

    SIZE =                  0x0100       # 256 bytes

    __BUFFER_SIZE =         32
    __TWR =                 0.005        # seconds

    __SERIAL_NUMBER_ADDR =  0x80
    __EUI_ADDR =            0x9a


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_array(cls, device_addr, memory_addr, count):
        try:
            I2C.start_tx(device_addr)

            return I2C.read_cmd(memory_addr, count)
        finally:
            I2C.end_tx()


    @classmethod
    def __read_image(cls, memory_addr, count):
        try:
            I2C.start_tx(Host.DFE_EEPROM_ADDR)

            content = I2C.read_cmd(memory_addr, count)

            return EEPROMImage(content)
        finally:
            I2C.end_tx()


    @classmethod
    def __write_image(cls, memory_addr, values):       # max 32 values
        try:
            I2C.start_tx(Host.DFE_EEPROM_ADDR)

            I2C.write_addr(memory_addr, *values)
            time.sleep(cls.__TWR)
        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        initialise with current EEPROM contents
        """
        self.__serial_number = self.__read_array(Host.DFE_EEPROM_ADDR + 8, AT24MAC402.__SERIAL_NUMBER_ADDR, 16)
        self.__eui = self.__read_array(Host.DFE_EEPROM_ADDR + 8, AT24MAC402.__EUI_ADDR, 6)

        # self.__image = self.__read_image(0, AT24MAC402.SIZE)
        self.__image = None


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, image):
        # verify...
        if len(image) != AT24MAC402.SIZE:
            raise ValueError("AT24MAC402.write: image has incorrect length.")

        addr = 0

        # write...
        while addr < len(image.content):
            values = image.content[addr: addr + AT24MAC402.__BUFFER_SIZE]

            self.__write_image(addr, values)

            addr += AT24MAC402.__BUFFER_SIZE

        # reload...
        self.__image = self.__read_image(0, AT24MAC402.SIZE)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return ''.join("%02x" % item for item in self.__serial_number)


    @property
    def eui(self):
        return ':'.join("%02x" % item for item in self.__eui)


    @property
    def image(self):
        return self.__image


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AT24MAC402:{serial_number:%s, eui:%s, image:%s}" % (self.serial_number, self.eui, self.image)
