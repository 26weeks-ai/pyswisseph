#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ANGLE_TOLERANCE_DEGREES, assert_close

class TestSweCalcPctr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        xx, retflags = swe.calc_pctr(2452275.5, swe.MOON, swe.MERCURY, flags)
        self.assertIsInstance(xx, tuple)
        self.assertIsInstance(retflags, int)
        self.assertEqual(len(xx), 6)
        self.assertEqual(retflags, flags)
        self.assertEqual(retflags, 258)
        expected = (
            115.59455771820501,
            2.0541309912075656,
            1.232681040486576,
            1.5728585725088604,
            -0.050397212612787234,
            -0.01808367765116861,
        )
        for index in (0, 1):
            assert_close(self, xx[index], expected[index], ANGLE_TOLERANCE_DEGREES)
        assert_close(self, xx[2], expected[2], 1e-12, rel_tol=1e-10, label='distance')
        for index in (3, 4, 5):
            assert_close(self, xx[index], expected[index], 1e-12, rel_tol=1e-7,
                         label='speed {0}'.format(index - 3))

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
