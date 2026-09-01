#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import math
import os
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

import swisseph as swe

from tests.ephemeris import set_test_ephe_path


def swetest_values(binary, ephemeris, extra_arguments):
    command = [
        str(binary),
        '-bj2452275.5',
        '-pf',
        '-eswe',
        '-head',
        '-fPlbrSS',
        '-g,',
        '-ep',
    ] + extra_arguments
    environment = os.environ.copy()
    environment['SE_EPHE_PATH'] = ephemeris
    output = subprocess.check_output(
        command,
        env=environment,
        universal_newlines=True,
    )
    numeric_output = output.strip().splitlines()[-1].split(',', 2)[2]
    row = next(csv.reader([numeric_output]))
    return tuple(float(row[index]) for index in (0, 1, 2, 4, 5, 6))


def assert_same(case, python_values, reference_values):
    absolute_tolerances = (1e-10, 1e-10, 1e-9, 5e-10, 5e-10, 1e-12)
    for index, (actual, reference) in enumerate(zip(python_values, reference_values)):
        if not math.isclose(
            actual,
            reference,
            rel_tol=1e-12,
            abs_tol=absolute_tolerances[index],
        ):
            raise AssertionError(
                '{0} component {1}: Python {2!r}, swetest {3!r}'.format(
                    case, index, actual, reference
                )
            )


def main():
    parser = argparse.ArgumentParser(
        description='Verify fixed-star baselines against swetest'
    )
    parser.add_argument('--swetest', required=True, type=Path)
    args = parser.parse_args()

    binary = args.swetest.expanduser().resolve()
    if not binary.is_file():
        raise RuntimeError('swetest executable not found: {0}'.format(binary))
    ephemeris = set_test_ephe_path()
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    equatorial_flags = flags | swe.FLG_EQUATORIAL
    cases = (
        (
            'fixstar Sirius',
            swe.fixstar('Sirius', 2452275.5, flags)[0],
            ['-xfSirius', '-speed'],
        ),
        (
            'fixstar2 Sirius',
            swe.fixstar2('Sirius', 2452275.5, flags)[0],
            ['-xfSirius', '-speed', '-swefixstar2'],
        ),
        (
            'fixstar_ut Polaris',
            swe.fixstar_ut('Polaris', 2452275.5, equatorial_flags)[0],
            ['-ut', '-xfPolaris', '-i2306'],
        ),
        (
            'fixstar2_ut Polaris',
            swe.fixstar2_ut('Polaris', 2452275.5, equatorial_flags)[0],
            ['-ut', '-xfPolaris', '-i2306', '-swefixstar2'],
        ),
    )
    for name, python_values, arguments in cases:
        reference_values = swetest_values(binary, ephemeris, arguments)
        assert_same(name, python_values, reference_values)
        print('verified {0}'.format(name))


if __name__ == '__main__':
    main()
