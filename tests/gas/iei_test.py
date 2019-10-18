#!/usr/bin/env python3

"""
Created on 7 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Set DFEConf to IEI before running
"""

import time

from scs_core.data.json import JSONify

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.afe_baseline import AFEBaseline

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.interface.interface_conf import InterfaceConf
from scs_dfe.gas.iei import IEI

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------


try:
    I2C.open(Host.I2C_SENSORS)

    sht_conf = SHTConf.load(Host)
    sht = sht_conf.ext_sht()
    print(sht)
    print("-")

    interface_conf = InterfaceConf.load(Host)
    print(interface_conf)
    print("-")

    interface = interface_conf.interface()
    print(interface)
    print("-")

    afe_calib = AFECalib.load(Host)
    print(afe_calib)
    print("-")

    afe_baseline = AFEBaseline.load(Host)
    print(afe_baseline)
    print("-")

    sensors = afe_calib.sensors(afe_baseline)
    print('\n\n'.join(str(sensor) for sensor in sensors))
    print("-")


# --------------------------------------------------------------------------------------------------------------------
    iei = IEI(sensors)
    print(iei)
    print("-")

    start_time = time.time()
    sht_datum = sht.sample()
    elapsed = time.time() - start_time

    print(sht_datum)
    print("elapsed:%0.3f" % elapsed)
    print("-")

    start_time = time.time()
    sample = iei.sample_station(1, sht_datum)
    elapsed = time.time() - start_time

    print("SN1: %s" % sample)
    print("elapsed:%0.3f" % elapsed)
    print("=")

    start_time = time.time()
    samples = iei.sample(sht_datum)
    elapsed = time.time() - start_time

    print(samples)
    print("elapsed:%0.3f" % elapsed)
    print("-")

    jstr = JSONify.dumps(samples)
    print(jstr)
    print("-")

finally:
    I2C.close()
