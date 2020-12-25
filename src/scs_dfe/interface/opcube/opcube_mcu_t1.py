"""
Created on 31 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

STMicro controller for Raspberry Pi Zero Header Breakout board (PZHB) Type 3

https://github.com/south-coast-science/scs_opcube_controller_t1
https://github.com/STMicroelectronics/STM32CubeF3/blob/master/Projects/STM32F302R8-Nucleo/Examples/ADC/ADC_Sequencer/Src/main.c
https://github.com/STMicroelectronics/STM32CubeL0/blob/master/Projects/NUCLEO-L031K6/Examples/ADC/ADC_DMA_Transfer/Src/main.c
"""

import time

from scs_core.data.datum import Decode

from scs_dfe.interface.opcube.opcube_led import OPCubeLED
from scs_dfe.interface.opcube.opcube_mcu import OPCubeMCU

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class OPCubeMCUt1(OPCubeMCU):
    """
    Constructor
    """

    DEFAULT_ADDR =          0x76

    # ----------------------------------------------------------------------------------------------------------------

    __SEND_WAIT_TIME =      0.010                   # seconds
    __LOCK_TIMEOUT =        2.0                     # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr


    # ----------------------------------------------------------------------------------------------------------------

    def host_shutdown_initiated(self):
        self.__cmd(0, 'h', 'i')


    def switch_state(self):
        response = self.__cmd(1, 's', 's')
        on = response == 1

        return on


    def version_ident(self):
        response = self.__cmd(40, 'v', 'i')

        return ''.join([chr(byte) for byte in response]).strip()


    def version_tag(self):
        response = self.__cmd(11, 'v', 't')

        return ''.join([chr(byte) for byte in response]).strip()


    # ----------------------------------------------------------------------------------------------------------------

    def read_temperature(self):
        response = self.__cmd(4, 'm', 't')
        temperature = Decode.float(response[0:4], '<')

        return round(temperature, 1)


    def read_temperature_count(self):
        response = self.__cmd(2, 'm', 'c')
        temperature_count = Decode.int(response[0:2], '<')

        return temperature_count


    def read_t30(self):
        response = self.__cmd(2, 'm', '3')
        t30 = Decode.int(response[0:2], '<')

        return t30


    def read_t130(self):
        response = self.__cmd(2, 'm', '1')
        t130 = Decode.int(response[0:2], '<')

        return t130


    # ----------------------------------------------------------------------------------------------------------------

    def led(self):
        return OPCubeLED(self)


    def power_gases(self, enable):                  # switches digital component only
        self.__cmd(0, 'p', 'g', enable)


    def power_gps(self, enable):
        self.__cmd(0, 'p', 'p', enable)


    def power_modem(self, enable):
        self.__cmd(0, 'p', 'm', enable)


    def power_ndir(self, enable):
        self.__cmd(0, 'p', 'n', enable)


    def power_opc(self, enable):
        self.__cmd(0, 'p', 'o', enable)


    # ----------------------------------------------------------------------------------------------------------------

    def led1(self, on):
        self.__cmd(0, 'l', '1', on)                 # LED 1: red


    def led2(self, on):
        self.__cmd(0, 'l', '2', on)                 # LED 2: green


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, response_size, device, command, arg=0):
        message = [ord(device), ord(command), arg]

        try:
            self.obtain_lock()
            I2C.Utilities.start_tx(self.__addr)

            response = I2C.Utilities.read_cmd(message, response_size, self.__SEND_WAIT_TIME)
            time.sleep(self.__SEND_WAIT_TIME)

            return response

        finally:
            I2C.Utilities.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return "%s-0x%02x" % (self.__class__.__name__, self.__addr)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCubeMCUt1:{addr:0x%0.2x}" % self.addr
