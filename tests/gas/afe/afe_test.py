#!/usr/bin/env python3

"""
Created on 15 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: this script uses the Pt1000 temp sensor for temperature compensation.
"""

import time

from scs_core.data.json import JSONify

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.afe.pt1000_calib import Pt1000Calib

from scs_dfe.gas.afe.afe import AFE
from scs_dfe.gas.afe.pt1000 import Pt1000

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------


try:
    I2C.open(Host.I2C_SENSORS)


    interface_conf = InterfaceConf.load(Host)
    print(interface_conf)
    print("-")

    interface = interface_conf.interface()
    print(interface)
    print("-")

    pt1000_calib = Pt1000Calib.load(Host)
    print(pt1000_calib)
    print("-")

    pt1000 = Pt1000(pt1000_calib)
    print(pt1000)
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


    # ----------------------------------------------------------------------------------------------------------------
    afe = AFE(interface, pt1000, sensors)
    print(afe)
    print("-")

    start_time = time.time()
    temp = afe.sample_pt1000()
    elapsed = time.time() - start_time

    print(temp)
    print("elapsed:%0.3f" % elapsed)
    print("-")

    start_time = time.time()
    sample = afe.sample_station(1)
    elapsed = time.time() - start_time

    print("SN1: %s" % sample)
    print("elapsed:%0.3f" % elapsed)
    print("-")

    start_time = time.time()
    sample = afe.sample_station(4)
    elapsed = time.time() - start_time

    print("SN4: %s" % sample)
    print("elapsed:%0.3f" % elapsed)
    print("=")

    start_time = time.time()
    samples = afe.sample()
    elapsed = time.time() - start_time

    print(samples)
    print("elapsed:%0.3f" % elapsed)
    print("-")

    jstr = JSONify.dumps(samples)
    print(jstr)
    print("-")

finally:
    I2C.close()
