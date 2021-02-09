# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import os.path
import shutil
import tempfile
import pytest

from .. import cli, filecabinet
from . import work_in_tempdir


def test_writer():
    with pytest.raises(ValueError):
        fcw = filecabinet.FileCabinetWriter()
        fcw.add_file_with_data('bad-file-not-bytes', u'This is not bytes.')


def test_cli(work_in_tempdir):
    "Simple smoke test to see if it runs at all."

    with open('file1.txt', 'wt', encoding='utf8') as f:
        print('Hello world', file=f)

    cli.entrypoint(['cabinet', 'pack', 'cabinet.wwtl', 'file1.txt'])

    os.remove('file1.txt')
    cli.entrypoint(['cabinet', 'unpack', 'cabinet.wwtl'])


def test_pack_globs(work_in_tempdir):
    """
    This doesn't quite belong here -- test that we properly glob filenames when
    run through the shell. This is something to worry about on Windows, when
    running in the basic command prompt.
    """
    cli.GLOB_PATHS_INTERNALLY = True

    with open('file1.txt', 'wt', encoding='utf8') as f:
        print('Hello world', file=f)

    with open('file2.txt', 'wt', encoding='utf8') as f:
        print('Hello again', file=f)

    cli.entrypoint(['cabinet', 'pack', 'cabinet1.wwtl', 'file?.txt'])
    cli.entrypoint(['cabinet', 'pack', 'cabinet2.wwtl', '?ile*.txt'])

    with open('cabinet1.wwtl', 'rb') as f:
        data1 = f.read()

    with open('cabinet2.wwtl', 'rb') as f:
        data2 = f.read()

    assert data1 == data2

    # Globby paths yield OSError, "invalid argument", on Windows.
    with pytest.raises((FileNotFoundError, OSError)):
        cli.entrypoint(['cabinet', 'pack', 'cabinet1.wwtl', '*unmatched*.txt'])
