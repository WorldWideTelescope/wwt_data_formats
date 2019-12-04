# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import pytest

from .. import filecabinet


def test_writer():
    with pytest.raises(ValueError):
        fcw = filecabinet.FileCabinetWriter()
        fcw.add_file_with_data('bad-file-not-bytes', u'This is not bytes.')
