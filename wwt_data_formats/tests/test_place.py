# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2022 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import imageset, place


def test_basic_xml():
    expected_str = """
<Place
    Angle="0"
    AngularSize="0"
    DataSetType="Earth"
    Lat="0"
    Lng="0"
    Magnitude="0"
    Opacity="100"
    Rotation="0"
    ZoomLevel="0"
/>
"""
    expected_xml = etree.fromstring(expected_str)
    pl = place.Place()
    observed_xml = pl.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_xmeta():
    expected_str = """
<Place
    Angle="0"
    AngularSize="0"
    DataSetType="Earth"
    Lat="0"
    Lng="0"
    Magnitude="0"
    Opacity="100"
    Rotation="0"
    ZoomLevel="0"
    XExtra1="hello"
    XExtra2="1"
/>
"""
    expected_xml = etree.fromstring(expected_str)
    pl = place.Place()
    pl.xmeta.Extra1 = "hello"
    pl.xmeta.Extra2 = 1
    observed_xml = pl.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_nesting():
    expected_str = """
<Place
    Angle="0"
    AngularSize="0"
    DataSetType="Earth"
    Lat="0"
    Lng="0"
    Magnitude="0"
    Opacity="100"
    Rotation="0"
    ZoomLevel="0"
>
    <BackgroundImageSet>
        <ImageSet
            BandPass="Visible"
            BaseDegreesPerTile="0"
            BaseTileLevel="0"
            BottomsUp="False"
            CenterX="0"
            CenterY="0"
            DataSetType="Sky"
            ElevationModel="False"
            FileType=".png"
            Generic="False"
            Name=""
            Projection="SkyImage"
            QuadTreeMap=""
            Rotation="0"
            Sparse="True"
            StockSet="False"
            TileLevels="0"
            Url="http://example.com/background"
            WidthFactor="2"
        >
            <ThumbnailUrl></ThumbnailUrl>
        </ImageSet>
    </BackgroundImageSet>
    <ForegroundImageSet>
        <ImageSet
            BandPass="Visible"
            BaseDegreesPerTile="0"
            BaseTileLevel="0"
            BottomsUp="False"
            CenterX="0"
            CenterY="0"
            DataSetType="Sky"
            ElevationModel="False"
            FileType=".png"
            Generic="False"
            Name=""
            Projection="SkyImage"
            QuadTreeMap=""
            Rotation="0"
            Sparse="True"
            StockSet="False"
            TileLevels="0"
            Url="http://example.com/foreground"
            WidthFactor="2"
        >
            <ThumbnailUrl></ThumbnailUrl>
        </ImageSet>
    </ForegroundImageSet>
    <ImageSet
        BandPass="Visible"
        BaseDegreesPerTile="0"
        BaseTileLevel="0"
        BottomsUp="False"
        CenterX="0"
        CenterY="0"
        DataSetType="Sky"
        ElevationModel="False"
        FileType=".png"
        Generic="False"
        Name=""
        Projection="SkyImage"
        QuadTreeMap=""
        Rotation="0"
        Sparse="True"
        StockSet="False"
        TileLevels="0"
        Url="http://example.com/unspecified"
        WidthFactor="2"
    >
        <ThumbnailUrl></ThumbnailUrl>
    </ImageSet>
</Place>
"""
    expected_xml = etree.fromstring(expected_str)
    pl = place.Place()
    pl.image_set = imageset.ImageSet()
    pl.image_set.url = "http://example.com/unspecified"
    pl.foreground_image_set = imageset.ImageSet()
    pl.foreground_image_set.url = "http://example.com/foreground"
    pl.background_image_set = imageset.ImageSet()
    pl.background_image_set.url = "http://example.com/background"
    observed_xml = pl.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)
