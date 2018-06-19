"""
Created on 19 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.nxp.com/docs/en/data-sheet/MPL115A2.pdf
https://www.nxp.com/docs/en/application-note/AN3785.pdf
https://community.nxp.com/thread/73878

https://gist.github.com/asciiphil/6167905
"""

import time

from scs_dfe.pressure.mpl115a2_driver import MPL115A2Driver

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class MPL115A2(object):
    """
    NXP MPL115A2 digital barometer
    """

    # ----------------------------------------------------------------------------------------------------------------

    __PRESSURE_CONV =   (115.0 - 50.0) / 1023.0

    __DEFAULT_C25 = 472                                 # T adc counts at 25 ºC
    __COUNTS_PER_DEGREE =  -5.35                        # T adc counts per degree centigrade


    # ----------------------------------------------------------------------------------------------------------------

    # sampling...
    __REG_P_ADC =       MPL115A2Driver(0x00, 10, 0,  0, 0)
    __REG_T_ADC =       MPL115A2Driver(0x02, 10, 0,  0, 0)

    # calibration...
    __REG_A0 =          MPL115A2Driver(0x04, 16, 1,  3, 0)
    __REG_B1 =          MPL115A2Driver(0x06, 16, 1, 13, 0)
    __REG_B2 =          MPL115A2Driver(0x08, 16, 1, 14, 0)
    __REG_C12 =         MPL115A2Driver(0x0a, 14, 1, 13, 9)


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =    2.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__a0 = None
        self.__b1 = None
        self.__b2 = None
        self.__c12 = None


    # ----------------------------------------------------------------------------------------------------------------

    def init(self):
        try:
            self.obtain_lock()

            self.__a0 = self.__REG_A0.read()
            self.__b1 = self.__REG_B1.read()
            self.__b2 = self.__REG_B2.read()
            self.__c12 = self.__REG_C12.read()

        finally:
            self.release_lock()


    def sample(self):
        try:
            self.obtain_lock()

            MPL115A2Driver.convert()
            time.sleep(0.005)

            # read...
            p_adc = self.__REG_P_ADC.read()
            t_adc = self.__REG_T_ADC.read()

            # interpret...
            p_comp = self.__a0 + (self.__b1 + self.__c12 * t_adc) * p_adc + self.__b2 * t_adc

            pressure = round(p_comp * self.__PRESSURE_CONV + 50.0, 1)
            temperature = round((t_adc - self.__DEFAULT_C25) / self.__COUNTS_PER_DEGREE + 25.0, 1)

            return pressure, temperature

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__class__.__name__, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__class__.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPL115A2:{a0:%s, b1:%s, b2:%s, c12:%s}" % (self.__a0, self.__b1, self.__b2, self.__c12)


