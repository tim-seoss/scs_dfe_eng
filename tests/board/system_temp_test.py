#!/usr/bin/env python3

"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport
from scs_core.sys.system_temp import SystemTemp

from scs_dfe.board.mcp9808 import MCP9808

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    # ------------------------------------------------------------------------------------------------------------
    # resource...

    board = MCP9808(True)
    print(board)
    print("-")


    # ------------------------------------------------------------------------------------------------------------
    # run...

    board_sample = board.sample()
    print(board_sample)

    mcu_sample = Host.mcu_temp()
    print(mcu_sample)
    print("-")

    sys_temp = SystemTemp.construct(board_sample, mcu_sample)
    print(sys_temp)

    print(JSONify.dumps(sys_temp))
    print("-")


# ----------------------------------------------------------------------------------------------------------------
# end...

except Exception as ex:
    print(JSONify.dumps(ExceptionReport.construct(ex)))

finally:
    I2C.close()
