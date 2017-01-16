#!/usr/bin/env python3

# invoke with ./test/pty_example.py > /dev/null

import os
import pty
import sys


# --------------------------------------------------------------------------------------------------------------------

class PTYTest(object):

    def __init__(self):
        pass


    def read(self, fd):
        data = os.read(fd, 1024)

        print("data:[%s]" % data)           # TODO use socket sender to send the data
        sys.stdout.flush()

        return data


    def run(self):
        pty.spawn(['sudo', 'rfcomm', 'listen', 'hci0'], self.read)      # using spawn because we need live data feed


p = PTYTest()

p.run()


print("DONE")
