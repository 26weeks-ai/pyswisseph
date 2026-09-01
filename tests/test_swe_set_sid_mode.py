#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ANGLE_TOLERANCE_DEGREES, assert_close

class TestSweSetSidMode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        jd = swe.julday(2021, 8, 20, 12)
        xx, rflags = swe.calc_ut(jd, swe.VENUS)
        assert_close(self, xx[0], 185.09289066160179, ANGLE_TOLERANCE_DEGREES,
                     label='tropical longitude')
        self.assertIsNone(swe.set_sid_mode(swe.SIDM_LAHIRI))
        xx, rflags = swe.calc_ut(jd, swe.VENUS, swe.FLG_SWIEPH|swe.FLG_SIDEREAL)
        assert_close(self, xx[0], 160.93755422246636, ANGLE_TOLERANCE_DEGREES,
                     label='sidereal longitude')

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
