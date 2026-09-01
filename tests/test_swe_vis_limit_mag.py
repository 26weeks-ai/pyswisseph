#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import swisseph as swe
import unittest

from tests.ephemeris import ANGLE_TOLERANCE_DEGREES, assert_close

class TestSweVisLimitMag(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        swe.set_ephe_path()

    def test_01(self):
        jd = 2452275.5
        geopos = (121.34, 43.57, 100)
        atmo = (0, 0, 0, 0)
        obs = (0, 0, 0, 0, 0, 0)
        obj = 'Venus'
        flags = swe.FLG_SWIEPH | swe.HELFLAG_OPTICAL_PARAMS
        res, dret = swe.vis_limit_mag(jd, geopos, atmo, obs, obj, flags)
        self.assertEqual(res, 0)
        self.assertEqual(len(dret), 10)
        expected = (-8.216269235697762, 5.416663786674341, 130.26229197547684,
                3.943499643265711, 127.36538540591431, 9.190665145103704,
                291.8595169945994, -3.912729321347505, 0.0, 0.0)
        assert_close(self, dret[0], expected[0], 1e-7, rel_tol=1e-7,
                     label='limiting magnitude')
        for index in range(1, 7):
            assert_close(self, dret[index], expected[index], ANGLE_TOLERANCE_DEGREES,
                         label='altitude/azimuth {0}'.format(index))
        assert_close(self, dret[7], expected[7], 1e-7, rel_tol=1e-7,
                     label='object magnitude')
        self.assertEqual(dret[8:], expected[8:])

if __name__ == '__main__':
    unittest.main()

# vi: sw=4 ts=4 et
