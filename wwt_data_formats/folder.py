# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the AAS WorldWide Telescope project
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
Folder
'''.split()

from xml.etree import ElementTree as etree


class Folder(object):
    """A grouping of WWT content assets.

    Children can be: places (aka "Items"), imagesets, linesets, tours,
    folders, or IThumbnail objects (to be explored).

    """
    children = None
    name = ''
    group = 'Explorer'
    url = None
    thumbnail = None
    browseable = True
    searchable = True
    type = ''
    sub_type = ''
    msr_community_id = 0
    msr_component_id = 0
    permission = 0

    # ItemsElementName ?

    def __init__(self):
        self.children = []

    def to_xml(self):
        """Seralize this object to XML.

        Returns
        -------
        elem : xml.etree.ElementTree.Element
          A ``Folder`` XML element serializing the object.

        """
        folder = etree.Element('Folder')
        folder.set('Name', self.name)
        folder.set('Group', self.group)
        if self.url is not None:
            folder.set('Url', self.url)
        if self.thumbnail is not None:
            folder.set('Thumbnail', self.thumbnail)
        folder.set('Browseable', str(self.browseable))
        folder.set('Searchable', str(self.searchable))
        folder.set('Type', self.type)
        folder.set('SubType', self.sub_type)

        for c in self.children:
            folder.append(c.to_xml())

        return folder
