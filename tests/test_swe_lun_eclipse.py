#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import (
    assert_julian_days,
    assert_lunar_eclipse_attributes,
)

class TestSweLunEclipse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        jd = 2454466.5
        flags = swe.FLG_SWIEPH
        geopos = (12.1, 49.0, 330)

        rflags, tret = swe.lun_eclipse_when(jd, flags, 0)

        self.assertEqual(rflags, 4)
        self.assertEqual(len(tret), 10)
        expected = (2454517.643069022, 0.0, 2454517.5717233163,
                2454517.714418893, 2454517.6258037863, 2454517.6603508913,
                2454517.525389098, 2454517.7608554307, 0.0, 0.0)
        assert_julian_days(self, tret, expected)

        tjdut = tret[0]
        rflags, tret, attr = swe.lun_eclipse_when_loc(tjdut, geopos, flags)

        self.assertEqual(rflags, 29584)
        self.assertEqual(len(tret), 10)
        expected = (2454695.382051714, 0.0, 2454695.316710274,
                2454695.447390307, 0.0, 0.0, 2454695.267205502,
                2454695.49679755, 0.0, 0.0)
        assert_julian_days(self, tret, expected)

        self.assertEqual(len(attr), 20)
        expected = (0.807612712816962, 1.8366496745409226, 0.0, 0.0,
                326.9885781414507, 21.362587376008065, 21.402247975418415,
                0.530161025257712, 0.807612712816962, 138.0, 28.0, 28.0,
                28.0, 28.0, 28.0, 28.0, 28.0, 28.0, 28.0, 28.0)
        assert_lunar_eclipse_attributes(self, attr, expected)

        rflags, attr = swe.lun_eclipse_how(tjdut, geopos, flags)

        self.assertEqual(rflags, 4)
        self.assertEqual(len(attr), 20)
        expected = (1.1061093564527134, 2.145134328347761, 0.0, 0.0,
                73.82030732787894, 26.299295664076965, 26.330705411368193,
                0.38016254918883874, 1.1061093564527134, 133.0, 26.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_lunar_eclipse_attributes(self, attr, expected)

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
