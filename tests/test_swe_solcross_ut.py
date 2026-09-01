#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ONE_SECOND_IN_JULIAN_DAYS, assert_close

class TestSweSolcrossUt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        x = swe.solcross_ut(30, 2455334.0, swe.FLG_SWIEPH)
        assert_close(self, x, 2455671.928764356, ONE_SECOND_IN_JULIAN_DAYS,
                     label='solar crossing Julian day')

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
