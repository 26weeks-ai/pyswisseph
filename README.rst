==========
Pyswisseph
==========

This is the Python extension to the Swiss Ephemeris by AstroDienst.

The Swiss Ephemeris is the de-facto standard library for astrological
calculations. Current Swiss Ephemeris planetary and lunar data files are based
upon NASA JPL DE441 and cover the time range 13201 BC to AD 17191.

Usage Example
=============

::

    >>> import swisseph as swe
    >>> # first set path to ephemeris files
    >>> swe.set_ephe_path('/usr/share/sweph/ephe')
    >>> # find time of next lunar eclipse
    >>> jd = swe.julday(2007, 3, 3) # julian day
    >>> res = swe.lun_eclipse_when(jd)
    >>> ecltime = swe.revjul(res[1][0])
    >>> print(ecltime)
    (2007, 3, 3, 23.347926892340183)
    >>> # get ecliptic position of asteroid 13681 "Monty Python"
    >>> jd = swe.julday(2008, 3, 21)
    >>> xx, rflags = swe.calc_ut(jd, swe.AST_OFFSET+13681)
    >>> # print longitude
    >>> print(xx[0])
    0.09843983166646618

Links
=====

:Pyswisseph docs:       https://astrorigin.com/pyswisseph
:Python Package Index:  https://pypi.org/project/pyswisseph
:AstroDienst:           https://www.astro.com/swisseph

Source code
===========

Clone the Github repository with command:

``git clone --recurse-submodules https://github.com/astrorigin/pyswisseph``

Licensing
=========

The Pyswisseph package adopts the GNU Affero General Public License version 3.
See the ``LICENSE.txt`` file.

The original swisseph library is distributed under a dual licensing system:
GNU Affero General Public License, or Swiss Ephemeris Professional License.
For more information, see file ``libswe/LICENSE``.

Test Suite
==========

The numerical tests use a checksum-pinned DE441 fixture. Download and verify it
with::

    python3 tests/fetch_ephemeris.py --destination .test-data/ephe

The fixture contains:

- ``seas_18.se1``
- ``sefstars.txt``
- ``semo_18.se1``
- ``sepl_18.se1``

The source revision and SHA-256 checksum for each file are recorded in
``tests/ephemeris-manifest.json``. The downloader uses immutable URLs and
refuses files whose size or checksum differs.

The path to the directory containing those files must be indicated in the
environment variable ``SE_EPHE_PATH``.

Run the suite in randomized order with a recorded seed::

    env SE_EPHE_PATH="$PWD/.test-data/ephe" python3 tests/run.py --seed 441

To reproduce the Sirius and Polaris speed baselines against the official
``swetest`` executable built from the bundled Swiss Ephemeris revision on the
same platform, run::

    make -C libswe swetest
    env SE_EPHE_PATH="$PWD/.test-data/ephe" \
      python3 tests/verify_swetest.py --swetest libswe/swetest

Credits
=======

Author: Stanislas Marquis <stan(at)astrorigin.com>

PyPI/CI: Jonathan de Jong <jonathan(at)automatia.nl>

..
