#!/usr/bin/env python3

"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.sys.system_temp import SystemTemp

from scs_dfe.interface.component.mcp9808 import MCP9808

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    # ------------------------------------------------------------------------------------------------------------
    # resources...

    board = MCP9808(True)
    print(board)
    print("-")


    # ------------------------------------------------------------------------------------------------------------
    # run...

    board_sample = board.sample()
    print(board_sample)

    host_status = Host.status()
    print(host_status)
    print("-")

    sys_temp = SystemTemp.construct(board_sample, host_status)
    print(sys_temp)

    print(JSONify.dumps(sys_temp))
    print("-")


# ----------------------------------------------------------------------------------------------------------------
# end...

finally:
    I2C.close()
