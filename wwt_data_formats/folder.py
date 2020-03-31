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
    """The URL at which the full contents of this folder can be downloaded in WTML
    format.

    """
    thumbnail = Unicode('').tag(xml=XmlSer.attr('Thumbnail'))
    browseable = Bool(True).tag(xml=XmlSer.attr('Browseable'))
    searchable = Bool(True).tag(xml=XmlSer.attr('Searchable'))
    type = UseEnum(
        FolderType,
        default_value = FolderType.SKY,
    ).tag(xml=XmlSer.attr('Type'))
    sub_type = Unicode('').tag(xml=XmlSer.attr('SubType'))
    msr_community_id = Int(0).tag(xml=XmlSer.attr('MSRCommunityId'))
    """The ID number of the WWT Community that this content came from."""

    msr_component_id = Int(0).tag(xml=XmlSer.attr('MSRComponentId'))
    """The ID number of this content item on the WWT Communities system."""

    permission = Int(0).tag(xml=XmlSer.attr('Permission'))
    "TBD."

    children = List(
        trait = Union([
            Instance('wwt_data_formats.folder.Folder', args=()),
            Instance('wwt_data_formats.place.Place', args=()),
            Instance('wwt_data_formats.imageset.ImageSet', args=()),
        ]),
        default_value = ()
    ).tag(xml=XmlSer.inner_list())

    def _tag_name(self):
        return 'Folder'

    def walk(self, download=False):
        yield (0, (), self)

        for index, child in enumerate(self.children):
            if isinstance(child, Folder):
                if not len(child.children) and child.url and download:
                    url = child.url
                    child = Folder.from_url(url)
                    child.url = url
                    self.children[index] = child

                for depth, path, subchild in child.walk(download=download):
                    yield (depth + 1, (index,) + path, subchild)
            else:
                yield (1, (index,), child)
