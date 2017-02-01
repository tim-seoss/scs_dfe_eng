#!/usr/bin/env python3

"""
Created on 25 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import subprocess as sp

from scs_core.sys.eeprom_image import EEPROMImage
from scs_dfe.board.cat24c32 import CAT24C32
from scs_host.bus import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

sp.call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])      # TODO: dtoverlay does not work on BBe


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_EEPROM)

    eeprom = CAT24C32()

finally:
    I2C.close()

eeprom.image.formatted(32)
print("-")

# --------------------------------------------------------------------------------------------------------------------

file_image = EEPROMImage.construct_from_file('/home/pi/hats/eepromutils/myhat.eep', CAT24C32.SIZE)    # hard-coded path

file_image.formatted(32)

print("equals: %s" % (eeprom.image == file_image))
