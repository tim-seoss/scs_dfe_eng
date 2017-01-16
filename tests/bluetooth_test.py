#!/usr/bin/env python3

"""
Created on 27 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.monitor.monitor_response import MonitorResponse

from scs_dfe.network.bluetooth_connection import BluetoothConnection
from scs_dfe.network.bluetooth_serial import BluetoothSerial


# --------------------------------------------------------------------------------------------------------------------

class EchoHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def respond(self, command):
        message = None
        error = None

        try:
            message = command

        except Exception as ex:
            error = type(ex).__name__ + ":" + str(ex)

        response = MonitorResponse(message, error)

        return JSONify.dumps(response)


# --------------------------------------------------------------------------------------------------------------------

handler = EchoHandler()

BluetoothConnection.enable()


# --------------------------------------------------------------------------------------------------------------------

for state in BluetoothConnection.monitor():
    print("state:[%s]" % state, end='\r\n')

    if state == BluetoothConnection.FAILED:
        print("FAILED")
        exit(-1)

    if state == BluetoothConnection.STOPPED:
        break

    if state == BluetoothConnection.CONNECTED:
        BluetoothSerial.monitor(handler)

print("DONE", end='\r\n')

