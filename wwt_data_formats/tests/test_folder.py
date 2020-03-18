# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

import pytest
from xml.etree import ElementTree as etree

from . import assert_xml_trees_equal
from .. import folder, imageset, place


def test_basic_xml():
    expected_str = '''
<Folder Browseable="True" Group="Explorer" Searchable="True" Type="Sky" />
'''
    expected_xml = etree.fromstring(expected_str)
    f = folder.Folder()
    observed_xml = f.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    # At the moment we can't check that this object equals the one we
    # constructed programmatically, but at least we can test that the
    # deserialization code doesn't crash.
    f = folder.Folder.from_xml(expected_xml)


def test_children():
    expected_str = '''
<Folder Browseable="True" Group="Explorer" Searchable="True" Type="Sky">
  <Place Angle="0.0" AngularSize="0.0" DataSetType="Earth" Dec="0.0" Distance="0.0"
         DomeAlt="0.0" DomeAz="0.0" Lat="0.0" Lng="0.0" Magnitude="0.0"
         Opacity="100.0" RA="0.0" Rotation="0.0" ZoomLevel="0.0">
  </Place>
  <Place Angle="0.0" AngularSize="0.0" DataSetType="Earth" Dec="0.0" Distance="0.0"
         DomeAlt="0.0" DomeAz="0.0" Lat="0.0" Lng="0.0" Magnitude="0.0"
         Opacity="100.0" RA="0.0" Rotation="0.0" ZoomLevel="0.0">
  </Place>
</Folder>
'''
    expected_xml = etree.fromstring(expected_str)
    f = folder.Folder()
    f.children.append(place.Place())
    f.children.append(place.Place())
    observed_xml = f.to_xml()
    assert_xml_trees_equal(expected_xml, observed_xml)

    f = folder.Folder.from_xml(expected_xml)
