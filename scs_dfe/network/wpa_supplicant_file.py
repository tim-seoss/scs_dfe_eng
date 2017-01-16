'''
Created on 1 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
'''

import os
import re
import subprocess

from scs_dfe.network.wpa_supplicant import WPASupplicant


# --------------------------------------------------------------------------------------------------------------------

class WPASupplicantFile(object):
    '''
    classdocs
    '''

    __TMP_DIR =         "/tmp/southcoastscience/"
    __LIVE_DIR =        "/etc/wpa_supplicant/"

    __FILE =            "wpa_supplicant.conf"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        '''
        Establish the /tmp/southcoastscience/ root.
        Should be invoked on class load.
        '''
        try:
            os.makedirs(cls.__TMP_DIR)
        except FileExistsError:
            pass


    @classmethod
    def read(cls):
        live_file = cls.__LIVE_DIR + cls.__FILE

        # file...
        p = subprocess.Popen(['sudo', 'cat', live_file], stdout=subprocess.PIPE)
        response = p.communicate()
        text = response[0].decode()

        # headers...
        headers = []
        for line in [line.strip() for line in text.splitlines()]:
            matches = re.search(r'network\s*=\s*\{', line)

            if matches:
                break

            if len(line) > 0:
                headers.append(line)

        # entries...
        entries = {}
        matches = re.findall(r'network\s*=\s*\{[^\}]+\}', text, re.DOTALL)

        for match in matches:
            entry = WPASupplicant.construct_from_entry(match)
            entries[entry.ssid] = entry

        return WPASupplicantFile(headers, entries)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, headers, supplicants):
        '''
        Constructor
        '''
        self.__headers = headers                # array of string
        self.__supplicants = supplicants        # dictionary of ssid: WPASupplicant


    def write(self):
        tmp_file = WPASupplicantFile.__TMP_DIR + WPASupplicantFile.__FILE
        live_file = WPASupplicantFile.__LIVE_DIR + WPASupplicantFile.__FILE

        # headers...
        content = '\n'.join(self.__headers)
        content += '\n\n'

        # entries...
        content += '\n\n'.join([supplicant.as_entry() for supplicant in self.supplicants])
        content += '\n'

        # file...
        with open(tmp_file, 'wt') as tmp:
            tmp.write(content)
            tmp.close()

        os.system('sudo mv %s %s' % (tmp_file, live_file))      # does not work with Popen!

        # security compliance...
        os.system('sudo chown root:root %s' % live_file)
        os.system('sudo chmod 600 %s' % live_file)

    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, supplicant):
        self.__supplicants[supplicant.ssid] = supplicant


    def remove(self, ssid):
        if ssid in self.__supplicants:
            del self.__supplicants[ssid]
            return True

        return False

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def headers(self):
        return self.__headers


    @property
    def supplicants(self):
        return [self.__supplicants[ssid] for ssid in self.__supplicants]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        supplicants = '[' + ', '.join([str(supplicant) for supplicant in self.supplicants]) + ']'

        return "WPASupplicantFile:{headers:%s, supplicants:%s}" % (self.headers, supplicants)

# --------------------------------------------------------------------------------------------------------------------

WPASupplicantFile.init()
