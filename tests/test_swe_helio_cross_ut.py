#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ONE_SECOND_IN_JULIAN_DAYS, assert_close

class TestSweHelioCrossUt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        pl = swe.SATURN
        jdx = swe.helio_cross_ut(pl, 30, 2455334.0, swe.FLG_SWIEPH, False)
        assert_close(self, jdx, 2461855.379537281, ONE_SECOND_IN_JULIAN_DAYS,
                     label='heliocentric crossing Julian day')

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
