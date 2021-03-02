#!/usr/bin/env python3

"""
Created on 7 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.gas.scd30.scd30_conf import SCD30Conf

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

def run():
    sensor.stop_periodic_measurement()
    sensor.set_measurement_interval(conf.sample_interval)

    sensor.start_periodic_measurement(100)

    time.sleep(10)


# --------------------------------------------------------------------------------------------------------------------

sensor = None

try:
    I2C.Sensors.open()

    conf = SCD30Conf(2, 0)
    print(conf)

    sensor = conf.scd30()
    print(sensor)

    run()

    conf = SCD30Conf(4, 0)
    print(conf)

    sensor = conf.scd30()
    print(sensor)

    run()

except KeyboardInterrupt:
    print()

finally:
    if sensor:
        sensor.stop_periodic_measurement()

    I2C.Sensors.close()
