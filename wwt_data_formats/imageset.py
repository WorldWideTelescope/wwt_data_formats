# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

"""An image, possibly tiled, for display in WWT.

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
ImageSet
'''.split()

import math
from traitlets import Bool, Float, Int, Unicode, UseEnum
from xml.etree import ElementTree as etree

from . import LockedXmlTraits, XmlSer
from .abcs import UrlContainer
from .enums import Bandpass, DataSetType, ProjectionType


class ImageSet(LockedXmlTraits, UrlContainer):
    """A set of images."""

    data_set_type = UseEnum(DataSetType, default_value=DataSetType.SKY).tag(xml=XmlSer.attr('DataSetType'))
    """The renderer mode to which these data apply.

    Possible values are ``"Earth"``, ``"Planet"``, ``"Sky"``, ``"Panorama"``,
    ``"SolarSystem"``, and ``"Sandbox"``.

    """
    reference_frame = Unicode('').tag(xml=XmlSer.attr('ReferenceFrame'))
    """TBD."""

    name = Unicode('').tag(xml=XmlSer.attr('Name'))
    """A name used to refer to this imageset.

    Various parts of the WWT internals reference imagesets by this name, so
    it should be distinctive.

    """
    url = Unicode('').tag(xml=XmlSer.attr('Url'))
    """The URL of the image data.

    Either a URL or a URL template. TODO: details

    """
    alt_url = Unicode('').tag(xml=XmlSer.attr('AltUrl'))
    """An alternative URL that provided the data.

    If provided and the Windows client attempts to load an imageset using this
    alternative URL, that imageset will be replaced by this one. This provides a
    mechanism for superseding old imagesets with improved versions.

    """
    dem_url = Unicode('').tag(xml=XmlSer.attr('DemUrl'))
    """The URL of the DEM data.

    Either a URL or a URL template. TODO: details

    """
    width_factor = Int(2).tag(xml=XmlSer.attr('WidthFactor'))
    """This is a legacy parameter. Leave it at 2."""

    base_tile_level = Int(0).tag(xml=XmlSer.attr('BaseTileLevel'))
    """The level of the highest (coarsest-resolution) tiling available.

    This should be zero except for special circumstances.

    """
    quad_tree_map = Unicode('').tag(xml=XmlSer.attr('QuadTreeMap'))
    """TBD."""

    tile_levels = Int(0).tag(xml=XmlSer.attr('TileLevels'))
    """The number of levels of tiling.

    Should be zero for untiled images. An image with ``tile_levels = 1`` has been
    broken into four tiles, each 256x256 pixels. For ``tile_levels = 2``, there are
    sixteen tiles, and the padded height of the tiled area is ``256 * 2**2 = 1024``
    pixels. Image with dimensions of 2048 pixels or smaller do not need to be tiled,
    so if this parameter is nonzero it will usually be 4 or larger.

    """
    base_degrees_per_tile = Float(0.0).tag(xml=XmlSer.attr('BaseDegreesPerTile'))
    """The angular scale of the image.

    For untiled images, should be the pixel scale: the number of degrees per
    pixel in the vertical direction. Non-square pixels are not supported.

    For tiled images, this is the height of the image with its dimensions
    padded out to the next largest power of 2 for tiling purposes. If a square
    image is 1200 pixels tall and has a height of 0.016 deg, the padded height
    would be 2048 pixels and this parameter should be set to
    0.016 * 2048 / 1200 = 0.0273.

    """
    file_type = Unicode('.png').tag(xml=XmlSer.attr('FileType'))
    """The extension of the image file(s) in this set, including a leading period.

    """
    bottoms_up = Bool(False).tag(xml=XmlSer.attr('BottomsUp'))
    """TBD."""

    projection = UseEnum(
        ProjectionType,
        default_value = ProjectionType.SKY_IMAGE
    ).tag(xml=XmlSer.attr('Projection'))
    """The type of projection used to place this image on the sky.

    For untiled images, this should be "SkyImage". For tiled images, it should
    be "Tan". The :meth:`set_position_from_wcs` method will set this value
    appropriately based on :attr:`tile_levels`.

    """
    center_x = Float(0.0).tag(xml=XmlSer.attr('CenterX'))
    """The horizontal location of the center of the image’s projection coordinate
    system.

    For sky images, this is a right ascension in degrees.

    """
    center_y = Float(0.0).tag(xml=XmlSer.attr('CenterY'))
    """The vertical location of the center of the image’s projection coordinate
    system.

    For sky images, this is a declination in degrees.

    """
    offset_x = Float(0.0).tag(xml=XmlSer.attr('OffsetX'))
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
    offset_y = Float(0.0).tag(xml=XmlSer.attr('OffsetY'))
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
    rotation_deg = Float(0.0).tag(xml=XmlSer.attr('Rotation'))
    """The rotation of image’s projection coordinate system, in degrees.

    For sky images, this is East from North, i.e. counterclockwise.

    """
    band_pass = UseEnum(
        Bandpass,
        default_value = Bandpass.VISIBLE
    ).tag(xml=XmlSer.attr('BandPass'))
    """The bandpass of the image data."""

    sparse = Bool(True).tag(xml=XmlSer.attr('Sparse'))
    """TBD."""

    elevation_model = Bool(False).tag(xml=XmlSer.attr('ElevationModel'))
    """TBD."""

    stock_set = Bool(False).tag(xml=XmlSer.attr('StockSet'))
    """TBD."""

    generic = Bool(False).tag(xml=XmlSer.attr('Generic'))
    """TBD."""

    mean_radius = Float(0.0).tag(xml=XmlSer.attr('MeanRadius'))
    """TBD."""

    credits = Unicode('').tag(xml=XmlSer.text_elem('Credits'))
    """Textual credits for the image originator."""

    credits_url = Unicode('').tag(xml=XmlSer.text_elem('CreditsUrl'))
    """A URL giving the source of the image or more information about its creation."""

    thumbnail_url = Unicode('').tag(xml=XmlSer.text_elem('ThumbnailUrl'))
    """A URL to a standard WWT thumbnail representation of this imageset."""

    description = Unicode('').tag(xml=XmlSer.text_elem('Description'))
    """A textual description of the imagery."""

    msr_community_id = Int(0).tag(xml=XmlSer.attr('MSRCommunityId'))
    """The ID number of the WWT Community that this content came from."""

    msr_component_id = Int(0).tag(xml=XmlSer.attr('MSRComponentId'))
    """The ID number of this content item on the WWT Communities system."""

    permission = Int(0).tag(xml=XmlSer.attr('Permission'))
    "TBD."

    def _tag_name(self):
        return 'ImageSet'

    def mutate_urls(self, mutator):
        if self.url:
            self.url = mutator(self.url)

        if self.dem_url:
            self.dem_url = mutator(self.dem_url)

        if self.credits_url:
            self.credits_url = mutator(self.credits_url)

        if self.thumbnail_url:
            self.thumbnail_url = mutator(self.thumbnail_url)

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

        Notes
        -----
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

            det = pc1_1 * pc2_2 - pc1_2 * pc2_1

            if det < 0:
                pc_sign = -1
            else:
                pc_sign = 1

            rot_rad = math.atan2(-pc_sign * pc1_2, pc2_2)

            # I am not sure if this is "supposed" to be allowed, but I've seen it.
            rtdet = math.sqrt(pc_sign * det)
            scale_x *= rtdet
            scale_y *= rtdet

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

        self.data_set_type = DataSetType.SKY
        self.width_factor = 2
        self.center_x = ra_deg
        self.center_y = dec_deg
        self.rotation_deg = rot_rad * 180 / math.pi

        if self.tile_levels > 0:  # are we tiled?
            self.projection = ProjectionType.TAN
            self.offset_x = (width / 2 - crpix_x) * abs(scale_x)
            self.offset_y = (height / 2 - crpix_y) * scale_y
            self.base_degrees_per_tile = scale_y * 256 * 2**self.tile_levels
        else:
            self.projection = ProjectionType.SKY_IMAGE
            self.offset_x = crpix_x
            self.offset_y = crpix_y
            self.base_degrees_per_tile = scale_y

        if place is not None:
            place.data_set_type = DataSetType.SKY
            place.rotation_deg = 0.  # I think this is better than propagating the image rotation?
            place.ra_hr = center_ra_deg / 15.
            place.dec_deg = center_dec_deg
            # It is hardcoded that in sky mode, zoom_level = height of client FOV * 6.
            place.zoom_level = height * scale_y * fov_factor * 6

        return self


    def wcs_headers_from_position(self):
        """Compute a set of WCS headers for this ImageSet's positional information.

        Returns
        -------
        A string-keyed dict-like containing FITS/WCS header keywords such as
        ``CTYPE1``, ``CRPIX1``, etc.

        Notes
        -----
        At the moment, this function only works for ImageSets with a
        projection type of ``SKY_IMAGE``. Support for other projections
        *might* be added later, if the need arises..

        """
        rv = {
            'CTYPE1': 'RA---TAN',
            'CTYPE2': 'DEC--TAN',
            'CRVAL1': self.center_x,
            'CRVAL2': self.center_y,
        }

        if self.projection != ProjectionType.SKY_IMAGE:
            raise NotImplementError('wcs_headers_from_position() only works if projection=SKY_IMAGE')

        rv['CRPIX1'] = self.offset_x + 1
        rv['CRPIX2'] = self.offset_y + 1
        rv['CDELT2'] = self.base_degrees_per_tile  # = scale_y, above
        rv['CDELT1'] = -self.base_degrees_per_tile  # AFAICT, non-square pixels can't be expressed

        c = math.cos(self.rotation_deg * math.pi / 180)
        s = math.sin(self.rotation_deg * math.pi / 180)

        rv['PC1_1'] = c
        rv['PC1_2'] = -s
        rv['PC2_1'] = s
        rv['PC2_2'] = c

        return rv
