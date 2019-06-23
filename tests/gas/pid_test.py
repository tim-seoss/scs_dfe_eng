#!/usr/bin/env python3

"""
Created on 17 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: this script uses the Pt1000 temp sensor for temperature compensation.
"""

import time

from scs_core.gas.sensor import Sensor

from scs_dfe.interface.interface_conf import InterfaceConf
from scs_dfe.gas.afe import AFE

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

interface_conf = InterfaceConf.load(Host)
interface = interface_conf.interface()

pt1000 = interface.pt1000(Host)

sensors = (Sensor.find(Sensor.CODE_OX), Sensor.find(Sensor.CODE_NO2), Sensor.find(Sensor.CODE_NO),
           Sensor.find(Sensor.CODE_VOC_PPB_T1))


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    pid = sensors[3]
    print(pid)
    print("-")

    afe = AFE(interface, pt1000, sensors)
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
