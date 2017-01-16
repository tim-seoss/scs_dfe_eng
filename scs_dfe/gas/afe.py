'''
Created on 10 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import time

from scs_dfe.gas.ads1115 import ADS1115
from scs_dfe.gas.afe_datum import AFEDatum
from scs_dfe.gas.mcp3425 import MCP3425


# --------------------------------------------------------------------------------------------------------------------

class AFE(object):
    '''
    Alphasense Analogue Front-End (AFE) with Ti ADS1115 ADC (gases), Microchip Technology MCP3425 ADC (temp)
    '''
    __RATE = ADS1115.RATE_8

    __MUX = (ADS1115.MUX_A3_GND, ADS1115.MUX_A2_GND, ADS1115.MUX_A1_GND, ADS1115.MUX_A0_GND)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pt1000, sensors):
        '''
        Constructor
        '''
        self.__pt1000 = pt1000
        self.__sensors = sensors

        self.__wrk = ADS1115(ADS1115.ADDR_WRK, AFE.__RATE)
        self.__aux = ADS1115(ADS1115.ADDR_AUX, AFE.__RATE)

        self.__temp = MCP3425(MCP3425.GAIN_4, MCP3425.RATE_15)

        self.__tconv = self.__wrk.tconv


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: this is where sensors can be labelled, e.g. (str(index + 1) + ':' + sensor.gas_name, sample)

    def sample(self):
        pt1000_datum = self.sample_temp()

        samples = []
        for index in range(len(self.__sensors)):
            sensor = self.__sensors[index]
            if sensor is None:
                continue

            sample = sensor.sample(self, pt1000_datum.temp, index)

            samples.append((sensor.gas_name, sample))

        return AFEDatum(pt1000_datum, *samples)


    def sample_station(self, sn):
        index = sn - 1

        pt1000_datum = self.sample_temp()

        sensor = self.__sensors[index]

        if sensor is None:
            return AFEDatum(pt1000_datum)

        sample = sensor.sample(self, pt1000_datum.temp, index)

        return AFEDatum(pt1000_datum, (sensor.gas_name, sample))


    def sample_temp(self):
        return self.__pt1000.sample(self)


    # ----------------------------------------------------------------------------------------------------------------

    def sample_raw_wrk_aux(self, index, gain):
        try:
            mux = AFE.__MUX[index]

            self.__wrk.start_conversion(mux, gain)
            self.__aux.start_conversion(mux, gain)

            time.sleep(self.__tconv)

            weV = self.__wrk.read_conversion()
            aeV = self.__aux.read_conversion()

            return weV, aeV

        finally:
            self.__wrk.release_lock()
            self.__aux.release_lock()


    def sample_raw_wrk(self, index, gain):
        try:
            mux = AFE.__MUX[index]

            self.__wrk.start_conversion(mux, gain)

            time.sleep(self.__tconv)

            weV = self.__wrk.read_conversion()

            return weV

        finally:
            self.__wrk.release_lock()


    def sample_raw_tmp(self):
        try:
            self.__temp.start_conversion()

            time.sleep(self.__temp.tconv)

            return self.__temp.read_conversion()

        finally:
            self.__temp.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        sensors = '[' + ', '.join([str(sensor) for sensor in self.__sensors]) + ']'

        return "AFE:{pt1000:%s, sensors:%s, tconv:%0.3f, wrk:%s, aux:%s, temp:%s}" % \
                        (self.__pt1000, sensors, self.__tconv, self.__wrk, self.__aux, self.__temp)
