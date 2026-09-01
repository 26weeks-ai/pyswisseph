#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import set_test_ephe_path

class TestSweGetTidAcc(unittest.TestCase):

    def tearDown(self):
        swe.close()

    def test_default_before_ephemeris_load(self):
        swe.close()
        self.assertEqual(swe.get_tid_acc(), -25.8)

    def test_de441_tidal_acceleration(self):
        set_test_ephe_path()
        swe.calc(2452275.5, swe.MOON, swe.FLG_SWIEPH)
        _, _, _, denum = swe.get_current_file_data(1)
        self.assertEqual(denum, 441)
        self.assertEqual(swe.get_tid_acc(), -25.936)

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
