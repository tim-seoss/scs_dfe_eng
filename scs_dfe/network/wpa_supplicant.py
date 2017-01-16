'''
Created on 1 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
'''

import re

from collections import OrderedDict

from scs_core.common.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class WPASupplicant(JSONable):
    '''
    classdocs

    network={
        ssid="YOUR_NETWORK_NAME"
        psk="YOUR_NETWORK_PASSWORD"
        proto=RSN
        key_mgmt=WPA-PSK
        pairwise=CCMP
        auth_alg=OPEN
        }

    '''

    KEY_MGMT = "WPA-PSK"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_entry(cls, entry):
        matches = re.search(r'network\s*=\s*\{\s*ssid="(.+)"\s*psk="(.+)"\s*key_mgmt=(.+)\s*\}', entry)

        if matches:
            return WPASupplicant(matches.group(1), matches.group(2), matches.group(3))

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ssid, psk, key_mgmt):
        '''
        Constructor
        '''
        self.__ssid = ssid
        self.__psk = psk
        self.__key_mgmt = key_mgmt


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ssid'] = self.ssid
        jdict['key_mgmt'] = self.key_mgmt

        return jdict


    def as_entry(self):
        entry = 'network={\n\tssid="%s"\n\tpsk="%s"\n\tkey_mgmt=%s\n}' % (self.ssid, self.psk, self.key_mgmt)

        return entry


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ssid(self):
        return self.__ssid


    @property
    def psk(self):
        return self.__psk


    @property
    def key_mgmt(self):
        return self.__key_mgmt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "WPASupplicant:{ssid:%s, psk:%s, key_mgmt:%s}" % (self.ssid, self.psk, self.key_mgmt)
