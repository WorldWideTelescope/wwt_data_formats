# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the AAS WorldWide Telescope project
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
ImageSet
'''.split()

from xml.etree import ElementTree as etree


class ImageSet(object):
    """A set of images."""

    data_set_type = 'Earth'
    name = ''
    url = ''
    width_factor = 2
    base_tile_level = 0
    tile_levels = 0
    base_degrees_per_tile = 0
    file_type = '.png'
    bottoms_up = False
    projection = 'Tan'
    center_x = 0.0
    center_y = 0.0
    offset_x = 0.0
    offset_y = 0.0
    rotation = 0.0
    band_pass = 'Visible'
    sparse = True
    credits = None
    credits_url = ''
    thumbnail_url = ''
    description = ''

    def to_xml(self):
        """Seralize this object to XML.

        Returns
        -------
        elem : xml.etree.ElementTree.Element
          An ``ImageSet`` XML element serializing the object.

        """
        imgset = etree.Element('ImageSet')
        imgset.set('Name', self.name)
        imgset.set('Url', self.url)
        imgset.set('WidthFactor', str(self.width_factor))
        imgset.set('BaseTileLevel', str(self.base_tile_level))
        imgset.set('TileLevels', str(self.tile_levels))
        imgset.set('BaseDegreesPerTile', str(self.base_degrees_per_tile))
        imgset.set('FileType', self.file_type)
        imgset.set('BottomsUp', str(self.bottoms_up))
        imgset.set('Projection', self.projection)
        imgset.set('CenterX', str(self.center_x))
        imgset.set('CenterY', str(self.center_y))
        imgset.set('OffsetX', str(self.offset_x))
        imgset.set('OffsetY', str(self.offset_y))
        imgset.set('Rotation', str(self.rotation))
        imgset.set('DataSetType', self.data_set_type)
        imgset.set('BandPass', self.band_pass)
        imgset.set('Sparse', str(self.sparse))

        credits = etree.SubElement(imgset, 'Credits')
        credits.text = self.credits

        credurl = etree.SubElement(imgset, 'CreditsUrl')
        credurl.text = self.credits_url

        thumburl = etree.SubElement(imgset, 'ThumbnailUrl')
        thumburl.text = self.thumbnail_url

        desc = etree.SubElement(imgset, 'Description')
        desc.text = self.description

        return imgset
