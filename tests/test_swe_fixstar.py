#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import assert_position_and_speed

class TestSweFixstar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        xx, retnam, retflags = swe.fixstar('Sirius', 2452275.5, flags)
        self.assertIsInstance(xx, tuple)
        self.assertEqual(len(xx), 6)
        expected = (
            104.11214970763878,
            -39.60552633160895,
            543929.8571831493,
        )
        assert_position_and_speed(self, xx, expected, 'Sirius')
        self.assertEqual(retnam, 'Sirius,alCMa')
        self.assertEqual(retflags, 258)
        self.assertEqual(retflags, flags)

    def test_notfound(self):
        with self.assertRaises(swe.Error):
            xx, retnam, retflags = swe.fixstar('xyz7', 2452275.5)

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
