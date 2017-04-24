#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.a4_calib import A4Calib


# --------------------------------------------------------------------------------------------------------------------

serial_number = 123456789
sensor_type = 'CO-A4'

we_elc_mv = 275
we_cal_mv = -8
we_tot_mv = 278

ae_elc_mv = 273
ae_cal_mv = -3
ae_tot_mv = 270

we_sens_na = 0.321
we_x_sens_na = None

pcb_gain = -0.73

we_sens_mv = 0.321
we_no2_x_sens_mv = None


# --------------------------------------------------------------------------------------------------------------------

calib = A4Calib(serial_number, sensor_type, we_elc_mv, we_cal_mv, we_tot_mv, ae_elc_mv, ae_cal_mv, ae_tot_mv,
                we_sens_na, we_x_sens_na, pcb_gain, we_sens_mv, we_no2_x_sens_mv)
print(calib)
print("-")
