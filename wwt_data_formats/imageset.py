# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .NET Foundation
# Licensed under the MIT License.

"""An image, possibly tiled, for display in WWT.

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
ImageSet
'''.split()

import math
from xml.etree import ElementTree as etree


class ImageSet(object):
    """A set of images."""

    data_set_type = 'Sky'
    """The renderer mode to which these data apply.

    Possible values are ``"Earth"``, ``"Planet"``, ``"Sky"``, ``"Panorama"``,
    ``"SolarSystem"``, and ``"Sandbox"``.

    """
    name = ''
    """A name used to refer to this imageset.

    Various parts of the WWT internals reference imagesets by this name, so
    it should be distinctive.

    """
    url = ''
    """The URL of the image data.

    Either a URL or a URL template. TODO: details

    """
    width_factor = 2
    """This is a legacy parameter. Leave it at 2."""

    base_tile_level = 0
    """The level of the highest (coarsest-resolution) tiling available.

    This should be zero except for special circumstances.

    """
    tile_levels = 0
    """The number of levels of tiling.

    Should be zero for untiled images. An image with ``tile_levels = 1`` has been
    broken into four tiles, each 256x256 pixels. For ``tile_levels = 2``, there are
    sixteen tiles, and the padded height of the tiled area is ``256 * 2**2 = 1024``
    pixels. Image with dimensions of 2048 pixels or smaller do not need to be tiled,
    so if this parameter is nonzero it will usually be 4 or larger.

    """
    base_degrees_per_tile = 0
    """The angular scale of the image.

    For untiled images, should be the pixel scale: the numer of degrees per
    pixel in the vertical direction. Non-square pixels are not supported.

    For tiled images, this is the height of the image with its dimensions
    padded out to the next largest power of 2 for tiling purposes. If a square
    image is 1200 pixels tall and has a height of 0.016 deg, the padded height
    would be 2048 pixels and this parameter should be set to
    0.016 * 2048 / 1200 = 0.0273.

    """
    file_type = '.png'
    """The extension of the image file(s) in this set, including a leading period.

    """
    bottoms_up = False
    """TBD."""

    projection = 'Tan'
    """The type of projection used to place this image on the sky.

    For untiled images, this should be "SkyImage". For tiled images, it should
    be "Tan". The :meth:`set_position_from_wcs` method will set this value
    appropriately based on :attr:`tile_levels`.

    """
    center_x = 0.0
    """The horizontal location of the center of the image’s projection coordinate
    system.

    For sky images, this is a right ascension in degrees.

    """
    center_y = 0.0
    """The vertical location of the center of the image’s projection coordinate
    system.

    For sky images, this is a declination in degrees.

    """
    offset_x = 0.0
    """The horizontal positioning of the image relative to its projection
    coordinate system.

    For untiled sky images, the image is by default positioned such that its
    lower left lands at the center of the projection coordinate system (namely,
    ``center_x`` and ``center_y``). The offset is measured in pixels and moves
    the image leftwards. Therefore, ``offset_x = image_width / 2`` places the
    center of the image at ``center_x``. This parameter is therefore analogous
    to the WCS keyword ``CRVAL1``.

    For tiled sky images, the offset is measured in *degrees*, and a value of
    zero means that the *center* of the image lands at the center of the
    projection coordinate system.

    """
    offset_y = 0.0
    """The vertical positioning of the image relative to its projection
    coordinate system.

    For untiled sky images, the image is by default positioned such that its
    lower left lands at the center of the projection coordinate system (namely,
    ``center_x`` and ``center_y``). The offset is measured in pixels and moves
    the image downwards. Therefore, ``offset_y = image_height / 2`` places the
    center of the image at ``center_y``. This parameter is therefore analogous
    to the WCS keyword ``CRVAL2``.

    For tiled sky images, the offset is measured in *degrees*, and a value of
    zero means that the *center* of the image lands at the center of the
    projection coordinate system.

    """
    rotation_deg = 0.0
    """The rotation of image’s projection coordinate system, in degrees.

    For sky images, this is East from North, i.e. counterclockwise.

    """
    band_pass = 'Visible'
    """The bandpass of the image data."""

    sparse = True
    """TBD."""

    credits = None
    """Textual credits for the image originator."""

    credits_url = ''
    """A URL giving the source of the image or more information about its creation."""

    thumbnail_url = ''
    """A URL to a standard WWT thumbnail representation of this imageset."""

    description = ''
    """A textual description of the imagery."""

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

        Parameters
        ----------
        headers : :class:`~astropy.io.fits.Header` or string-keyed dict-like
          A set of FITS-like headers including WCS keywords such as ``CRVAL1``.
        width : positive integer
          The width of the image associated with the WCS, in pixels.
        height : positive integer
          The height of the image associated with the WCS, in pixels.
        place : optional :class:`~wwt_data_formats.place.Place`
          If specified, the centering and zoom level of the :class:`~wwt_data_formats.place.Place`
          object will be set to match the center and size of this image.
        fov_factor : optional float
          If *place* is provided, its zoom level will be set so that the
          angular height of the client viewport is this factor times the
          angular height of the image. The default is 1.7.

        Returns
        -------
        self
          For convenience in chaining function calls.

        Remarks
        -------

        Certain of the ImageSet parameters take on different meanings depending on
        whether the image in question is a tiled "study" or not. This method will alter
        its behavior depending on whether the :attr:`tile_levels` attribute is greater
        than zero. If you are computing coordinates for a tiled study, make sure to set
        this parameter *before* calling this function.

        For the time being, the WCS must be equatorial using the gnomonic
        (``TAN``) projection.

        Required keywords in *headers* are:

        - ``CTYPE1`` and ``CTYPE2``
        - ``CRVAL1`` and ``CRVAL2``
        - ``CRPIX1`` and ``CRPIX2``
        - Either:
          - ``CDELT1``, ``CDELT2``, ``PC1_1``, and ``PC1_2``; or
          - ``CD1_1``, ``CD2_2``

        If present ``PC1_2``, ``PC2_1``, ``CD1_2``, and/or ``CD2_1`` are used.
        If absent, they are assumed to be zero.

        """
        if headers['CTYPE1'] != 'RA---TAN' or headers['CTYPE2'] != 'DEC--TAN':
            raise ValueError('WCS coordinates must be in an equatorial/TAN projection')

        # Figure out the stuff we need from the headers.

        ra_deg = headers['CRVAL1']
        dec_deg = headers['CRVAL2']
        crpix_x = headers['CRPIX1'] - 1
        crpix_y = headers['CRPIX2'] - 1

        if 'CD1_1' in headers:
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
        else:
            scale_x = headers['CDELT1']
            scale_y = headers['CDELT2']
            pc1_1 = headers.get('PC1_1', 1.0)
            pc2_2 = headers.get('PC2_2', 1.0)
            pc1_2 = headers.get('PC1_2', 0.0)
            pc2_1 = headers.get('PC2_1', 0.0)

            if pc1_1 * pc2_2 - pc1_2 * pc2_1 < 0:
                pc_sign = -1
            else:
                pc_sign = 1

            rot_rad = math.atan2(-pc_sign * pc1_2, pc2_2)

        # This is our best effort to make sure that the view centers on the
        # center of the image.

        try:
            from astropy.wcs import WCS
        except:
            center_ra_deg = ra_deg
            center_dec_deg = dec_deg
        else:
            wcs = WCS(headers)
            center = wcs.pixel_to_world(height / 2, width / 2)
            center_ra_deg = center.ra.deg
            center_dec_deg = center.dec.deg

        # Now, assign the fields

        self.data_set_type = 'Sky'
        self.width_factor = 2
        self.center_x = ra_deg
        self.center_y = dec_deg
        self.rotation_deg = rot_rad * 180 / math.pi

        if self.tile_levels > 0:  # are we tiled?
            self.projection = 'Tan'
            self.offset_x = (width / 2 - crpix_x) * abs(scale_x)
            self.offset_y = (height / 2 - crpix_y) * scale_y
            self.base_degrees_per_tile = scale_y * 256 * 2**self.tile_levels
        else:
            self.projection = 'SkyImage'
            self.offset_x = crpix_x
            self.offset_y = crpix_y
            self.base_degrees_per_tile = scale_y

        if place is not None:
            place.data_set_type = 'Sky'
            place.rotation_deg = 0.  # I think this is better than propagating the image rotation?
            place.ra_hr = center_ra_deg / 15.
            place.dec_deg = center_dec_deg
            # It is hardcoded that in sky mode, zoom_level = height of client FOV * 6.
            place.zoom_level = height * scale_y * fov_factor * 6

        return self
