# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the AAS WorldWide Telescope project
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
ImageSet
'''.split()

import math
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
    rotation_deg = 0.0
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
        imgset.set('Rotation', str(self.rotation_deg))
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


    def set_position_from_wcs(self, headers, width, height, place=None, fov_factor=1.7):
        """Set the positional information associated with this imageset to match a set
        of WCS headers.

        """
        # Figure out the stuff we need from the headers.

        ra_deg = headers['CRVAL1']
        dec_deg = headers['CRVAL2']
        crpix_x = headers['CRPIX1'] - 1
        crpix_y = headers['CRPIX2'] - 1

        if 'PC1_1' in headers:
            scale_x = headers['CDELT1']
            scale_y = headers['CDELT2']
            pc1_1 = headers['PC1_1']
            pc2_2 = headers['PC2_2']
            pc1_2 = headers.get('PC1_2', 0.0)
            pc2_1 = headers.get('PC2_1', 0.0)

            if pc1_1 * pc2_2 - pc1_2 * pc2_1 < 0:
                pc_sign = -1
            else:
                pc_sign = 1

            rot_rad = math.atan2(-pc_sign * pc1_2, pc2_2)
        else:
            cd1_1 = headers['CD1_1']
            cd2_2 = headers['CD2_2']
            cd1_2 = headers.get('CD1_2', 0.0)
            cd2_1 = headers.get('CD2_1', 0.0)

            if cd1_1 * cd2_2 - cd1_2 * cd2_1 < 0:
                cd_sign = -1
            else:
                cd_sign = 1

            rot_rad = math.atan2(-cd_sign * cd1_2, cd2_2)
            scale_x = math.sqrt(cd1_1**2 + cd2_1**2) * cd_sign
            scale_y = math.sqrt(cd1_2**2 + cd2_2**2)

        center_crx = width // 2 - crpix_x
        center_cry = height // 2 - crpix_y

        # Now, assign the fields

        self.data_set_type = 'Sky'
        self.projection = 'SkyImage'
        self.width_factor = 1
        self.center_x = ra_deg
        self.center_y = dec_deg
        self.offset_x = center_crx * abs(scale_x)
        self.offset_y = center_cry * scale_y
        self.base_degrees_per_tile = scale_y
        self.rotation_deg = rot_rad * 180 / math.pi

        if place is not None:
            place.data_set_type = 'Sky'
            place.rotation_deg = self.rotation_deg
            place.ra_hr = ra_deg / 15.
            place.dec_deg = dec_deg
            # It is hardcoded that in sky mode, zoom_level = height of client FOV * 6.
            place.zoom_level = height * scale_y * fov_factor * 6
