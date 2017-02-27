#!/usr/bin/env python3

"""
Created on 17 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000_calib import Pt1000Calib
from scs_dfe.gas.sensor import Sensor

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

calib = Pt1000Calib.load_from_host(Host)
pt1000 = calib.pt1000()

sensors = (Sensor.find(Sensor.CODE_OX), Sensor.find(Sensor.CODE_NO2), Sensor.find(Sensor.CODE_NO),
           Sensor.find(Sensor.CODE_VOC_PPM))


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    pid = sensors[3]
    print(pid)
    print("-")

    afe = AFE(pt1000, sensors)
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
