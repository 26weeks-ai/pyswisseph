#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import (
    assert_eclipse_attributes,
    assert_geopos,
    assert_julian_days,
)

class TestSweSolEclipse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        jd = 2454466.5
        flags = swe.FLG_SWIEPH

        res, tret = swe.sol_eclipse_when_glob(jd, flags, 0)

        self.assertEqual(res, 9)
        self.assertEqual(len(tret), 10)
        expected = (2454503.6632118295, 2454503.6311451807,
                2454503.5686267945, 2454503.758220695,
                2454503.6388334082, 2454503.68782387,
                2454503.641705108, 2454503.6849778355, 0.0, 0.0)
        assert_julian_days(self, tret, expected)

        tjdut = tret[0]
        rflags, geopos, attr = swe.sol_eclipse_where(tjdut, flags)

        self.assertEqual(rflags, 9)
        self.assertEqual(len(geopos), 10)
        expected = (-150.26578636931097, -67.54726366387055,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_geopos(self, geopos, expected)

        self.assertEqual(len(attr), 20)
        expected = (0.9808845308425124, 0.9657677545807911,
                0.9327073557880233, 123.54229260739888,
                88.56601566180666, 16.228773015947755, 16.283977157036617,
                0.0010808703550863033, 0.9657677545807911,
                121.0, 60.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_eclipse_attributes(self, attr, expected)

        rflags, tret, attr = swe.sol_eclipse_when_loc(jd, geopos[:3], flags)

        self.assertEqual(rflags, 8072)
        self.assertEqual(len(tret), 10)
        expected = (2454503.6632903684, 2454503.6195803257,
                2454503.6625299426, 2454503.664052069, 2454503.705140943,
                0.0, 0.0, 0.0, 0.0, 0.0)
        assert_julian_days(self, tret, expected)

        self.assertEqual(len(attr), 20)
        expected = (0.9820490555662591, 0.9657656140089812,
                0.9327032212021444, 123.53919820241275,
                88.53997551948561, 16.21795602619367, 16.27319661698918,
                0.0004507358868249765, 0.9657656140089812,
                121.0, 60.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_eclipse_attributes(self, attr, expected)

        rflags, attr = swe.sol_eclipse_how(tjdut, geopos[:3], flags)

        self.assertEqual(rflags, 137)
        self.assertEqual(len(attr), 20)
        expected = (0.9808845308425124, 0.9657677545807911,
                0.9327073557880233, 123.54229260739888,
                88.56601566180666, 16.228773015947755, 16.283977157036617,
                0.0010808703550863033, 0.9657677545807911,
                121.0, 60.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert_eclipse_attributes(self, attr, expected)

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
