# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2022 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import numpy as np
import numpy.testing as nt
import pytest
from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import imageset, enums, stringify_xml_doc, write_xml_doc


def test_basic_xml():
    expected_str = """
<ImageSet
    BandPass="Gamma"
    BaseDegreesPerTile="0.1"
    BaseTileLevel="1"
    BottomsUp="True"
    CenterX="1.234"
    CenterY="-0.31415"
    DataSetType="Planet"
    ElevationModel="False"
    FileType=".PNG"
    Generic="False"
    Name="Test name"
    OffsetX="100.1"
    OffsetY="100.2"
    Projection="SkyImage"
    QuadTreeMap=""
    Rotation="5.4321"
    Sparse="False"
    StockSet="False"
    TileLevels="4"
    Url="http://example.org/{0}"
    WidthFactor="2"
>
    <Credits>Escaping &amp; Entities</Credits>
    <CreditsUrl>https://example.org/credits</CreditsUrl>
    <Description>Escaping &lt;entities&gt;</Description>
    <ThumbnailUrl>https://example.org/thumbnail.jpg</ThumbnailUrl>
</ImageSet>
"""
    expected_xml = etree.fromstring(expected_str)

    imgset = imageset.ImageSet()
    imgset.data_set_type = enums.DataSetType.PLANET
    imgset.name = "Test name"
    imgset.url = "http://example.org/{0}"
    imgset.width_factor = 2
    imgset.base_tile_level = 1
    imgset.tile_levels = 4
    imgset.base_degrees_per_tile = 0.1
    imgset.file_type = ".PNG"
    imgset.bottoms_up = True
    imgset.projection = enums.ProjectionType.SKY_IMAGE
    imgset.center_x = 1.234
    imgset.center_y = -0.31415
    imgset.offset_x = 100.1
    imgset.offset_y = 100.2
    imgset.rotation_deg = 5.4321
    imgset.band_pass = enums.Bandpass.GAMMA
    imgset.sparse = False
    imgset.credits = "Escaping & Entities"
    imgset.credits_url = "https://example.org/credits"
    imgset.thumbnail_url = "https://example.org/thumbnail.jpg"
    imgset.description = "Escaping <entities>"

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def _check_wcs_roundtrip(imgset, height, source_kws):
    roundtrip_kws = imgset.wcs_headers_from_position(height)

    # Postprocess if needed

    if "CDELT1" in source_kws:
        det = (
            roundtrip_kws["CD1_1"] * roundtrip_kws["CD2_2"]
            - roundtrip_kws["CD1_2"] * roundtrip_kws["CD2_1"]
        )
        if det < 0:
            cd_sign = -1
        else:
            cd_sign = 1

        roundtrip_kws["CDELT1"] = (
            np.sqrt(roundtrip_kws["CD1_1"] ** 2 + roundtrip_kws["CD1_2"] ** 2) * cd_sign
        )
        roundtrip_kws["CDELT2"] = np.sqrt(
            roundtrip_kws["CD2_1"] ** 2 + roundtrip_kws["CD2_2"] ** 2
        )
        roundtrip_kws["PC1_1"] = roundtrip_kws["CD1_1"] / roundtrip_kws["CDELT1"]
        roundtrip_kws["PC1_2"] = roundtrip_kws["CD1_2"] / roundtrip_kws["CDELT1"]
        roundtrip_kws["PC2_1"] = roundtrip_kws["CD2_1"] / roundtrip_kws["CDELT2"]
        roundtrip_kws["PC2_2"] = roundtrip_kws["CD2_2"] / roundtrip_kws["CDELT2"]

        for hn in "CD1_1 CD1_2 CD2_1 CD2_2".split():
            del roundtrip_kws[hn]

    # OK, now we can compare

    for kw, expected in source_kws.items():
        observed = roundtrip_kws[kw]

        if kw in ("CTYPE1", "CTYPE2"):
            assert observed == expected
        else:
            nt.assert_almost_equal(observed, expected)


def test_wcs_1():
    expected_str = """
<ImageSet
    BandPass="Visible"
    BaseDegreesPerTile="4.870732233333334e-05"
    BaseTileLevel="0"
    BottomsUp="True"
    CenterX="83.633083"
    CenterY="22.0145"
    DataSetType="Sky"
    ElevationModel="False"
    FileType=".png"
    Generic="False"
    Name=""
    OffsetX="1503.3507831457316"
    OffsetY="1520.6994064339963"
    Projection="SkyImage"
    QuadTreeMap=""
    Rotation="179.70963521481"
    Sparse="True"
    StockSet="False"
    TileLevels="0"
    Url=""
    WidthFactor="2"
>
    <ThumbnailUrl></ThumbnailUrl>
</ImageSet>
"""
    expected_xml = etree.fromstring(expected_str)

    wcs_keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 83.633083,
        "CRVAL2": 22.0145,
        "PC1_1": 0.9999871586199364,
        "PC1_2": 0.005067799840785529,
        "PC2_1": -0.005067799840785529,
        "PC2_2": 0.9999871586199364,
        "CRPIX1": 1503.8507831457316,
        "CRPIX2": 1479.8005935660037,
        "CDELT1": -4.870732233333334e-05,
        "CDELT2": 4.870732233333334e-05,
    }

    imgset = imageset.ImageSet()
    imgset.set_position_from_wcs(wcs_keywords, 3000, 3000)

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    _check_wcs_roundtrip(imgset, 3000, wcs_keywords)


def test_wcs_only_two_pc_values():
    expected_str = """
<ImageSet
    BandPass="Visible"
    BaseDegreesPerTile="0.003888888888889"
    BaseTileLevel="0"
    BottomsUp="False"
    CenterX="233.73705402943"
    CenterY="23.506972488486"
    DataSetType="Sky"
    ElevationModel="False"
    FileType=".fits"
    Generic="False"
    Name="herschel_spire_tiled"
    OffsetX="130.5"
    OffsetY="126.5"
    Projection="SkyImage"
    QuadTreeMap=""
    Rotation="-0"
    Sparse="True"
    StockSet="False"
    TileLevels="0"
    Url=""
    WidthFactor="2"
>
    <ThumbnailUrl></ThumbnailUrl>
</ImageSet>
"""
    expected_xml = etree.fromstring(expected_str)

    wcs_keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 233.73705402943,
        "CRVAL2": 23.506972488486,
        "PC1_1": -0.003888888888889,
        "PC2_2": -0.003888888888889,
        "CRPIX1": 131.0,
        "CRPIX2": 130.0,
        "CDELT1": 1.0,
        "CDELT2": 1.0,
    }

    imgset = imageset.ImageSet()
    imgset.file_type = ".fits"
    imgset.name = "herschel_spire_tiled"
    imgset.set_position_from_wcs(wcs_keywords, 256, 256)

    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)


def test_wcs_ok_matrices():
    base_keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 0,
        "CRVAL2": 0,
        "CRPIX1": 0,
        "CRPIX2": 0,
    }

    case1 = {
        "CD1_1": -0.05,
        "CD1_2": -0.3,
        "CD2_1": -0.3,
        "CD2_2": 0.05,
    }

    case2 = {
        "CD1_1": -0.05,
        "CD1_2": -0.3,
        "CD2_1": 0.3,
        "CD2_2": -0.05,
    }

    for these_kws in (case1, case2):
        all_kws = dict(base_keywords)
        all_kws.update(these_kws)

        imgset = imageset.ImageSet()
        imgset.set_position_from_wcs(all_kws, 1000, 1000)
        _check_wcs_roundtrip(imgset, 1000, these_kws)


def test_wcs_bad_matrices():
    base_keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 0,
        "CRVAL2": 0,
        "CRPIX1": 0,
        "CRPIX2": 0,
    }

    case1 = {
        "CD1_1": 0.05,
        "CD1_2": 0.3,
        "CD2_1": 0.3,
        "CD2_2": 0.05,
    }

    case2 = {
        "CD1_1": -0.05,
        "CD1_2": -0.3,
        "CD2_1": -0.3,
        "CD2_2": -0.05,
    }

    case3 = {
        "CD1_1": -0.05,
        "CD1_2": -0.3,
        "CD2_1": 0.3,
        "CD2_2": 0.05,
    }

    case4 = {
        "CD1_1": -0.05,
        "CD1_2": 0.3,
        "CD2_1": -0.3,
        "CD2_2": 0.05,
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
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 0,
        "CRVAL2": 0,
        "CRPIX1": 0,
        "CRPIX2": 0,
        "CD1_1": 0.05,
        "CD1_2": 0.3,
        "CD2_1": 0.3,
        "CD2_2": -0.05,
    }

    imgset = imageset.ImageSet()
    imgset.tile_levels = 5

    with pytest.raises(Exception):
        imgset.set_position_from_wcs(keywords, 1000, 1000)

    # flip parity, as far as CD is concerned ...
    keywords["CD2_1"] *= -1
    keywords["CD2_2"] *= -1
    # This should now work:
    imgset.set_position_from_wcs(keywords, 1000, 1000)


def test_wcs_45deg():
    """
    We had an issue with tolerance-checking with rotations near 145 degrees.
    Example: NOIRLab image `noao-abell39hotelling`.
    """

    keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 0,
        "CRVAL2": 0,
        "CRPIX1": 0,
        "CRPIX2": 0,
        "CD1_1": 0.00015024947791364,
        "CD1_2": 0.00015517263725712,
        "CD2_1": -0.00015521026392131,
        "CD2_2": 0.00015021305386212,
    }

    imgset = imageset.ImageSet()
    imgset.set_position_from_wcs(keywords, 1000, 1000)


def test_wcs_offsety():
    """
    This test case isn't materially different than some of the others, but you
    can check its performance empirically with the test image
    ``noao-02190_300x240.png`` stored in the ``tests`` directory. This image is
    a scaled-down version of the "Large JPEG" form of
    https://noirlab.edu/public/images/noao-02190/, which comes with embedded AVM
    information. Helpfully for us, this image has a large OffsetY and a
    perceptible rotation. The rescaled image has AVM too, so you can test this
    package's untiled, top-down WCS code as follows::

        import toasty.builder, toasty.pyramid, pyavm
        b = toasty.builder.Builder(toasty.pyramid.PyramidIO("."))
        width, height = 300, 240
        avm = pyavm.AVM.from_image("noao-02190_300x240.png")
        b.imgset.url = "./noao-02190_300x240.png"
        b.apply_avm_info(avm, width, height)
        b.write_index_rel_wtml()
        # then run: `wwtdatatool preview index_rel.wtml`

    If you preview the image based on the emitted WTML, it should line up well
    on the Rosette Nebula. There's a small horizontal scale distortion because
    the image has slightly non-square pixels, which WWT's data model can't
    capture. (The WCS headers below don't exactly match what comes out of pyAVM
    because they square up the pixels, so that we can test WCS roundtripping
    here too.)

    The above image is stored in the standard "top-down" parity. You can
    generate a parity-flipped image using PIL::

        from PIL import Image
        import numpy as np
        buf = np.asarray(Image.open("noao-02190_300x240.png"))
        Image.fromarray(buf[::-1]).save("noao-02190_300x240_botup.png")

    And you can test the untiled, bottoms-up WCS routines in this package with
    the following code. Importantly, the WCS that we get directly from (py)AVM
    assumes bottoms-up parity, even though the relevant images are top-down. So
    the AVM WCS from the top-down file is correct for the bottoms-up file! (In
    Toasty, ``Builder.apply_avm_info()`` parity-flips the AVM WCS before
    applying it.) Thus::

        # Continuing the prior example:
        botup_wcs = avm.to_wcs(target_shape=(width, height))
        b.imgset.url = "./noao-02190_300x240_botup.png"
        b.apply_wcs_info(botup_wcs, width, height)
        b.write_index_rel_wtml()

    Finally, you can test this package's *tiled*, top-down WCS code through the
    command line, with::

        toasty tile-study --avm noao-02190_300x240.png
        toasty cascade --start 1 .
        wwtdatatool preview index_rel.wtml

    And for tiled rendering, bottoms-up isn't allowed, so that's all of the
    possibilities. All three images should render in WWT identically.
    """

    # Untiled, top-down:

    expected_topdown_str = """
<ImageSet
    BandPass="Visible"
    BaseDegreesPerTile="0.008950062085625134"
    BaseTileLevel="0"
    BottomsUp="False"
    CenterX="97.99720145"
    CenterY="4.722029196"
    DataSetType="Sky"
    ElevationModel="False"
    FileType=".png"
    Generic="False"
    Name="noao-02190_300x240"
    OffsetX="163.6018453"
    OffsetY="93.40002848"
    Projection="SkyImage"
    QuadTreeMap=""
    Rotation="-1.2477001179999867"
    Sparse="True"
    StockSet="False"
    TileLevels="0"
    Url=""
    WidthFactor="2"
>
    <ThumbnailUrl></ThumbnailUrl>
</ImageSet>
"""
    expected_xml = etree.fromstring(expected_topdown_str)

    width, height = 300, 240
    topdown_wcs_keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 97.99720145,
        "CRVAL2": 4.722029196,
        "CD1_1": -0.008947940043224373,
        "CD1_2": 0.00019488540070081815,
        "CD2_1": -0.00019488540070081815,
        "CD2_2": -0.008947940043224373,
        "CRPIX1": 164.1018453,
        "CRPIX2": 147.09997152,
    }

    imgset = imageset.ImageSet()
    imgset.file_type = ".png"
    imgset.name = "noao-02190_300x240"
    imgset.set_position_from_wcs(topdown_wcs_keywords, width, height)
    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)
    _check_wcs_roundtrip(imgset, height, topdown_wcs_keywords)

    # Untiled, bottoms-up:

    expected_botup_str = """
<ImageSet
    BandPass="Visible"
    BaseDegreesPerTile="0.00895006208562516"
    BaseTileLevel="0"
    BottomsUp="True"
    CenterX="97.99720145"
    CenterY="4.722029196"
    DataSetType="Sky"
    ElevationModel="False"
    FileType=".png"
    Generic="False"
    Name="noao-02190_300x240_botup"
    OffsetX="163.6018453"
    OffsetY="146.59997152"
    Projection="SkyImage"
    QuadTreeMap=""
    Rotation="178.75229988200002"
    Sparse="True"
    StockSet="False"
    TileLevels="0"
    Url=""
    WidthFactor="2"
>
    <ThumbnailUrl></ThumbnailUrl>
</ImageSet>
"""
    expected_xml = etree.fromstring(expected_botup_str)

    botup_wcs_keywords = {
        "CTYPE1": "RA---TAN",
        "CTYPE2": "DEC--TAN",
        "CRVAL1": 97.99720145,
        "CRVAL2": 4.722029196,
        "CD1_1": -0.0089479400432244,
        "CD1_2": -0.00019488540070082,
        "CD2_1": -0.00019488540070081,
        "CD2_2": 0.0089479400432244,
        "CRPIX1": 164.1018453,
        "CRPIX2": 93.90002848,
    }

    imgset.name = "noao-02190_300x240_botup"
    imgset.set_position_from_wcs(botup_wcs_keywords, width, height)
    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)
    _check_wcs_roundtrip(imgset, height, botup_wcs_keywords)

    # Tiled (and therefore required to be top-down):

    expected_tiled_str = """
<ImageSet
    BandPass="Visible"
    BaseDegreesPerTile="4.582431787840068"
    BaseTileLevel="0"
    BottomsUp="False"
    CenterX="97.99720145"
    CenterY="4.722029196"
    DataSetType="Sky"
    ElevationModel="False"
    FileType=".png"
    Generic="False"
    Name="noao-02190_300x240_tiled"
    OffsetX="-0.12173735991406849"
    OffsetY="0.23807139657986032"
    Projection="Tan"
    QuadTreeMap=""
    Rotation="-1.2477001179999867"
    Sparse="True"
    StockSet="False"
    TileLevels="1"
    Url=""
    WidthFactor="2"
>
    <ThumbnailUrl></ThumbnailUrl>
</ImageSet>
"""
    expected_xml = etree.fromstring(expected_tiled_str)

    imgset.name = "noao-02190_300x240_tiled"
    imgset.tile_levels = 1
    imgset.set_position_from_wcs(topdown_wcs_keywords, width, height)
    observed_xml = imgset.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)
    # NB: can't currently roundtrip WCS for tiled images


def test_misc_ser():
    expected_str = """
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
"""
    expected_xml = etree.fromstring(expected_str)

    imgset = imageset.ImageSet()
    imgset.url = "http://example.com/unspecified"

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
    assert b"encoding='UTF-8'" in observed_bio.getvalue()


def test_windows_compat():
    """
    When processing the `imageset.xml` file, the classic Windows app requires
    that the following XML items are present:

    - BaseDegreesPerTile
    - BaseTileLevel
    - BottomsUp
    - CenterX
    - CenterY
    - FileType
    - Name
    - QuadTreeMap
    - Rotation
    - Sparse
    - ThumbnailUrl child element
    - TileLevels
    - Url

    Here we verify that these are included in the XML output even when given
    null-ish values. Note that while we could update the Windows app to be more
    forgiving, old versions of the app would remain stringent, and we don't want
    to break those.
    """
    imgset = imageset.ImageSet()
    imgset.base_degrees_per_tile = 0
    imgset.base_tile_level = 0
    imgset.bottoms_up = False
    imgset.center_x = 0
    imgset.center_y = 0
    imgset.file_type = ""
    imgset.name = ""
    imgset.quad_tree_map = ""
    imgset.rotation_deg = 0
    imgset.sparse = False
    imgset.thumbnail_url = ""
    imgset.tile_levels = 0
    imgset.url = ""

    observed_xml = imgset.to_xml()

    NEED_ATTRS = """
    BaseDegreesPerTile
    BaseTileLevel
    BottomsUp
    CenterX
    CenterY
    FileType
    Name
    QuadTreeMap
    Rotation
    Sparse
    TileLevels
    Url
    """.split()

    NEED_CHILDREN = ["ThumbnailUrl"]

    for attr in NEED_ATTRS:
        assert attr in observed_xml.attrib

    tags = frozenset(e.tag for e in observed_xml)

    for ctag in NEED_CHILDREN:
        assert ctag in tags
