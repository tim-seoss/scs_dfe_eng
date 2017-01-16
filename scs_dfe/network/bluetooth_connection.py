"""
Created on 27 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import pty
import subprocess

from multiprocessing import Pipe
from multiprocessing import Process


# --------------------------------------------------------------------------------------------------------------------

class BluetoothConnection(Process):
    """
    classdocs
    """

    WAITING = 1
    CONNECTED = 2
    DISCONNECTED = 3
    STOPPED = 4
    FAILED = 0

    __conn = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def enable(cls):
        # enable scan...
        p = subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'], stdout=subprocess.PIPE)

        # add sp service..
        p = subprocess.call(['sudo', 'sdptool', 'add', 'sp'], stdout=subprocess.PIPE)


    @classmethod
    def monitor(cls):
        if BluetoothConnection.__conn is not None:
            raise RuntimeError("BluetoothConnection.monitor: a connection instance is already running.")

        # construct connection...
        output, input = Pipe()

        BluetoothConnection.__conn = BluetoothConnection(input)
        BluetoothConnection.__conn.start()

        input.close()

        # monitor...
        while True:
            try:
                state = output.recv()

                if state == BluetoothConnection.FAILED:
                    # BluetoothConnection.__conn.terminate()          # this causes a problem in a use case that I can't remember
                    print("monitor: failed")
                    break

            except EOFError:
                print("monitor: EOF")
                BluetoothConnection.__conn.join()
                return

            yield (state)

        BluetoothConnection.__conn.join()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pipe_input):
        Process.__init__(self)

        self.__pipe_input = pipe_input


    def run(self):
        pty.spawn(['sudo', 'rfcomm', 'watch', 'hci0'], self.__read)      # using spawn because we need live data feed   listen  '-S',


    # ----------------------------------------------------------------------------------------------------------------

    def __read(self, fd):
        # read...
        data = os.read(fd, 1024)
        lines = data.decode().strip().splitlines()

        if len(lines) == 0:
            return data

        msg = lines[0]

        # parse...
        if "Waiting for connection" in msg:
            state = BluetoothConnection.WAITING

        elif "Connection from" in msg:
            state = BluetoothConnection.CONNECTED

        elif "Disconnected" in msg:
            state = BluetoothConnection.DISCONNECTED

        elif "Can't bind RFCOMM socket" in msg:
            state = BluetoothConnection.FAILED

        elif "^C" in msg:
            state = BluetoothConnection.STOPPED

        else:
            return data

        # send...
        self.__pipe_input.send(state)

        return data


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BluetoothConnection:{pipe_input:%s}" % self.__pipe_input

