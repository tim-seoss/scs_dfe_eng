'''
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_dfe.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class TempComp(object):
    '''
    classdocs
    '''

    __MIN_TEMP =        -30
    __MAX_TEMP =         50
    __INTERVAL =         10

    __COMP = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.__COMP = {      # ºC                         -30    -20     -10      0       10      20     30       40      50
                   Sensor.CO_A4:    TempComp(1, 'nT',   [ 1.0,   1.0,    1.0,    1.0,   -0.2,   -0.9,   -1.5,   -1.5,   -1.5]),
                   Sensor.H2S_A4:   TempComp(2, 'kT',   [-1.5,  -1.5,   -1.5,   -0.5,    0.5,    1.0,    0.8,    0.5,    0.3]),
                   Sensor.NO_A4:    TempComp(3, 'kpT',  [ 0.7,   0.7,    0.7,    0.7,    0.8,    1.0,    1.2,    1.4,    1.6]),
                   Sensor.NO2_A43F: TempComp(1, 'nT',   [ 0.8,   0.8,    1.0,    1.2,    1.6,    1.8,    1.9,    2.5,    3.6]),
                   Sensor.OX_A431:  None,
                   Sensor.SO2_A4:   TempComp(4, 'kppT', [ 0.0,   0.0,    0.0,    0.0,    0.0,    0.0,    5.0,   25.0,   45.0])
                }


    @classmethod
    def find(cls, sensor_type):
        if not sensor_type in cls.__COMP:
            raise ValueError("TempComp.find: unrecognised sensor type: %s." % sensor_type)

        return cls.__COMP[sensor_type]


    @classmethod
    def in_range(cls, temp):
        if temp < cls.__MIN_TEMP or temp > cls.__MAX_TEMP:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, algorithm, factor, values):
        '''
        Constructor
        '''
        length = (TempComp.__MAX_TEMP - TempComp.__MIN_TEMP) // TempComp.__INTERVAL + 1

        if len(values) != length:
            raise ValueError("TempComp: value count should be %d." % length)

        self.__algorithm = algorithm    # int
        self.__factor = factor          # string
        self.__values = values          # array of float


    # ----------------------------------------------------------------------------------------------------------------

    def correct(self, calib, temp, weT, aeT):
        '''
        Find corrected we.
        '''
        if not TempComp.in_range(temp):
            return None

        if self.__algorithm == 1:
            return self.__eq1(temp, weT, aeT)

        if self.__algorithm == 2:
            return self.__eq2(temp, weT, aeT, calib.weCAL, calib.aeCAL)

        if self.__algorithm == 3:
            return self.__eq3(temp, weT, aeT, calib.weCAL, calib.aeCAL)

        if self.__algorithm == 4:
            return self.__eq4(temp, weT, calib.weCAL)

        raise ValueError("TempComp.conv: unrecognised algorithm: %d." % self.__algorithm)


    # ----------------------------------------------------------------------------------------------------------------

    def __eq1(self, temp, weT, aeT):
        nT = self.cfT(temp)

        return weT - nT * aeT


    def __eq2(self, temp, weT, aeT, weCAL, aeCAL):
        kT = self.cfT(temp)

        return weT - kT * (weCAL / aeCAL) * aeT


    def __eq3(self, temp, weT, aeT, weCAL, aeCAL):
        kpT = self.cfT(temp)

        return weT - kpT * (weCAL - aeCAL) * aeT


    def __eq4(self, temp, weT, weCAL):
        kppT = self.cfT(temp)

        return weT - weCAL - kppT


    # ----------------------------------------------------------------------------------------------------------------

    def cfT(self, temp):
        '''
        Find the linear-interpolated temperature compensation factor.
        '''
        index = int((temp - TempComp.__MIN_TEMP) // TempComp.__INTERVAL)        # index of start of interval

        # on boundary...
        if temp % TempComp.__INTERVAL == 0:
            return self.__values[index]

        # all others...
        y1 = self.__values[index]                                               # y value at start of interval
        y2 = self.__values[index + 1]                                           # y value at end of interval

        delta_y = y2 - y1

        delta_x = (temp % TempComp.__INTERVAL) / TempComp.__INTERVAL            # proportion of interval

        return y1 + (delta_y * delta_x)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def algorithm(self):
        return self.__algorithm


    @property
    def factor(self):
        return self.__factor


    @property
    def values(self):
        return self.__values


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TempComp:{algorithm:%d, factor:%s, values:%s}" % (self.algorithm, self.factor, self.values)


# --------------------------------------------------------------------------------------------------------------------

TempComp.init()
