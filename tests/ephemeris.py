#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import math
import os
import platform
from functools import lru_cache
from pathlib import Path

import swisseph as swe


MANIFEST_PATH = Path(__file__).with_name('ephemeris-manifest.json')
ONE_SECOND_IN_JULIAN_DAYS = 1.0 / 86400.0
ANGLE_TOLERANCE_DEGREES = 0.1 / 3600.0
RATIO_TOLERANCE = 2e-7
SMALL_VALUE_ABS_TOLERANCE = 1e-12
# Numerical speed derivatives vary by architecture. Each baseline below is
# reproduced against the same-platform swetest build by verify_swetest.py.
FIXED_STAR_SPEED_BASELINES = {
    ('darwin', 'arm64', 'Sirius'): (
        7.988858696370463e-05,
        -4.909968457116758e-05,
        -0.004058783747934266,
    ),
    ('darwin', 'arm64', 'Polaris'): (
        -0.005939293194827129,
        7.651886467570471e-05,
        -0.009287547437675991,
    ),
    ('darwin', 'x86_64', 'Sirius'): (
        7.988566891758197e-05,
        -4.910121265786019e-05,
        -0.003998473811499148,
    ),
    ('darwin', 'x86_64', 'Polaris'): (
        -0.00593928660366758,
        7.651874559559961e-05,
        -0.007759332946554232,
    ),
    ('linux', 'aarch64', 'Sirius'): (
        7.988858696370463e-05,
        -4.909968457116758e-05,
        -0.004058783747934266,
    ),
    ('linux', 'aarch64', 'Polaris'): (
        -0.005939289575559061,
        7.65188291177801e-05,
        -0.009250077164182809,
    ),
    ('linux', 'x86_64', 'Sirius'): (
        7.988566891758197e-05,
        -4.910121265786019e-05,
        -0.003998473811499148,
    ),
    ('linux', 'x86_64', 'Polaris'): (
        -0.005939290187488762,
        7.651878270778714e-05,
        -0.007722300859817233,
    ),
}


def _sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest():
    with MANIFEST_PATH.open(encoding='utf-8') as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def verified_ephemeris_path():
    value = os.environ.get('SE_EPHE_PATH')
    if not value:
        raise RuntimeError(
            'SE_EPHE_PATH must point to the pinned test fixture; '
            'run tests/fetch_ephemeris.py first'
        )

    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise RuntimeError('SE_EPHE_PATH is not a directory: {0}'.format(path))

    manifest = load_manifest()
    for item in manifest['files']:
        fixture = path / item['name']
        if not fixture.is_file():
            raise RuntimeError('missing pinned ephemeris file: {0}'.format(fixture))
        if fixture.stat().st_size != item['size']:
            raise RuntimeError(
                'size mismatch for pinned ephemeris file: {0}'.format(fixture)
            )
        if _sha256(fixture) != item['sha256']:
            raise RuntimeError(
                'checksum mismatch for pinned ephemeris file: {0}'.format(fixture)
            )
    return str(path)


def set_test_ephe_path():
    path = verified_ephemeris_path()
    swe.close()
    swe.set_ephe_path(path)
    return path


def assert_close(test_case, actual, expected, abs_tol, rel_tol=0.0, label=None):
    if not math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol):
        test_case.fail(
            '{0}: {1!r} != {2!r} (abs_tol={3!r}, rel_tol={4!r})'.format(
                label or 'value', actual, expected, abs_tol, rel_tol
            )
        )


def assert_julian_days(test_case, actual, expected):
    for index, (actual_value, expected_value) in enumerate(zip(actual, expected)):
        if expected_value == 0.0:
            test_case.assertEqual(actual_value, expected_value)
        else:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                ONE_SECOND_IN_JULIAN_DAYS,
                label='Julian day {0}'.format(index),
            )


def assert_geopos(test_case, actual, expected):
    for index, (actual_value, expected_value) in enumerate(zip(actual, expected)):
        if index < 2:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                ANGLE_TOLERANCE_DEGREES,
                label='geographic angle {0}'.format(index),
            )
        else:
            test_case.assertEqual(actual_value, expected_value)


def assert_position_and_speed(test_case, actual, expected_position, star):
    for index, (actual_value, expected_value) in enumerate(zip(actual, expected_position)):
        if index < 2:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                ANGLE_TOLERANCE_DEGREES,
                label='position angle {0}'.format(index),
            )
        else:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                1e-9,
                rel_tol=1e-12,
                label='distance',
            )
    platform_key = (platform.system().lower(), platform.machine().lower(), star)
    expected_speed = FIXED_STAR_SPEED_BASELINES.get(platform_key)
    if expected_speed is None:
        for index, actual_value in enumerate(actual[3:]):
            test_case.assertTrue(
                math.isfinite(actual_value),
                'speed {0} is not finite'.format(index),
            )
            test_case.assertNotEqual(actual_value, 0.0)
        return

    for index, (actual_value, expected_value) in enumerate(
        zip(actual[3:], expected_speed)
    ):
        assert_close(
            test_case,
            actual_value,
            expected_value,
            SMALL_VALUE_ABS_TOLERANCE,
            rel_tol=1e-7,
            label='speed {0}'.format(index),
        )


def assert_eclipse_attributes(test_case, actual, expected):
    ratio_indexes = {0, 1, 2, 8}
    angle_indexes = {4, 5, 6}
    for index, (actual_value, expected_value) in enumerate(zip(actual, expected)):
        if index in ratio_indexes:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                RATIO_TOLERANCE,
                rel_tol=RATIO_TOLERANCE,
                label='eclipse ratio {0}'.format(index),
            )
        elif index == 3:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                0.001,
                label='shadow diameter (km)',
            )
        elif index in angle_indexes:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                ANGLE_TOLERANCE_DEGREES,
                label='eclipse angle {0}'.format(index),
            )
        elif index == 7:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                SMALL_VALUE_ABS_TOLERANCE,
                rel_tol=5e-3,
                label='separation angle',
            )
        else:
            test_case.assertEqual(actual_value, expected_value)


def assert_lunar_eclipse_attributes(test_case, actual, expected):
    ratio_indexes = {0, 1, 7, 8}
    angle_indexes = {4, 5, 6}
    for index, (actual_value, expected_value) in enumerate(zip(actual, expected)):
        if index in ratio_indexes:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                RATIO_TOLERANCE,
                rel_tol=RATIO_TOLERANCE,
                label='lunar eclipse value {0}'.format(index),
            )
        elif index in angle_indexes:
            assert_close(
                test_case,
                actual_value,
                expected_value,
                ANGLE_TOLERANCE_DEGREES,
                label='lunar eclipse angle {0}'.format(index),
            )
        else:
            test_case.assertEqual(actual_value, expected_value)
