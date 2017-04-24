#!/usr/bin/env python3

"""
Created on 1 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)


    # ----------------------------------------------------------------------------------------------------------------

    sht_conf = SHTConf.load_from_host(Host)
    sht = sht_conf.int_sht()

    sht.reset()

    sht = sht.sample()
    print(sht)
    print("-")


    # ----------------------------------------------------------------------------------------------------------------

    calib = Pt1000Calib.load_from_host(Host)
    print(calib)
    print("-")

    pt1000 = Pt1000(calib)
    print(pt1000)
    print("-")

    afe = AFE(pt1000, [])
    print(afe)
    print("-")

    pt1000_datum = afe.sample_temp()
    print(pt1000_datum)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    v20 = pt1000_datum.v20(sht.temp)
    print(v20)
    print("-")

    calib = Pt1000Calib(None, v20)
    print(calib)
    print("=")

    calib.save(Host)

    pt1000 = Pt1000(calib)
    print(pt1000)
    print("-")

    afe = AFE(pt1000, [])
    print(afe)
    print("-")

    pt1000_datum = afe.sample_temp()
    print(pt1000_datum)
    print("-")


finally:
    I2C.close()

