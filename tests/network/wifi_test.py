#!/usr/bin/env python3

"""
Created on 31 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.network.wifi_station import WiFiStation


# --------------------------------------------------------------------------------------------------------------------

connected = WiFiStation.find_connected()
print("connected:%s" % connected)
print("-")

stations = WiFiStation.find_all()

if stations is not None:
    for station in stations:
        print(station)

print("-")

print(JSONify.dumps(stations))
print("-")

ssid = "Solaris"

print("%s exists:%s" % (ssid, WiFiStation.exists(ssid)))
print("-")

ssid = "Solar"

print("%s exists:%s" % (ssid, WiFiStation.exists(ssid)))
print("-")

