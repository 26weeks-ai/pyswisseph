#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from urllib.request import urlopen


MANIFEST_PATH = Path(__file__).with_name('ephemeris-manifest.json')


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='Download the pinned DE441 test fixture'
    )
    parser.add_argument('--destination', default='.test-data/ephe', type=Path)
    args = parser.parse_args()

    with MANIFEST_PATH.open(encoding='utf-8') as handle:
        manifest = json.load(handle)

    destination = args.destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    base_url = manifest['source']['base_url'].rstrip('/')

    for item in manifest['files']:
        target = destination / item['name']
        valid_target = (
            target.is_file()
            and target.stat().st_size == item['size']
            and sha256(target) == item['sha256']
        )
        if valid_target:
            print('verified {0}'.format(target))
            continue
        if target.exists():
            raise RuntimeError('refusing to overwrite invalid fixture: {0}'.format(target))

        descriptor, temporary_name = tempfile.mkstemp(
            prefix=item['name'] + '.', dir=str(destination)
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            url = '{0}/{1}'.format(base_url, item['name'])
            with urlopen(url, timeout=30) as response:
                with temporary.open('wb') as handle:
                    shutil.copyfileobj(response, handle)
            valid_download = (
                temporary.stat().st_size == item['size']
                and sha256(temporary) == item['sha256']
            )
            if not valid_download:
                raise RuntimeError(
                    'downloaded fixture did not match manifest: {0}'.format(
                        item['name']
                    )
                )
            temporary.replace(target)
            print('downloaded {0}'.format(target))
        finally:
            if temporary.exists():
                temporary.unlink()


if __name__ == '__main__':
    main()
