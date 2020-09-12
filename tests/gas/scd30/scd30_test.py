#!/usr/bin/env python3

"""
Created on 7 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.average import Average
from scs_core.data.json import JSONify

from scs_dfe.gas.scd30.scd30 import SCD30

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

sampling_interval = 3

try:
    I2C.open(Host.I2C_SENSORS)

    sensor = SCD30()
    print(sensor)
    print("-", file=sys.stderr)

    # sensor.reset()


    # ----------------------------------------------------------------------------------------------------------------
    # sensor...

    firmware = sensor.get_firmware_version()
    print("firmware: %s" % str(firmware), file=sys.stderr)


    serial = sensor.get_serial_no()
    print("serial: %s" % str(serial), file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # temperature_offset...

    temperature_offset = sensor.get_temperature_offset()
    print("old temperature_offset: %s" % temperature_offset, file=sys.stderr)

    # sensor.set_temperature_offset(0.0)

    temperature_offset = sensor.get_temperature_offset()
    print("new temperature_offset: %s" % temperature_offset, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # altitude...

    altitude = sensor.get_altitude()
    print("old altitude: %s" % altitude, file=sys.stderr)

    # sensor.set_altitude(100)
    #
    # altitude = sensor.get_altitude()
    # print("new altitude: %s" % altitude, file=sys.stderr)
    # print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # forced_calib...

    forced_calib = sensor.get_forced_calib()
    print("old forced_calib: %s" % forced_calib, file=sys.stderr)

    # sensor.set_forced_calib(1000)

    # forced_calib = sensor.get_forced_calib()
    # print("new forced_calib: %s" % forced_calib, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # auto_self_calib...
    auto_self_calib = sensor.get_auto_self_calib()
    print("old auto_self_calib: %s" % auto_self_calib, file=sys.stderr)

    sensor.set_auto_self_calib(True)

    auto_self_calib = sensor.get_auto_self_calib()
    print("new auto_self_calib: %s" % auto_self_calib, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # ready...

    ready = sensor.get_data_ready()
    print("ready: %s" % ready, file=sys.stderr)
    print("-", file=sys.stderr)

    if ready:
        measurement = sensor.read_measurement()         # discard reading from previous test


    # ----------------------------------------------------------------------------------------------------------------
    # interval...

    interval = sensor.get_measurement_interval()
    print("old interval: %s" % interval, file=sys.stderr)

    sensor.set_measurement_interval(sampling_interval)

    interval = sensor.get_measurement_interval()
    print("new interval: %s" % interval, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # sensor.stop_periodic_measurement()

    for pressure in (90, 100, 110, None):
        print("pressure: %s" % pressure, file=sys.stderr)

        average = Average()

        sensor.start_periodic_measurement(pressure)

        for _ in range(10):
            start_time = time.time()

            while not sensor.get_data_ready():
                time.sleep(0.1)

            measurement = sensor.read_measurement()
            end_time = time.time() - start_time

            print("%0.1f: %s" % (end_time, JSONify.dumps(measurement.as_json())))
            sys.stdout.flush()

            average.append(measurement)

            sensor.start_periodic_measurement(pressure)

        print("average: %s" % average.compute())
        print("-", file=sys.stderr)


except KeyboardInterrupt:
    print()

finally:
    I2C.close()
