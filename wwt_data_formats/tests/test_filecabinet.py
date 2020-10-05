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


def test_writer():
    with pytest.raises(ValueError):
        fcw = filecabinet.FileCabinetWriter()
        fcw.add_file_with_data('bad-file-not-bytes', u'This is not bytes.')


def test_cli(tempdir):
    "Simple smoke test to see if it runs at all."

    prev_dir = os.getcwd()

    try:
        os.chdir(tempdir)

        with open('file1.txt', 'wt', encoding='utf8') as f:
            print('Hello world', file=f)

        cli.entrypoint(['cabinet', 'pack', 'cabinet.wwtl', 'file1.txt'])

        os.remove('file1.txt')
        cli.entrypoint(['cabinet', 'unpack', 'cabinet.wwtl'])
    finally:
        # Windows can't remove the temp tree unless we chdir out of it.
        os.chdir(prev_dir)