"""
Created on 14 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Decode
from scs_core.data.crc import modbus_crc

from scs_core.particulate.opc_datum import OPCDatum

from scs_dfe.climate.sht31 import SHT31


# --------------------------------------------------------------------------------------------------------------------

class OPCR1Datum(OPCDatum):
    """
    classdocs
    """

    SOURCE =                    'R1'
    CHARS =                     64

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, chars):
        if len(chars) != cls.CHARS:
            raise ValueError(chars)

        # checksum...
        actual = Decode.unsigned_int(chars[62:64], '<')
        required = modbus_crc(chars[:62])

        if required != actual:
            raise ValueError("bad checksum: required: 0x%04x actual: 0x%04x" % (required, actual))

        # time...
        rec = LocalizedDatetime.now().utc()

        # bins...
        bins = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(0, 32, 2)]

        # bin MToFs...
        bin_1_mtof = chars[32]
        bin_3_mtof = chars[33]
        bin_5_mtof = chars[34]
        bin_7_mtof = chars[35]

        # sample flow rate...
        sfr = Decode.float(chars[36:40], '<')

        # temperature & humidity
        raw_temp = Decode.unsigned_int(chars[40:42], '<')
        raw_humid = Decode.unsigned_int(chars[42:44], '<')

        sht = SHTDatum(SHT31.humid(raw_humid), SHT31.temp(raw_temp))

        # period...
        period = Decode.float(chars[44:48], '<')

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

        return cls(cls.SOURCE, rec, pm1, pm2p5, pm10, period, bins,
                   bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof, sfr=sfr, sht=sht)
