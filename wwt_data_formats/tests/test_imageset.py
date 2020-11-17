# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import numpy.testing as nt
import pytest
from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import imageset, enums, stringify_xml_doc, write_xml_doc


def test_basic_xml():
    expected_str = '''
<ImageSet MSRCommunityId="0" MSRComponentId="0" Permission="0"
          BandPass="Gamma" BaseDegreesPerTile="0.1" BaseTileLevel="1"
          BottomsUp="True" CenterX="1.234" CenterY="-0.31415"
          DataSetType="Planet" ElevationModel="False" FileType=".PNG" Generic="False"
          MeanRadius="0.0" Name="Test name"
          OffsetX="100.1" OffsetY="100.2" Projection="SkyImage"
          Rotation="5.4321" Sparse="False" StockSet="False" TileLevels="4"
          Url="http://example.org/{0}" WidthFactor="2">
  <Credits>Escaping &amp; Entities</Credits>
  <CreditsUrl>https://example.org/credits</CreditsUrl>
  <Description>Escaping &lt;entities&gt;</Description>
  <ThumbnailUrl>https://example.org/thumbnail.jpg</ThumbnailUrl>
</ImageSet>
'''
    expected_xml = etree.fromstring(expected_str)

    imgset = imageset.ImageSet()
    imgset.data_set_type = enums.DataSetType.PLANET
    imgset.name = 'Test name'
    imgset.url = 'http://example.org/{0}'
    imgset.width_factor = 2
    imgset.base_tile_level = 1
    imgset.tile_levels = 4
    imgset.base_degrees_per_tile = 0.1
    imgset.file_type = '.PNG'
    imgset.bottoms_up = True
    imgset.projection = enums.ProjectionType.SKY_IMAGE
    imgset.center_x = 1.234
    imgset.center_y = -0.31415
    imgset.offset_x = 100.1
    imgset.offset_y = 100.2
    imgset.rotation_deg = 5.4321
    imgset.band_pass = enums.Bandpass.GAMMA
    imgset.sparse = False
    imgset.credits = 'Escaping & Entities'
    imgset.credits_url = 'https://example.org/credits'
    imgset.thumbnail_url = 'https://example.org/thumbnail.jpg'
    imgset.description = 'Escaping <entities>'

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_wcs_1():
    expected_str = '''
<ImageSet MSRCommunityId="0" MSRComponentId="0" Permission="0"
          BandPass="Visible" BaseDegreesPerTile="4.870732233333334e-05"
          BaseTileLevel="0" BottomsUp="False" CenterX="83.633083" CenterY="22.0145"
          DataSetType="Sky" ElevationModel="False" FileType=".png" Generic="False"
          MeanRadius="0.0" OffsetX="1502.8507831457316" OffsetY="1478.8005935660037"
          Projection="SkyImage" Rotation="-0.29036478519000003" Sparse="True"
          StockSet="False" TileLevels="0" WidthFactor="2">
</ImageSet>
'''
    expected_xml = etree.fromstring(expected_str)

    wcs_keywords = {
        'CTYPE1': 'RA---TAN',
        'CTYPE2': 'DEC--TAN',
        'CRVAL1': 83.633083,
        'CRVAL2': 22.0145,
        'PC1_1': 0.9999871586199364,
        'PC1_2': 0.005067799840785529,
        'PC2_1': -0.005067799840785529,
        'PC2_2': 0.9999871586199364,
        'CRPIX1': 1503.8507831457316,
        'CRPIX2': 1479.8005935660037,
        'CDELT1': -4.870732233333334e-05,
        'CDELT2': 4.870732233333334e-05,
    }

    imgset = imageset.ImageSet()
    imgset.set_position_from_wcs(wcs_keywords, 3000, 3000)

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    wcs_roundtrip = imgset.wcs_headers_from_position()

    for kw in wcs_roundtrip.keys():
        expected = wcs_keywords[kw]
        observed = wcs_roundtrip[kw]

        if kw in ('CTYPE1', 'CTYPE2'):
            assert expected == observed
        else:
            nt.assert_almost_equal(expected, observed)


def test_misc_ser():
    expected_str = '''
<ImageSet BandPass="Visible" BaseDegreesPerTile="0.0" BaseTileLevel="0"
          BottomsUp="False" CenterX="0.0" CenterY="0.0" DataSetType="Sky" ElevationModel="False"
          FileType=".png" Generic="False" MeanRadius="0.0" MSRCommunityId="0" MSRComponentId="0"
          OffsetX="0.0" OffsetY="0.0" Permission="0" Projection="SkyImage"
          Rotation="0.0" Sparse="True" StockSet="False" TileLevels="0"
          Url="http://example.com/unspecified" WidthFactor="2" />
'''
    expected_xml = etree.fromstring(expected_str)

    imgset = imageset.ImageSet()
    imgset.url = 'http://example.com/unspecified'

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    expected_text = stringify_xml_doc(expected_xml)
    observed_text = imgset.to_xml_string()
    assert observed_text == expected_text

    from io import BytesIO

    expected_bio = BytesIO()
    observed_bio = BytesIO()
    write_xml_doc(expected_xml, dest_stream=expected_bio, dest_wants_bytes=True)
    imgset.write_xml(observed_bio, dest_wants_bytes=True)
    assert observed_bio.getvalue() == expected_bio.getvalue()
    assert b'encoding=\'UTF-8\'' in observed_bio.getvalue()
