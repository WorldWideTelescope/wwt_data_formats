# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import pytest

from . import assert_xml_trees_equal, test_path
from .. import layers


def test_read_imageset():
    lcr = layers.LayerContainerReader.from_file(test_path('imagesetlayer.wwtl'))
    assert len(lcr.layers) == 1
    assert lcr.layers[0].image_set.file_type == '.tif'

    imgdata = lcr.read_layer_file(lcr.layers[0], lcr.layers[0].extension)
    assert len(imgdata) == 13224

    lcr.close()
