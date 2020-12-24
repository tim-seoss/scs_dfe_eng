#!/usr/bin/env python3

"""
Created on 23 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.gas.afe.ads1115 import ADS1115

from scs_host.bus.i2c import SensorI2C


# --------------------------------------------------------------------------------------------------------------------

ADS1115.init()

gain = ADS1115.GAIN_1p024
rate = ADS1115.RATE_8

sn1 = ADS1115.MUX_A3_GND
sn2 = ADS1115.MUX_A2_GND
sn3 = ADS1115.MUX_A1_GND
sn4 = ADS1115.MUX_A0_GND

mux = sn4


# --------------------------------------------------------------------------------------------------------------------

try:
    SensorI2C.open()

    wrk = ADS1115(ADS1115.ADDR_WRK, rate)
    print("wrk: %s" % wrk)

    aux = ADS1115(ADS1115.ADDR_AUX, rate)
    print("aux: %s" % aux)

    wrk.start_conversion(mux, gain)
    aux.start_conversion(mux, gain)

    time.sleep(wrk.tconv)

    v_wrk = wrk.read_conversion()
    v_aux = aux.read_conversion()

    print("wrk v: %0.6f" % v_wrk)
    print("aux v: %0.6f" % v_aux)
    print("-")

    v_wrk = wrk.convert(mux, gain)
    print("wrk v: %0.6f" % v_wrk)

finally:
    SensorI2C.close()
