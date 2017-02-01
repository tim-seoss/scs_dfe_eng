#!/usr/bin/env python3

"""
Created on 25 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.eeprom_image import EEPROMImage

from scs_dfe.board.cat24c32 import CAT24C32

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Host.enable_eeprom_access()


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_EEPROM)

    file_image = EEPROMImage.construct_from_file('/home/pi/hats/eepromutils/myhat.eep', CAT24C32.SIZE) # hard-coded path

    print("file:")
    file_image.formatted(32)
    print("-")

    eeprom = CAT24C32()
    eeprom.write(file_image)

    eeprom_image = eeprom.image

    print("eeprom:")
    eeprom_image.formatted(32)
    print("-")

    verified = eeprom_image == file_image
    print("verified:%s" % verified)
    print("-")

finally:
    I2C.close()
