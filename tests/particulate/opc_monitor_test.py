#!/usr/bin/env python3

"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.python.org/3/library/multiprocessing.html#sharing-state-between-processes
http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing/
"""

import sys
import time

from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_core.sync.interval_timer import IntervalTimer


# --------------------------------------------------------------------------------------------------------------------
# run...

if __name__ == '__main__':

    interval = 5

    monitor = OPCMonitor(interval)
    print("main: %s" % monitor)

    timer = IntervalTimer(interval)

    time.sleep(1)                       # make main loop one second ahead of monitor loop
    proc = monitor.start()

    while timer.true():
        datum = monitor.sample()

        print("main: %s" % datum)
        print("main: -")
        sys.stdout.flush()

        if not proc.is_alive():
            break
