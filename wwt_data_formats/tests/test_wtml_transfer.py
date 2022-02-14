# -*- mode: python; coding: utf-8 -*-
# Copyright 2021 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from .. import cli, enums, folder, imageset, place
from . import test_path, work_in_tempdir


def test_transfer_cli(work_in_tempdir):
    # Reference data

    iref = imageset.ImageSet()
    iref.name = "my imageset"
    iref.data_set_type = enums.DataSetType.SKY
    iref.url = "ref"
    iref.width_factor = 2
    iref.tile_levels = 5
    iref.base_degrees_per_tile = 1.7
    iref.projection = enums.ProjectionType.TAN
    iref.center_x = 11.11
    iref.center_y = 22.22
    iref.offset_x = 33.11
    iref.offset_y = 44.11
    iref.rotation_deg = 98.76

    pref = place.Place()
    pref.name = "my place"
    pref.data_set_type = enums.DataSetType.SKY
    pref.ra_hr = 12.34
    pref.dec_deg = -88.88
    pref.zoom_level = 17.02
    pref.rotation_deg = 45.0
    pref.description = "ref"
    pref.thumbnail = "ref"
    pref.foreground_image_set = iref

    fref = folder.Folder()
    fref.children.append(pref)

    with open("reference.wtml", "wt", encoding="utf8") as f:
        fref.write_xml(f)

    # "Updated data"

    iupd = imageset.ImageSet.from_text(iref.to_xml_string())
    # should change:
    iupd.base_degrees_per_tile = 0.0
    iupd.center_x = 0.0
    iupd.center_y = 0.0
    iupd.offset_x = 0.0
    iupd.offset_y = 0.0
    # should be preserved:
    iupd.url = "upd-url"
    iupd.dem_url = "upd-dem"
    iupd.mean_radius = 5555.5

    pupd = place.Place.from_text(pref.to_xml_string())
    pupd.foreground_image_set = iupd
    # should change:
    pupd.ra_hr = 0.0
    pupd.dec_deg = 0.0
    pupd.zoom_level = 0.0
    pupd.rotation_deg = 0.0
    # should be preserved:
    pupd.description = "upd-desc"
    pupd.thumbnail = "upd-th"

    fupd1 = folder.Folder()
    f2 = folder.Folder()
    fupd1.children.append(f2)
    f2.children.append(pupd)

    with open("update1.wtml", "wt", encoding="utf8") as f:
        fupd1.write_xml(f)

    fupd2 = folder.Folder()
    fupd2.children.append(iupd)

    with open("update2.wtml", "wt", encoding="utf8") as f:
        fupd2.write_xml(f)

    # Run the command

    cli.entrypoint(
        [
            "wtml",
            "transfer-astrometry",
            "reference.wtml",
            "update1.wtml",
            "update2.wtml",
        ]
    )

    # How did we do?

    iupd.base_degrees_per_tile = iref.base_degrees_per_tile
    iupd.center_x = iref.center_x
    iupd.center_y = iref.center_y
    iupd.offset_x = iref.offset_x
    iupd.offset_y = iref.offset_y

    pupd.ra_hr = pref.ra_hr
    pupd.dec_deg = pref.dec_deg
    pupd.zoom_level = pref.zoom_level
    pupd.rotation_deg = pref.rotation_deg

    u1 = folder.Folder.from_file("update1.wtml")
    assert fupd1.to_xml_string() == u1.to_xml_string()

    u2 = folder.Folder.from_file("update2.wtml")
    assert fupd2.to_xml_string() == u2.to_xml_string()
