#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import assert_position_and_speed

class TestSweFixstar2Ut(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL
        xx, retnam, retflags = swe.fixstar2_ut('Polaris', 2452275.5, flags)
        self.assertIsInstance(xx, tuple)
        self.assertEqual(len(xx), 6)
        expected = (
            38.64742459831258,
            89.2764693605161,
            27356067.78375791,
        )
        assert_position_and_speed(self, xx, expected, 'Polaris')
        self.assertEqual(retnam, 'Polaris,alUMi')
        self.assertEqual(retflags, 2306)
        self.assertEqual(retflags, flags)

    def test_notfound(self):
        with self.assertRaises(swe.Error):
            xx, retnam, retflags = swe.fixstar2_ut('xyz7', 2452275.5)

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
