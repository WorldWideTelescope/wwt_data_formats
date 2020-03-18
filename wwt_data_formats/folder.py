# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
Folder
'''.split()

from traitlets import Bool, Instance, Int, List, Unicode, Union, UseEnum

from . import LockedXmlTraits, XmlSer
from .enums import FolderType

class Folder(LockedXmlTraits):
    """A grouping of WWT content assets.

    Children can be: places (aka "Items"), imagesets, linesets, tours,
    folders, or IThumbnail objects (to be explored).

    """
    name = Unicode('').tag(xml=XmlSer.attr('Name'))
    group = Unicode('Explorer').tag(xml=XmlSer.attr('Group'))
    url = Unicode('').tag(xml=XmlSer.attr('Url'))
    thumbnail = Unicode('').tag(xml=XmlSer.attr('Thumbnail'))
    browseable = Bool(True).tag(xml=XmlSer.attr('Browseable'))
    searchable = Bool(True).tag(xml=XmlSer.attr('Searchable'))
    type = UseEnum(
        FolderType,
        default_value = FolderType.SKY,
    ).tag(xml=XmlSer.attr('Type'))
    sub_type = Unicode('').tag(xml=XmlSer.attr('SubType'))

    children = List(
        trait = Union([
            Instance('wwt_data_formats.folder.Folder', args=()),
            Instance('wwt_data_formats.place.Place', args=()),
            Instance('wwt_data_formats.imageset.ImageSet', args=()),
        ]),
        default_value = ()
    ).tag(xml=XmlSer.inner_list())

    # todo(?): msr_community_id
    # todo(?): msr_component_id
    # todo(?): permission

    def _tag_name(self):
        return 'Folder'
