#!/usr/bin/env python3

"""
Created on 16 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.interface.opcube.opcube_mcu_t1 import OPCubeMCUt1

from scs_host.bus.i2c import SensorI2C
from scs_host.sys.host import Host

# --------------------------------------------------------------------------------------------------------------------
# resources...

controller = OPCubeMCUt1(OPCubeMCUt1.DEFAULT_ADDR)
print("controller: %s" % controller, file=sys.stderr)

conf = SHTConf.load(Host)
sht = conf.ext_sht()
print("sht: %s" % sht, file=sys.stderr)

timer = IntervalTimer(0.5)


# --------------------------------------------------------------------------------------------------------------------
# run...

try:
    SensorI2C.open()

    while timer.true():
        climate = sht.sample()
        temperature = controller.read_temperature()

        report = {"sht": climate.temp, "ctrl": temperature}
        print(JSONify.dumps(report))
        sys.stdout.flush()

except KeyboardInterrupt:
    print(file=sys.stderr)

finally:
    SensorI2C.close()
