#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ONE_SECOND_IN_JULIAN_DAYS, assert_close

class TestSweGetOrbitalElements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        tjdet = 2452275.5
        pl = swe.MERCURY
        flags = swe.FLG_SWIEPH | swe.FLG_HELCTR
        elem = swe.get_orbital_elements(tjdet, pl, flags)
        self.assertEqual(len(elem), 50)
        results = (0.3870973116752384,
                0.20564082761390637,
                7.004832547718116,
                48.32860398797294,
                29.134013561486853,
                77.4626175494598,
                284.23849969043636,
                260.5580773512961,
                272.46706891532926,
                1.7011172398961207,
                0.2408502395882737,
                4.092360093937826,
                0.24085768950188863,
                -115.87662958397914,
                2452206.0441131364,
                0.30749430013522416,
                0.4667003232152527,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        for index, (actual, expected) in enumerate(zip(elem, results)):
            if expected == 0.0:
                self.assertEqual(actual, expected)
            elif index == 14:
                assert_close(self, actual, expected, ONE_SECOND_IN_JULIAN_DAYS,
                             label='perihelion Julian day')
            else:
                assert_close(self, actual, expected, 1e-10, rel_tol=1e-10,
                             label='orbital element {0}'.format(index))

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
