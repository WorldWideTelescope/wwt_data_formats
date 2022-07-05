# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2022 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import imageset, place
from ..enums import Constellation, DataSetType


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


def test_constellations():
    SAMPLES = [
        (23.99, 90, Constellation.URSA_MINOR),
        (1.5, 82.5, Constellation.CEPHEUS),
        (20.5, 41.5, Constellation.CYGNUS),
        (17.0, -42.6, Constellation.SCORPIUS),
        (0, -90, Constellation.OCTANS),
        (6, -84.5, Constellation.MENSA),
        (14.57, -78.39, Constellation.APUS),
        (0.094, -80.079, Constellation.OCTANS),
        (0.188, -80.079, Constellation.HYDRUS),
        (3.294, -80.079, Constellation.HYDRUS),
        (3.388, -80.079, Constellation.MENSA),
        (7.435, -80.079, Constellation.MENSA),
        (7.529, -80.079, Constellation.CHAMAELEON),
        (13.835, -80.079, Constellation.CHAMAELEON),
        (13.929, -80.079, Constellation.APUS),
        (18.353, -80.079, Constellation.APUS),
        (18.447, -80.079, Constellation.OCTANS),
        (23.999, -80.079, Constellation.OCTANS),
    ]

    pl = place.Place()

    for ra_hr, dec_deg, expected in SAMPLES:
        pl.set_ra_dec(ra_hr, dec_deg)
        assert pl.constellation == expected


def test_update_constellation_semantics():
    pl = place.Place()
    pl.data_set_type = DataSetType.SKY
    pl.latitude = 1
    pl.longitude = 1
    pl.ra_hr = 0.012
    pl.dec_deg = 0.034
    pl.update_constellation()
    assert pl.latitude == 0
    assert pl.longitude == 0
    assert pl.ra_hr == 0.012
    assert pl.dec_deg == 0.034
    assert pl.constellation == Constellation.PISCES

    pl.data_set_type = DataSetType.PLANET
    pl.latitude = 12
    pl.longitude = 34
    pl.ra_hr = 1
    pl.dec_deg = 1
    pl.update_constellation()
    assert pl.latitude == 12
    assert pl.longitude == 34
    assert pl.ra_hr == 0
    assert pl.dec_deg == 0
    assert pl.constellation == Constellation.UNSPECIFIED
