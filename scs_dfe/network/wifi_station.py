'''
Created on 31 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://www.codefoster.com/pi-wifi/
https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

sudo iwlist wlan0 scan
'''

import re
import subprocess
import time

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class WiFiStation(JSONable):
    '''
    classdocs

          Cell 01 - Address: 42:B8:9A:BD:6A:BB
                    Channel:6
                    Frequency:2.437 GHz (Channel 6)
                    Quality=51/70  Signal level=-59 dBm
                    Encryption key:on
                    ESSID:"DIRECT-bb-HP M452 LaserJet"
                    Bit Rates:6 Mb/s; 9 Mb/s; 12 Mb/s; 18 Mb/s; 24 Mb/s
                              36 Mb/s; 48 Mb/s; 54 Mb/s
                    Mode:Master
                    Extra:tsf=0000000000000000
                    Extra: Last beacon: 90ms ago
                    IE: Unknown: 001A4449524543542D62622D4850204D343532204C617365724A6574
                    IE: Unknown: 01088C129824B048606C
                    IE: Unknown: 030106
                    IE: Unknown: 200100
                    IE: Unknown: 23021100
                    IE: Unknown: 2A0100
                    IE: Unknown: 2F0100
                    IE: IEEE 802.11i/WPA2 Version 1

    '''

    @classmethod
    def find_all(cls):
        stations = WiFiStation.__find_all()

        if stations is None:
            return None

        return [stations[key] for key in sorted(stations.keys())]


    @classmethod
    def exists(cls, ssid):
        stations = WiFiStation.__find_all()

        if stations is None:
            return None

        return ssid in stations.keys()


    @classmethod
    def find_connected(cls):
        ssid = WiFiStation.__find_connected_ssid()

        if ssid is None:
            return None

        stations = WiFiStation.__find_all()

        return stations[ssid]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __find_all(cls):
        stations = {}
        station = None

        scan = WiFiStation.__scan()

        if scan is None:
            return None

        connected_ssid = WiFiStation.__find_connected_ssid()

        # parse...
        for line in scan.splitlines():
            # new station...
            if re.search(r'Cell [0-9]+ - Address', line):
                if station:
                    stations[station.__ssid] = station

                station = WiFiStation()
                continue

            # ssid...
            matches = re.search(r'ESSID:"(.+)"', line)
            if matches:
                station.__ssid = matches.group(1)
                station.__is_connected = station.__ssid == connected_ssid
                continue

            # encryption...
            matches = re.search(r'Encryption key:(.+)', line)
            if matches:
                station.__encryption = matches.group(1) == 'on'
                continue

            # quality...
            matches = re.search(r'Quality=([0-9]+)/([0-9]+)', line)
            if matches:
                station.__quality = round(float(matches.group(1)) / float(matches.group(2)), 2)
                continue

            # security...
            matches = re.search(r'IE: IEEE .+/(.+)', line)
            if matches:
                station.__security = matches.group(1)

        stations[station.__ssid] = station

        return stations


    @classmethod
    def __scan(cls):
        while True:
            p = subprocess.Popen(['sudo', 'iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            response = p.communicate()

            scan = response[0].decode()

            # network down?...
            matches = re.search(r'Network is down', scan)
            if matches:
                return None

            # busy?...
            matches = re.search(r'Device or resource busy', scan)
            if not matches:
                break

            time.sleep(1)

        return scan


    @classmethod
    def __find_connected_ssid(cls):
        '''
        also: sudo iwlist wlan0 scan
        '''
        p = subprocess.Popen(['iwgetid', '-r'], stdout=subprocess.PIPE)
        response = p.communicate()

        ssid = response[0].decode().strip()

        if len(ssid) == 0:
            return None

        return ssid


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ssid = None, encryption = None, quality = None, security = None, is_connected = None):
        '''
        Constructor
        '''
        self.__ssid = ssid
        self.__encryption = encryption
        self.__quality = quality
        self.__security = security

        self.__is_connected = is_connected


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ssid'] = self.ssid
        jdict['encryption'] = self.encryption
        jdict['quality'] = self.quality
        jdict['security'] = self.security

        jdict['is_connected'] = self.is_connected

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ssid(self):
        return self.__ssid


    @property
    def encryption(self):
        return self.__encryption


    @property
    def quality(self):
        return self.__quality


    @property
    def security(self):
        return self.__security


    @property
    def is_connected(self):
        return self.__is_connected


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "WiFiStation:{ssid:%s, encryption:%s, quality:%s, security:%s, is_connected:%s}" % \
                    (self.ssid, self.encryption, self.quality, self.security, self.is_connected)
