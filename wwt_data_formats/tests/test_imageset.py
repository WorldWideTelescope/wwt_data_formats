# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2021 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import numpy as np
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
<ImageSet BandPass="Visible" BaseDegreesPerTile="4.870732233333334e-05"
          BaseTileLevel="0" BottomsUp="True" CenterX="83.633083"
          CenterY="22.0145" DataSetType="Sky" ElevationModel="False"
          FileType=".png" Generic="False" MeanRadius="0.0" MSRCommunityId="0"
          MSRComponentId="0" OffsetX="1503.3507831457316"
          OffsetY="1479.3005935660037" Permission="0" Projection="SkyImage"
          Rotation="-179.70963521481" Sparse="True" StockSet="False"
          TileLevels="0" WidthFactor="2">
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

    # Postprocess CD into PC/CDELT using the usual normalization

    det = wcs_roundtrip['CD1_1'] * wcs_roundtrip['CD2_2'] - wcs_roundtrip['CD1_2'] * wcs_roundtrip['CD2_1']
    if det < 0:
        cd_sign = -1
    else:
        cd_sign = 1

    wcs_roundtrip['CDELT1'] = np.sqrt(wcs_roundtrip['CD1_1']**2 + wcs_roundtrip['CD1_2']**2) * cd_sign
    wcs_roundtrip['CDELT2'] = np.sqrt(wcs_roundtrip['CD2_1']**2 + wcs_roundtrip['CD2_2']**2)
    wcs_roundtrip['PC1_1'] = wcs_roundtrip['CD1_1'] / wcs_roundtrip['CDELT1']
    wcs_roundtrip['PC1_2'] = wcs_roundtrip['CD1_2'] / wcs_roundtrip['CDELT1']
    wcs_roundtrip['PC2_1'] = wcs_roundtrip['CD2_1'] / wcs_roundtrip['CDELT2']
    wcs_roundtrip['PC2_2'] = wcs_roundtrip['CD2_2'] / wcs_roundtrip['CDELT2']

    for hn in 'CD1_1 CD1_2 CD2_1 CD2_2'.split():
        del wcs_roundtrip[hn]

    # OK, now we can compare again

    for kw in wcs_roundtrip.keys():
        expected = wcs_keywords[kw]
        observed = wcs_roundtrip[kw]

        if kw in ('CTYPE1', 'CTYPE2'):
            assert expected == observed
        else:
            nt.assert_almost_equal(expected, observed)


def test_wcs_ok_matrices():
    base_keywords = {
        'CTYPE1': 'RA---TAN',
        'CTYPE2': 'DEC--TAN',
        'CRVAL1': 0,
        'CRVAL2': 0,
        'CRPIX1': 0,
        'CRPIX2': 0,
    }

    case1 = {
        'CD1_1': -0.05,
        'CD1_2': -0.3,
        'CD2_1': -0.3,
        'CD2_2': 0.05,
    }

    case2 = {
        'CD1_1': -0.05,
        'CD1_2': -0.3,
        'CD2_1': 0.3,
        'CD2_2': -0.05,
    }

    for these_kws in (case1, case2):
        all_kws = dict(base_keywords)
        all_kws.update(these_kws)

        imgset = imageset.ImageSet()
        imgset.set_position_from_wcs(all_kws, 1000, 1000)
        roundtrip_kws = imgset.wcs_headers_from_position()

        # Postprocess if needed

        if 'CDELT1' in these_kws:
            det = roundtrip_kws['CD1_1'] * roundtrip_kws['CD2_2'] - roundtrip_kws['CD1_2'] * roundtrip_kws['CD2_1']
            if det < 0:
                cd_sign = -1
            else:
                cd_sign = 1

            roundtrip_kws['CDELT1'] = np.sqrt(roundtrip_kws['CD1_1']**2 + roundtrip_kws['CD1_2']**2) * cd_sign
            roundtrip_kws['CDELT2'] = np.sqrt(roundtrip_kws['CD2_1']**2 + roundtrip_kws['CD2_2']**2)
            roundtrip_kws['PC1_1'] = roundtrip_kws['CD1_1'] / roundtrip_kws['CDELT1']
            roundtrip_kws['PC1_2'] = roundtrip_kws['CD1_2'] / roundtrip_kws['CDELT1']
            roundtrip_kws['PC2_1'] = roundtrip_kws['CD2_1'] / roundtrip_kws['CDELT2']
            roundtrip_kws['PC2_2'] = roundtrip_kws['CD2_2'] / roundtrip_kws['CDELT2']

            for hn in 'CD1_1 CD1_2 CD2_1 CD2_2'.split():
                del roundtrip_kws[hn]

        # OK, now we can compare

        for kw, expected in these_kws.items():
            observed = roundtrip_kws[kw]
            nt.assert_almost_equal(expected, observed)


def test_wcs_bad_matrices():
    base_keywords = {
        'CTYPE1': 'RA---TAN',
        'CTYPE2': 'DEC--TAN',
        'CRVAL1': 0,
        'CRVAL2': 0,
        'CRPIX1': 0,
        'CRPIX2': 0,
    }

    case1 = {
        'CD1_1': 0.05,
        'CD1_2': 0.3,
        'CD2_1': 0.3,
        'CD2_2': 0.05,
    }

    case2 = {
        'CD1_1': -0.05,
        'CD1_2': -0.3,
        'CD2_1': -0.3,
        'CD2_2': -0.05,
    }

    case3 = {
        'CD1_1': -0.05,
        'CD1_2': -0.3,
        'CD2_1': 0.3,
        'CD2_2': 0.05,
    }

    case4 = {
        'CD1_1': -0.05,
        'CD1_2': 0.3,
        'CD2_1': -0.3,
        'CD2_2': 0.05,
    }

    for these_kws in (case1, case2, case3, case4):
        all_kws = dict(base_keywords)
        all_kws.update(these_kws)

        imgset = imageset.ImageSet()

        with pytest.raises(ValueError):
            imgset.set_position_from_wcs(all_kws, 1000, 1000)


def test_wcs_tiled_topdown():
    """
    If you're setting WCS for a tiled image, it must have negative (JPEG,
    top-down) parity -- bottoms-up tiled images won't render

    """
    keywords = {
        'CTYPE1': 'RA---TAN',
        'CTYPE2': 'DEC--TAN',
        'CRVAL1': 0,
        'CRVAL2': 0,
        'CRPIX1': 0,
        'CRPIX2': 0,
        'CD1_1': 0.05,
        'CD1_2': 0.3,
        'CD2_1': 0.3,
        'CD2_2': -0.05,
    }

    imgset = imageset.ImageSet()
    imgset.tile_levels = 5

    with pytest.raises(Exception):
        imgset.set_position_from_wcs(keywords, 1000, 1000)

    # flip parity, as far as CD is concerned ...
    keywords['CD2_1'] *= -1
    keywords['CD2_2'] *= -1
    # This should now work:
    imgset.set_position_from_wcs(keywords, 1000, 1000)


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
