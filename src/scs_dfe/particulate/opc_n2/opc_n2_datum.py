"""
Created on 14 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Decode

from scs_core.particulate.opc_datum import OPCDatum


# --------------------------------------------------------------------------------------------------------------------

class OPCN2Datum(OPCDatum):
    """
    classdocs
    """

    SOURCE =                    'N2'
    CHARS =                     62

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, chars):
        if len(chars) != cls.CHARS:
            raise ValueError(chars)

        # time...
        rec = LocalizedDatetime.now().utc()

        # bins...
        bins = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(0, 32, 2)]

        # bin MToFs...
        bin_1_mtof = chars[32]
        bin_3_mtof = chars[33]
        bin_5_mtof = chars[34]
        bin_7_mtof = chars[35]

        # period...
        period = Decode.float(chars[44:48], '<')

        # checksum...
        actual = Decode.unsigned_int(chars[48:50], '<')
        required = sum(bins) % 65536

        if required != actual:
            raise ValueError("bad checksum: required: 0x%04x actual: 0x%04x" % (required, actual))

        # PMx...
        try:
            pm1 = Decode.float(chars[50:54], '<')
        except TypeError:
            pm1 = None

        try:
            pm2p5 = Decode.float(chars[54:58], '<')
        except TypeError:
            pm2p5 = None

        try:
            pm10 = Decode.float(chars[58:62], '<')
        except TypeError:
            pm10 = None

        return cls(cls.SOURCE, rec, pm1, pm2p5, pm10, period, bins, bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof)
