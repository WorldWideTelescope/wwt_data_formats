# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import pytest
from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import imageset


def test_basic_xml():
    expected_str = '''
<ImageSet BandPass="Gamma" BaseDegreesPerTile="0.1" BaseTileLevel="1"
          BottomsUp="True" CenterX="1.234" CenterY="-0.31415"
          DataSetType="Planet" FileType=".PNG" Name="Test name"
          OffsetX="100.1" OffsetY="100.2" Projection="SkyImage"
          Rotation="5.4321" Sparse="False" TileLevels="4"
          Url="http://example.org/{0}" WidthFactor="2">
  <Credits>Escaping &amp; Entities</Credits>
  <CreditsUrl>https://example.org/credits</CreditsUrl>
  <ThumbnailUrl>https://example.org/thumbnail.jpg</ThumbnailUrl>
  <Description>Escaping &lt;entities&gt;</Description>
</ImageSet>
'''
    expected_xml = etree.fromstring(expected_str)

    imgset = imageset.ImageSet()
    imgset.data_set_type = 'Planet'
    imgset.name = 'Test name'
    imgset.url = 'http://example.org/{0}'
    imgset.width_factor = 2
    imgset.base_tile_level = 1
    imgset.tile_levels = 4
    imgset.base_degrees_per_tile = 0.1
    imgset.file_type = '.PNG'
    imgset.bottoms_up = True
    imgset.projection = 'SkyImage'
    imgset.center_x = 1.234
    imgset.center_y = -0.31415
    imgset.offset_x = 100.1
    imgset.offset_y = 100.2
    imgset.rotation_deg = 5.4321
    imgset.band_pass = 'Gamma'
    imgset.sparse = False
    imgset.credits = 'Escaping & Entities'
    imgset.credits_url = 'https://example.org/credits'
    imgset.thumbnail_url = 'https://example.org/thumbnail.jpg'
    imgset.description = 'Escaping <entities>'

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)
