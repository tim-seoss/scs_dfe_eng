"""
Created on 21 Aug 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

STMicro controller for Raspberry Pi Zero Header Breakout board (PZHB) Type 2

https://github.com/south-coast-science/scs_rpz_header_t2_f1
"""

import time

from scs_core.data.datum import Decode

from scs_dfe.interface.component.mcu_led import MCULED
from scs_dfe.interface.pzhb.pzhb_mcu import PZHBMCU

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class PZHBMCUt2f1(PZHBMCU):
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


    def button_enable(self):
        self.__cmd(0, 'b', 'e')


    def button_pressed(self):
        response = self.__cmd(1, 'b', 'p')

        button_pressed = response == 1

        return button_pressed


    def read_batt_v(self):
        response = self.__cmd(2, 'm', 'b')

        c_batt = Decode.unsigned_int(response[0:2], '<')
        v_batt = 2.0 * 3.3 * c_batt / 4095

        return v_batt


    def read_current_count(self):
        response = self.__cmd(2, 'm', 'c')

        c_current = Decode.unsigned_int(response[0:2], '<')

        return c_current


    def version_ident(self):
        response = self.__cmd(40, 'v', 'i')          # 40

        return ''.join([chr(byte) for byte in response]).strip()


    def version_tag(self):
        response = self.__cmd(11, 'v', 't')

        return ''.join([chr(byte) for byte in response]).strip()


    # ----------------------------------------------------------------------------------------------------------------

    def led(self):
        return MCULED(self)


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
        self.__cmd(0, 'l', '1', on)                 # LED 1


    def led2(self, on):
        self.__cmd(0, 'l', '2', on)                 # LED 2


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, response_size, device, command, arg=0):
        message = [ord(device), ord(command), arg]

        try:
            self.obtain_lock()
            I2C.start_tx(self.__addr)

            response = I2C.read_cmd(message, response_size, self.__SEND_WAIT_TIME)

            time.sleep(self.__SEND_WAIT_TIME)

            return response

        finally:
            I2C.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return self.__class__.__name__ + "-" + ("0x%02x" % self.__addr)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__addr


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PZHBMCUt2f1:{addr:0x%0.2x}" % self.addr
