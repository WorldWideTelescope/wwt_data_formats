# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import os.path

from .. import cli, folder
from . import test_path, work_in_tempdir


def test_merge_cli(work_in_tempdir):
    os.mkdir('subdir1')
    os.mkdir('subdir2')

    source = folder.Folder.from_file(test_path('test1_rel.wtml'))
    test1_path = os.path.join('subdir1', 'test1_rel.wtml')
    with open(test1_path, 'w') as f:
        source.write_xml(f)

    merge_path = os.path.join('subdir2', 'merged.wtml')

    cli.entrypoint(['wtml', 'merge', test1_path, merge_path])

    merged = folder.Folder.from_file(merge_path)

    assert len(merged.children) == 1
    assert merged.children[0].thumbnail == '../subdir1/thumb.jpg'
    assert merged.children[0].foreground_image_set.credits_url == 'https://www.spacetelescope.org/images/heic0707a/'
    assert merged.children[0].foreground_image_set.url == '../subdir1/L{1}X{2}Y{3}.png'
