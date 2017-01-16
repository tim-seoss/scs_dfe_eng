'''
Created on 29 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import os
import pty
import sys

from multiprocessing import Process


# TODO: handle the case when going from CONNECTED to STOPPED

# --------------------------------------------------------------------------------------------------------------------

class BluetoothSerial(Process):
    '''
    classdocs
    '''

    __serial = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def monitor(cls, handler):
        # if cls.__serial is not None:
        #     raise RuntimeError("BluetoothSerial.monitor: a serial instance is already running.")

        cls.__serial = BluetoothSerial(handler)
        cls.__serial.start()


    @classmethod
    def stop(cls):
        if cls.__serial is None:
            return

        try:
            cls.__serial.join()
        except Exception as ex:
            print("BluetoothSerial.stop: " + type(ex).__name__, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, handler):
        Process.__init__(self)

        self.__handler = handler
        self.__line = ''


    def run(self):
        pty.spawn(['cat', '/dev/rfcomm0'], self.__read)  # using spawn because we need live data feed
        print("BluetoothSerial.run - running")


    # ----------------------------------------------------------------------------------------------------------------

    def __read(self, fd):
        # read chars...
        data = os.read(fd, 1024)
        chars = data.decode()

        self.__line += chars

        if not chars.endswith('\n'):        # accepts both char-by-char and line-by-line clients
            return data

        # get command...
        request = self.__line.strip()
        self.__line = ''

        # process...
        response = self.__handler.respond(request)

        if response:
            self.__write(response)

        return data


    def __write(self, str):
        fout = open('/dev/rfcomm0', 'w')

        print(str, file=fout)
        fout.flush()

        fout.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BluetoothSerial:{handler:%s, line:%s}" % (self.__handler, self.__line)

