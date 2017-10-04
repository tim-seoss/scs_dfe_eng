#!/usr/bin/env python3

"""
Created on 17 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: this script uses the Pt1000 temp sensor for temperature compensation.
"""

import time

from scs_core.gas.pt1000_calib import Pt1000Calib
from scs_core.gas.sensor import Sensor

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.pt1000_conf import Pt1000Conf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

pt1000_conf = Pt1000Conf.load(Host)

pt1000_calib = Pt1000Calib.load(Host)
pt1000 = Pt1000(pt1000_calib)

sensors = (Sensor.find(Sensor.CODE_OX), Sensor.find(Sensor.CODE_NO2), Sensor.find(Sensor.CODE_NO),
           Sensor.find(Sensor.CODE_VOC_PPM))


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    pid = sensors[3]
    print(pid)
    print("-")

    afe = AFE(pt1000_conf, pt1000, sensors)
    print(afe)
    print("-")

    while True:
        start_time = time.time()
        wrk = afe.sample_station(4)
        elapsed = time.time() - start_time

        print(wrk)
        time.sleep(1)

finally:
    I2C.close()
