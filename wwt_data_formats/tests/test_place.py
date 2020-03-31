# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import pytest
from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import enums, imageset, place


def test_basic_xml():
    expected_str = '''
<Place MSRCommunityId="0" MSRComponentId="0" Permission="0"
       Angle="0.0" AngularSize="0.0" DataSetType="Earth" Dec="0.0" Distance="0.0"
       DomeAlt="0.0" DomeAz="0.0" Lat="0.0" Lng="0.0" Magnitude="0.0"
       Opacity="100.0" RA="0.0" Rotation="0.0" ZoomLevel="0.0">
</Place>
'''
    expected_xml = etree.fromstring(expected_str)
    pl = place.Place()
    observed_xml = pl.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_xmeta():
    expected_str = '''
<Place MSRCommunityId="0" MSRComponentId="0" Permission="0"
       Angle="0.0" AngularSize="0.0" DataSetType="Earth" Dec="0.0" Distance="0.0"
       DomeAlt="0.0" DomeAz="0.0" Lat="0.0" Lng="0.0" Magnitude="0.0"
       Opacity="100.0" RA="0.0" Rotation="0.0" ZoomLevel="0.0" XExtra1="hello"
       XExtra2="1">
</Place>
'''
    expected_xml = etree.fromstring(expected_str)
    pl = place.Place()
    pl.xmeta.Extra1 = 'hello'
    pl.xmeta.Extra2 = 1
    observed_xml = pl.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_nesting():
    expected_str = '''
<Place MSRCommunityId="0" MSRComponentId="0" Permission="0"
       Angle="0.0" AngularSize="0.0" DataSetType="Earth" Dec="0.0" Distance="0.0"
       DomeAlt="0.0" DomeAz="0.0" Lat="0.0" Lng="0.0" Magnitude="0.0"
       Opacity="100.0" RA="0.0" Rotation="0.0" ZoomLevel="0.0">
  <BackgroundImageSet>
    <ImageSet MSRCommunityId="0" MSRComponentId="0" Permission="0"
              BandPass="Visible" BaseDegreesPerTile="0.0" BaseTileLevel="0"
              BottomsUp="False" CenterX="0.0" CenterY="0.0" DataSetType="Sky" ElevationModel="False"
              FileType=".png" Generic="False" MeanRadius="0.0" OffsetX="0.0" OffsetY="0.0" Projection="SkyImage"
              Rotation="0.0" Sparse="True" StockSet="False" TileLevels="0"
              Url="http://example.com/background" WidthFactor="2">
    </ImageSet>
  </BackgroundImageSet>
  <ForegroundImageSet>
    <ImageSet MSRCommunityId="0" MSRComponentId="0" Permission="0"
              BandPass="Visible" BaseDegreesPerTile="0.0" BaseTileLevel="0"
              BottomsUp="False" CenterX="0.0" CenterY="0.0" DataSetType="Sky" ElevationModel="False"
              FileType=".png" Generic="False" MeanRadius="0.0" OffsetX="0.0" OffsetY="0.0" Projection="SkyImage"
              Rotation="0.0" Sparse="True" StockSet="False" TileLevels="0"
              Url="http://example.com/foreground" WidthFactor="2">
    </ImageSet>
  </ForegroundImageSet>
  <ImageSet MSRCommunityId="0" MSRComponentId="0" Permission="0"
            BandPass="Visible" BaseDegreesPerTile="0.0" BaseTileLevel="0"
            BottomsUp="False" CenterX="0.0" CenterY="0.0" DataSetType="Sky" ElevationModel="False"
            FileType=".png" Generic="False" MeanRadius="0.0" OffsetX="0.0" OffsetY="0.0" Projection="SkyImage"
            Rotation="0.0" Sparse="True" StockSet="False" TileLevels="0"
            Url="http://example.com/unspecified" WidthFactor="2">
  </ImageSet>
</Place>
'''
    expected_xml = etree.fromstring(expected_str)
    pl = place.Place()
    pl.image_set = imageset.ImageSet()
    pl.image_set.url = 'http://example.com/unspecified'
    pl.foreground_image_set = imageset.ImageSet()
    pl.foreground_image_set.url = 'http://example.com/foreground'
    pl.background_image_set = imageset.ImageSet()
    pl.background_image_set.url = 'http://example.com/background'
    observed_xml = pl.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)
