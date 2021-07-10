"""
Created on 13 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.crc import modbus_crc
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Decode

from scs_core.particulate.opc_datum import OPCDatum

from scs_dfe.climate.sht31 import SHT31


# --------------------------------------------------------------------------------------------------------------------

class OPCN3Datum(OPCDatum):
    """
    classdocs
    """

    SOURCE =                    'N3'
    CHARS =                     86

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, chars):
        if len(chars) != cls.CHARS:
            raise ValueError(chars)

        # checksum...
        required = Decode.unsigned_int(chars[84:86], '<')
        actual = modbus_crc(chars[:84])

        if required != actual:
            raise ValueError("bad checksum: required: 0x%04x actual: 0x%04x" % (required, actual))

        # time...
        rec = LocalizedDatetime.now().utc()

        # bins...
        bins = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(0, 48, 2)]

        # bin MToFs...
        bin_1_mtof = chars[48]
        bin_3_mtof = chars[49]
        bin_5_mtof = chars[50]
        bin_7_mtof = chars[51]

        # period...
        raw_period = Decode.unsigned_int(chars[52:54], '<')
        period = round(float(raw_period) / 100.0, 3)

        # sample flow rate...
        int_sfr = Decode.unsigned_int(chars[54:56], '<')
        sfr = round(float(int_sfr) / 100.0, 2)

        # temperature & humidity
        raw_temp = Decode.unsigned_int(chars[56:58], '<')
        raw_humid = Decode.unsigned_int(chars[58:60], '<')

        sht = SHTDatum(SHT31.humid(raw_humid), SHT31.temp(raw_temp))

        # PMx...
        try:
            pm1 = Decode.float(chars[60:64], '<')
        except TypeError:
            pm1 = None

        try:
            pm2p5 = Decode.float(chars[64:68], '<')
        except TypeError:
            pm2p5 = None

        try:
            pm10 = Decode.float(chars[68:72], '<')
        except TypeError:
            pm10 = None

        return cls(cls.SOURCE, rec, pm1, pm2p5, pm10, period, bins,
                   bin_1_mtof, bin_3_mtof, bin_5_mtof, bin_7_mtof, sfr=sfr, sht=sht)
