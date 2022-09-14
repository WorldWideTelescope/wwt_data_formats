# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2022 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from mock import Mock
import os.path
import pytest
from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal, tempdir, test_path, work_in_tempdir
from .. import cli, folder, imageset, place


BASIC_XML_STRING = """
<Folder Browseable="True" Group="Explorer" Searchable="True" />
"""

ROOT_XML_STRING = """
<Folder Browseable="True" Group="Explorer" Searchable="True" Type="Sky">
    <Folder Url="http://example.com/child1.wtml" />
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
</Folder>
"""

CHILD1_XML_STRING = """
<Folder Name="Child1" Browseable="True" Group="Explorer" Searchable="True" Type="Sky">
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
</Folder>
"""


def fake_request_session_send(request, **kwargs):
    rv = Mock()

    if request.url == "http://example.com/root.wtml":
        rv.text = ROOT_XML_STRING
    elif request.url == "http://example.com/child1.wtml":
        rv.text = CHILD1_XML_STRING
    else:
        raise Exception(
            f"unexpected URL to fake requests.Session.send(): {request.url}"
        )

    return rv


@pytest.fixture
def fake_requests(mocker):
    m = mocker.patch("requests.Session.send")
    m.side_effect = fake_request_session_send


def test_basic_xml():
    expected_xml = etree.fromstring(BASIC_XML_STRING)
    f = folder.Folder()
    observed_xml = f.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    # At the moment we can't check that this object equals the one we
    # constructed programmatically, but at least we can test that the
    # deserialization code doesn't crash.
    f = folder.Folder.from_xml(expected_xml)


def test_children():
    expected_str = """
<Folder Browseable="True" Group="Explorer" Searchable="True">
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
</Folder>
"""
    expected_xml = etree.fromstring(expected_str)
    f = folder.Folder()
    f.children.append(place.Place())
    f.children.append(place.Place())
    observed_xml = f.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    f = folder.Folder.from_xml(expected_xml)


def test_walk():
    f0 = folder.Folder()
    f1 = folder.Folder()
    pl0 = place.Place()
    pl1 = place.Place()
    is0 = imageset.ImageSet()

    f0.children = [pl0, f1]
    f1.children = [is0, pl1]

    expected = [
        (0, (), f0),
        (1, (0,), pl0),
        (1, (1,), f1),
        (2, (1, 0), is0),
        (2, (1, 1), pl1),
    ]

    observed = list(f0.walk(download=False))
    assert observed == expected


def test_from_url():
    "Note that this test hits the network."
    url = "http://www.worldwidetelescope.org/wwtweb/catalog.aspx?W=ExploreRoot"
    folder.Folder.from_url(url)  # just test that we don't crash


def test_fetch_tree(fake_requests, tempdir):
    "Simple smoke test to see whether it crashes."

    def on_fetch(url):
        pass

    folder.fetch_folder_tree("http://example.com/root.wtml", tempdir, on_fetch)

    for item in folder.walk_cached_folder_tree(tempdir):
        pass


def test_basic_url_mutation():
    f = folder.Folder()
    f.url = "../updir/somewhere.wtml"
    f.mutate_urls(folder.make_absolutizing_url_mutator("https://example.com/subdir/"))
    assert f.url == "https://example.com/updir/somewhere.wtml"

    from ..place import Place
    from ..imageset import ImageSet

    imgset = ImageSet()
    imgset.url = "image.jpg"
    p = Place()
    p.background_image_set = imgset
    f.children.append(p)
    f.mutate_urls(folder.make_absolutizing_url_mutator("https://example.com/subdir/"))

    assert f.url == "https://example.com/updir/somewhere.wtml"
    assert imgset.url == "https://example.com/subdir/image.jpg"


def test_wtml_report():
    """Dumb smoketest."""
    cli.entrypoint(["wtml", "report", test_path("test1_rel.wtml")])
    cli.entrypoint(["wtml", "report", test_path("report_rel.wtml")])


def test_wtml_rewrite_disk(work_in_tempdir):
    f = folder.Folder()
    f.url = "sub%20dir/image.jpg"

    with open("index_rel.wtml", "wt", encoding="utf8") as f_out:
        f.write_xml(f_out)

    cli.entrypoint(["wtml", "rewrite-disk", "index_rel.wtml", "index_disk.wtml"])

    f = folder.Folder.from_file("index_disk.wtml")
    # abspath('') is not necessarily equal to abspath(work_in_tempdir), due to
    # symlinks and Windows filename shorterning.
    assert f.url == os.path.join(os.path.abspath(""), "sub dir", "image.jpg")


def test_wtml_rewrite_urls(work_in_tempdir):
    f = folder.Folder()
    f.url = "../updir/somewhere.wtml"

    with open("index_rel.wtml", "wt", encoding="utf8") as f_out:
        f.write_xml(f_out)

    cli.entrypoint(
        [
            "wtml",
            "rewrite-urls",
            "index_rel.wtml",
            "https://example.com/subdir/",
            "index.wtml",
        ]
    )

    f = folder.Folder.from_file("index.wtml")
    assert f.url == "https://example.com/updir/somewhere.wtml"
