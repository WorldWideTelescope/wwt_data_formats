# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import os.path
import shutil
import tempfile
import pytest

from .. import cli, filecabinet


@pytest.fixture
def tempdir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def test_cli(tempdir):
    "Simple smoke test to see if it runs at all."

    prev_dir = os.getcwd()

    try:
        os.chdir(tempdir)
        cli.entrypoint(['tree', 'fetch',
            'https://web.wwtassets.org/engine/assets/builtin-image-sets.wtml'])
        cli.entrypoint(['tree', 'summarize'])
        cli.entrypoint(['tree', 'print-image-urls'])
        cli.entrypoint(['tree', 'print-dem-urls'])
    finally:
        # Windows can't remove the temp tree unless we chdir out of it.
        os.chdir(prev_dir)
