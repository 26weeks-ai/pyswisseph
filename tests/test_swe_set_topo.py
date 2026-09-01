#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ANGLE_TOLERANCE_DEGREES, assert_close

class TestSweSetTopo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        jd = swe.julday(2021, 8, 20, 12)
        xx, rflgs = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH)
        assert_close(self, xx[0], 301.86738437396843, ANGLE_TOLERANCE_DEGREES,
                     label='geocentric longitude')
        self.assertIsNone(swe.set_topo(121.5, 25.05, 9))
        xx, rflags = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH|swe.FLG_TOPOCTR)
        assert_close(self, xx[0], 302.20830488913884, ANGLE_TOLERANCE_DEGREES,
                     label='topocentric longitude')

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
