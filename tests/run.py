#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from tests.ephemeris import verified_ephemeris_path


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            for test in flatten(item):
                yield test
        else:
            yield item


def main():
    parser = argparse.ArgumentParser(
        description='Run tests in a reproducibly randomized order'
    )
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--verbosity', type=int, default=2)
    args = parser.parse_args()

    verified_ephemeris_path()
    tests = list(flatten(unittest.defaultTestLoader.discover('tests')))
    random.Random(args.seed).shuffle(tests)
    print('test order seed: {0}'.format(args.seed))
    result = unittest.TextTestRunner(verbosity=args.verbosity).run(
        unittest.TestSuite(tests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
