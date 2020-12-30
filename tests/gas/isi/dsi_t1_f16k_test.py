#!/usr/bin/env python3

"""
Created on 27 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_dfe.gas.isi.dsi_t1_f16k import DSIt1f16K

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

controller = DSIt1f16K(DSIt1f16K.DEFAULT_ADDR)
print(controller)


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    ident = controller.version_ident()
    print("ident:[%s]" % ident)

    tag = controller.version_tag()
    print("tag:[%s]" % tag)

    print("-")

    for _ in range(5):
        controller.start_conversion()
        time.sleep(0.1)

        c_wrk, c_aux = controller.read_conversion_count()
        print('{"wrk": %d, "aux": %d}' % (c_wrk, c_aux))

        sys.stdout.flush()

        time.sleep(2.0)

    print("-")

    while True:
        controller.start_conversion()

        time.sleep(0.1)

        v_wrk, v_aux = controller.read_conversion_voltage()
        print('{"wrk": %0.5f, "aux": %0.5f}' % (v_wrk, v_aux))

        sys.stdout.flush()

        time.sleep(2.0)

except KeyboardInterrupt:
    print("-")

finally:
    I2C.Sensors.close()
