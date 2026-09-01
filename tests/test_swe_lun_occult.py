#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import (
    assert_eclipse_attributes,
    assert_geopos,
    assert_julian_days,
)

class TestSweLunOccult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        jd = 2454466.5
        pl = swe.VENUS
        flags = swe.FLG_SWIEPH

        rflags, tret = swe.lun_occult_when_glob(jd, pl, flags, 0)

        self.assertEqual(rflags, 5)
        self.assertEqual(len(tret), 10)
        expected = (2454531.296945435, 2454531.3051413717,
                2454531.198629135, 2454531.3950790856,
                2454531.198885796, 2454531.394823484,
                2454531.220605363, 2454531.3731206455, 0.0, 0.0)
        assert_julian_days(self, tret, expected)

        tjdut = tret[0]
        rflags, geopos, attr = swe.lun_occult_where(tjdut, pl, flags)

        self.assertEqual(rflags, 5)
        self.assertEqual(len(geopos), 10)
        expected = (-132.44807418017055, -3.223940822842425, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0)
        assert_geopos(self, geopos, expected)

        self.assertEqual(len(attr), 20)
        expected = (86.75745367716024, 172.52668475305524,
                29765.456951880104, -3461.913794250017, 336.2071184236425,
                76.84479711667942, 76.84858771377847,
                1.8151476701449225e-05, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_eclipse_attributes(self, attr, expected)

        rflags, tret, attr = swe.lun_occult_when_loc(jd, pl, geopos[:3], flags)

        self.assertEqual(rflags, 32644)
        self.assertEqual(len(tret), 10)
        expected = (2454531.296943703, 2454531.2598328353,
                2454531.2602917543, 2454531.3328175787,
                2454531.333256723, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_julian_days(self, tret, expected)

        self.assertEqual(len(attr), 20)
        expected = (1.0, 172.52667692374098, 1.0, -3461.913793839377,
                336.2047193310712, 76.84454557620569, 76.84833624839384,
                1.4787793334711022e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0)
        assert_eclipse_attributes(self, attr, expected)

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
