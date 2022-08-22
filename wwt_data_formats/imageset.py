# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2022 the .NET Foundation
# Licensed under the MIT License.

"""
An image, possibly tiled, for display in WWT.
"""

from __future__ import absolute_import, division, print_function

__all__ = """
ImageSet
""".split()

import math
from traitlets import Bool, Float, Int, Unicode, UseEnum
from xml.etree import ElementTree as etree

from . import LockedXmlTraits, XmlSer
from .abcs import UrlContainer
from .enums import Bandpass, DataSetType, ProjectionType


class ImageSet(LockedXmlTraits, UrlContainer):
    """
    A WWT imagery dataset.

    Instances of this class express WWT imagery datasets and their spatial
    positioning. Imagesets are exposed to the WWT engine through their XML
    serialization in a WTML :class:`~wwt_data_formats.folder.Folder`. The engine
    can be instructed to load such a folder, making its imagesets available for
    rendering.
    """

    data_set_type = UseEnum(DataSetType, default_value=DataSetType.SKY).tag(
        xml=XmlSer.attr("DataSetType")
    )
    """The renderer mode to which these data apply.

    Possible values are ``"Earth"``, ``"Planet"``, ``"Sky"``, ``"Panorama"``,
    ``"SolarSystem"``, and ``"Sandbox"``.

    """
    reference_frame = Unicode("").tag(xml=XmlSer.attr("ReferenceFrame"))
    """TBD."""

    name = Unicode("").tag(xml=XmlSer.attr("Name"), xml_even_if_empty=True)
    """A name used to refer to this imageset.

    Various parts of the WWT internals reference imagesets by this name, so
    it should be distinctive.

    """
    url = Unicode("").tag(xml=XmlSer.attr("Url"), xml_even_if_empty=True)
    """The URL of the image data.

    Either a URL or a URL template. URLs that are exposed to the engine should
    be absolute and use the ``http://`` protocol (the web engine will rewrite
    them to HTTPS if needed). The ``wwtdatatool`` program that comes with this
    package provides some helpful utilities to allow data-processing to use relative URLs. TODO: more
    details.

    """
    alt_url = Unicode("").tag(xml=XmlSer.attr("AltUrl"))
    """An alternative URL that provided the data.

    If provided and the Windows client attempts to load an imageset using this
    alternative URL, that imageset will be replaced by this one. This provides a
    mechanism for superseding old imagesets with improved versions.

    """
    dem_url = Unicode("").tag(xml=XmlSer.attr("DemUrl"))
    """The URL of the DEM data.

    Either a URL or a URL template. TODO: details

    """
    width_factor = Int(2).tag(xml=XmlSer.attr("WidthFactor"))
    """This is a legacy parameter. Leave it at 2."""

    base_tile_level = Int(0).tag(xml=XmlSer.attr("BaseTileLevel"))
    """The level of the highest (coarsest-resolution) tiling available.

    This should be zero except for special circumstances.

    """
    quad_tree_map = Unicode("").tag(
        xml=XmlSer.attr("QuadTreeMap"), xml_even_if_empty=True
    )
    """TBD."""

    tile_levels = Int(0).tag(xml=XmlSer.attr("TileLevels"))
    """The number of levels of tiling.

    Should be zero for untiled images (``projection =
    ProjectionType.SkyImage``).

    For tiled images (``projection = ProjectionType.Tan``), an image with
    ``tile_levels = 1`` has been broken into four tiles, each 256x256 pixels.
    For ``tile_levels = 2``, there are sixteen tiles, and the padded height of
    the tiled area is ``256 * 2**2 = 1024`` pixels. Image with dimensions of
    2048 pixels or smaller do not need to be tiled, so if this parameter is
    nonzero it will usually be 4 or larger.

    """
    base_degrees_per_tile = Float(0.0).tag(xml=XmlSer.attr("BaseDegreesPerTile"))
    """The angular scale of the image.

    For untiled images, this is the pixel scale: the number of degrees per pixel
    in the vertical direction. Non-square pixels are not supported.

    For tiled images, this is the angular height of the image, in degrees, after
    its dimensions have been padded out to the next largest power of 2 for
    tiling purposes. If a square image is 1200 pixels tall and has a height of
    0.016 deg, the padded height would be 2048 pixels and this parameter should
    be set to 0.016 * 2048 / 1200 = 0.0273.

    """
    file_type = Unicode(".png").tag(xml=XmlSer.attr("FileType"), xml_even_if_empty=True)
    """
    The extension(s) of the image file(s) in this set.

    In the simplest case, this field will contain an image filetype extension
    including the leading period, such as ``.jpeg`` or ``.png``. Some datasets
    in the wild lack the leading period: they have just ``png`` or something
    similar. The value ``.auto`` is also used in some cases, which can be OK
    because often WWT doesn't actually use this field for any particular
    purpose.

    Some datasets, like HiPS imagery, provide multiple filetypes simultaneously.
    These can be expressed by including several filename extensions separated by
    spaces. For instance, ``png jpeg fits``. The existing WTML records that
    support multiple filetypes do not include any leading periods, but clients
    should be prepared for them to be present.

    Imagesets to be rendered as FITS data *must* have the exact value ``.fits``
    for this field. If multiple filetypes are specified, the special
    FITS-rendering machinery will not be invoked. This is true for both single
    FITS files and tiled FITS imagesets, including HiPS FITS datasets.

    A supported filetype extension of ``tsv`` (or ``.tsv``) means that this
    "imageset" actually contains a HiPS progressive catalog, not bitmap imagery.
    Imageset records should not intermix image-type and catalog-type filetypes.
    (We don't know if there are any examples in the wild of HiPS datasets that
    claim to contain both kinds of data.)
    """

    bottoms_up = Bool(False).tag(xml=XmlSer.attr("BottomsUp"))
    """
    The parity of the image's projection on the sky.

    For untiled (``projection = SkyImage``) images, this flag defines the
    image's parity, which basically sets whether the image needs to be flipped
    during rendering. This field should be False for typical RGB color images
    that map onto the sky as if you had taken them with a digital camera. For
    these images, the first row of image data is at the top of the image at zero
    rotation. For typical FITS files, on the other hand, the first row of image
    data is at the bottom of the image, which results in a parity inversion. In
    these cases, the ``bottoms_up`` flag should be True (hence its name). In the
    terminology of `Astrometry.Net
    <https://astroquery.readthedocs.io/en/latest/astrometry_net/astrometry_net.html#parity>`_,
    ``bottoms_up = False`` corresponds to negative parity, and ``bottoms_up =
    True`` corresponds to positive parity.

    The effect of setting this flag to True is to effectively flip the image and
    its coordinate system left-to-right. For a ``bottoms_up = False`` image with
    :attr:`offset_x`, :attr:`offset_y`, and :attr:`rotation_deg` all zero, the
    lower-left corner of the image lands at the :attr:`center_x` and
    :attr:`center_y`, and positive rotations rotate the image counter-clockwise
    around that origin. If you take the same image and make ``bottoms_up =
    True``, the image will appear to have been flipped left-to-right, the
    lower-*right* corner of the image will land at the coordinate center, and
    positive rotations will rotate it *clockwise* around that origin. In both
    cases, positive values of :attr:`offset_x` and :attr:`offset_y` move the
    center of the image closer to the coordinate center, but when ``bottoms_up =
    False``, this means that the image is moving down and left, and when
    ``bottoms_up = True`` this means that the image is moving down and right.

    For tiled images (``projection = Tan``), this field must be false. If it is
    true, the imageset won't render.
    """

    projection = UseEnum(ProjectionType, default_value=ProjectionType.SKY_IMAGE).tag(
        xml=XmlSer.attr("Projection")
    )
    """The type of projection used to place this image on the sky.

    For untiled images, this should be "SkyImage". For tiled images, it should
    be "Tan". The :meth:`set_position_from_wcs` method will set this value
    appropriately based on :attr:`tile_levels`.

    """
    center_x = Float(0.0).tag(xml=XmlSer.attr("CenterX"))
    """The horizontal location of the center of the image’s projection
    coordinate system.

    For sky images, this is a right ascension in degrees. Note that this
    parameter just helps to define a coordinate system; it does not control how
    the actual image data are placed onto that coordinate system. The
    :attr:`offset_x` and :attr:`offset_y` parameters do that.

    """
    center_y = Float(0.0).tag(xml=XmlSer.attr("CenterY"))
    """The vertical location of the center of the image’s projection coordinate
    system.

    For sky images, this is a declination in degrees. Note that this parameter
    just helps to define a coordinate system; it does not control how the actual
    image data are placed onto that coordinate system. The :attr:`offset_x` and
    :attr:`offset_y` parameters do that.

    """
    offset_x = Float(0.0).tag(xml=XmlSer.attr("OffsetX"), xml_omit_zero=True)
    """
    The horizontal positioning of the image relative to its projection
    coordinate system.

    For untiled sky images with :attr:`bottoms_up` false, the image is by
    default positioned such that its lower left corner lands at the center of
    the projection coordinate system (namely, :attr:`center_x` and
    :attr:`center_y`). The offset is measured in pixels and moves the image
    leftwards. Therefore, ``offset_x = image_width / 2`` places the horizontal
    center of the image at ``center_x``. This parameter is therefore analogous
    to the WCS keyword ``CRVAL1``.

    For untiled sky images where :attr:`bottoms_up` is true, the X coordinate
    system has been mirrored. Therefore when this field is zero, the lower
    *right* corner of the image will land at the center of the projection
    coordinate system, and positive values will move the image to the right.

    For tiled sky images, the offset is measured in *degrees*, and a value of
    zero means that the *center* of the image lands at the center of the
    projection coordinate system. Increasingly positive values move the image to
    the right.

    As per the usual practice, offsets are always along the horizontal axis of
    the image in question, regardless of its :attr:`rotation <rotation_deg>` on
    the sky.

    """
    offset_y = Float(0.0).tag(xml=XmlSer.attr("OffsetY"), xml_omit_zero=True)
    """The vertical positioning of the image relative to its projection
    coordinate system.

    For untiled sky images with :attr:`bottoms_up` false, the image is by
    default positioned such that its lower left corner lands at the center of
    the projection coordinate system (namely, :attr:`center_x` and
    :attr:`center_y`). The offset is measured in pixels and moves the image
    downwards. Therefore, ``offset_y = image_height / 2`` places the vertical
    center of the image at ``center_y``. This parameter is therefore analogous
    to the WCS keyword ``CRVAL2``.

    For untiled sky images where :attr:`bottoms_up` is true, the X coordinate
    system has been mirrored but the Y coordinate system is the same. Therefore
    when this field is zero, the lower *right* corner of the image will land at
    the center of the projection coordinate system, but positive values will
    still move the image downwards.

    For tiled sky images, the offset is measured in *degrees*, and a value of
    zero means that the *center* of the image lands at the center of the
    projection coordinate system. Increasingly positive values move the image
    upwards.

    As per the usual practice, offsets are always along the vertical axis of the
    image in question, regardless of its :attr:`rotation <rotation_deg>` on the
    sky.

    """
    rotation_deg = Float(0.0).tag(xml=XmlSer.attr("Rotation"))
    """
    The rotation of image’s projection coordinate system, in degrees.

    For sky images with :attr:`bottoms_up` false, this is East from North, i.e.
    counterclockwise. If :attr:`bottoms_up` is true (only allowed for untiled
    images), the image coordinate system is mirrored, and positive rotations
    rotate the image *clockwise* relative to the sky.
    """

    band_pass = UseEnum(Bandpass, default_value=Bandpass.VISIBLE).tag(
        xml=XmlSer.attr("BandPass")
    )
    """The bandpass of the image data."""

    sparse = Bool(True).tag(xml=XmlSer.attr("Sparse"))
    """TBD."""

    elevation_model = Bool(False).tag(xml=XmlSer.attr("ElevationModel"))
    """TBD."""

    stock_set = Bool(False).tag(xml=XmlSer.attr("StockSet"))
    """TBD."""

    generic = Bool(False).tag(xml=XmlSer.attr("Generic"))
    """TBD."""

    mean_radius = Float(0.0).tag(xml=XmlSer.attr("MeanRadius"), xml_omit_zero=True)
    """TBD."""

    credits = Unicode("").tag(xml=XmlSer.text_elem("Credits"))
    """Textual credits for the image originator."""

    credits_url = Unicode("").tag(xml=XmlSer.text_elem("CreditsUrl"))
    """A URL giving the source of the image or more information about its creation."""

    thumbnail_url = Unicode("").tag(
        xml=XmlSer.text_elem("ThumbnailUrl"), xml_even_if_empty=True
    )
    """A URL to a standard WWT thumbnail representation of this imageset."""

    description = Unicode("").tag(xml=XmlSer.text_elem("Description"))
    """
    A textual description of the imagery.

    This field is referenced a few times in the original WWT documentation, but
    is not actually implemented. The ``Place.description`` field is at least
    loaded from the XML.
    """

    msr_community_id = Int(0).tag(xml=XmlSer.attr("MSRCommunityId"), xml_omit_zero=True)
    """The ID number of the WWT Community that this content came from."""

    msr_component_id = Int(0).tag(xml=XmlSer.attr("MSRComponentId"), xml_omit_zero=True)
    """The ID number of this content item on the WWT Communities system."""

    permission = Int(0).tag(xml=XmlSer.attr("Permission"), xml_omit_zero=True)
    "TBD."

    pixel_cut_low = Float(0.0).tag(xml=XmlSer.attr("PixelCutLow"), xml_omit_zero=True)
    """Suggested default low cutoff value when displaying FITS."""

    pixel_cut_high = Float(0.0).tag(xml=XmlSer.attr("PixelCutHigh"), xml_omit_zero=True)
    """Suggested default high cutoff value when displaying FITS."""

    data_min = Float(0.0).tag(xml=XmlSer.attr("DataMin"), xml_omit_zero=True)
    """Lowest data value of a FITS file."""

    data_max = Float(0.0).tag(xml=XmlSer.attr("DataMax"), xml_omit_zero=True)
    """Highest data value of a FITS file."""

    def _tag_name(self):
        return "ImageSet"

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
        """
        Set the positional information associated with this imageset to match a
        set of WCS headers.

        Parameters
        ----------
        headers : :class:`~astropy.io.fits.Header` or string-keyed dict-like

            A set of FITS-like headers including WCS keywords such as ``CRVAL1``.

        width : positive integer

            The width of the image associated with the WCS, in pixels.

        height : positive integer

            The height of the image associated with the WCS, in pixels.

        place : optional :class:`~wwt_data_formats.place.Place`

            If specified, the centering and zoom level of the
            :class:`~wwt_data_formats.place.Place` object will be set to match
            the center and size of this image.

        fov_factor : optional

            If *place* is provided, its zoom level will be set so that the angular
            height of the client viewport is this factor times the angular height of
            the image. The default is 1.7.

        Returns
        -------
        **self**

            For convenience in chaining function calls.

        Notes
        -----
        Certain of the ImageSet parameters take on different meanings depending
        on whether the image in question is a tiled "study" or not. This method
        will alter its behavior depending on whether the :attr:`tile_levels`
        attribute is greater than zero. **Make sure that this parameter has
        acquired its final value before calling this function.**

        For the time being, the WCS must be equatorial using the gnomonic
        (``TAN``) projection.

        Required keywords in *headers* are:

        - ``CTYPE1`` and ``CTYPE2``
        - ``CRVAL1`` and ``CRVAL2``
        - ``CRPIX1`` and ``CRPIX2``
        - Either:
            - ``CD1_1``, ``CD2_2`` (preferred) or
            - ``CDELT1``, ``CDELT2``, ``PC1_1``, and ``PC1_2``;

        If present ``PC1_2``, ``PC2_1``, ``CD1_2``, and/or ``CD2_1`` are used.
        If absent, they are assumed to be zero.

        This routine assumes that the WCS coordinates have the correct parity
        for the data that they describe. If these WCS coordinates describe a
        JPEG-like image, the parity of the coordinates should be negative
        ("top-down"), which means that the determinant of the CD matrix should
        have a *positive* sign. If these coordinates describe a FITS-like image,
        the parity should be positive or "bottoms-up", with a negative
        determinant of the CD matrix. If the image in question is tiled, the
        parity must be top-down, in the sense the bottoms-up tiled imagery just
        won't render in the engine. There are some CD matrices that can't be
        expressed in WWT's formalism (rotation, scale, parity) and this method
        will do its best to detect and reject them.
        """

        if headers["CTYPE1"] != "RA---TAN" or headers["CTYPE2"] != "DEC--TAN":
            raise ValueError("WCS coordinates must be in an equatorial/TAN projection")

        # Figure out the stuff we need from the headers.

        ra_deg = headers["CRVAL1"]
        dec_deg = headers["CRVAL2"]

        # In FITS/WCS, pixel coordinates are 1-based and integer pixel
        # coordinates land on pixel centers. Therefore in standard FITS
        # orientation, where the "first" pixel is at the lower-left, the
        # lower-left corner of the image has pixel coordinate (0.5, 0.5). For
        # the WWT offset parameters, the lower-left corner of the image has
        # coordinate (0, 0).
        refpix_x = headers["CRPIX1"] - 0.5
        refpix_y = headers["CRPIX2"] - 0.5

        if "CD1_1" in headers:
            cd1_1 = headers["CD1_1"]
            cd2_2 = headers["CD2_2"]
            cd1_2 = headers.get("CD1_2", 0.0)
            cd2_1 = headers.get("CD2_1", 0.0)
        else:
            # older PC/CDELT form -- note that we're using two additional
            # numbers to express the same information.
            d1 = headers["CDELT1"]
            d2 = headers["CDELT2"]
            cd1_1 = d1 * headers.get("PC1_1", 1.0)
            cd2_2 = d2 * headers.get("PC2_2", 1.0)
            cd1_2 = d1 * headers.get("PC1_2", 0.0)
            cd2_1 = d2 * headers.get("PC2_1", 0.0)

        cd_det = cd1_1 * cd2_2 - cd1_2 * cd2_1

        if cd_det < 0:
            cd_sign = -1

            if self.tile_levels > 0 and self.projection != ProjectionType.TOAST:
                raise Exception(
                    "WCS for tiled imagery must have top-down/negative/JPEG_like parity"
                )
        else:
            cd_sign = 1

        # Given how WWT implements its rotation coordinates, this expression
        # turns out to give us the correct value for different rotations and
        # parities:

        rot_rad = math.atan2(-cd_sign * cd1_2, -cd2_2)

        # We can only express square pixels with a rotation and a potential
        # parity flip. Do some cross-checks to ensure that the input matrix can
        # be well-approximated this way. There's probably a smarter
        # linear-algebra way to do this.

        TOL = 0.05

        if not abs(cd_det) > 0:
            raise ValueError("determinant of the CD matrix is not positive")

        scale_x = math.sqrt(cd1_1**2 + cd1_2**2)
        scale_y = math.sqrt(cd2_1**2 + cd2_2**2)

        if abs(scale_x - scale_y) / (scale_x + scale_y) > TOL:
            raise ValueError("WWT cannot express non-square pixels, which this WCS has")

        det_scale = math.sqrt(abs(cd_det))

        if abs((cd1_1 - cd_sign * cd2_2) / det_scale) > TOL:
            raise ValueError(
                f"WWT cannot express this CD matrix (1; {cd1_1} {cd_sign} {cd2_2} {det_scale})"
            )

        if abs((cd2_1 + cd_sign * cd1_2) / det_scale) > TOL:
            raise ValueError(
                f"WWT cannot express this CD matrix (2; {cd2_1} {cd_sign} {cd1_2} {det_scale})"
            )

        # This is our best effort to make sure that the view centers on the
        # center of the image.

        try:
            from astropy.wcs import WCS
        except:
            center_ra_deg = ra_deg
            center_dec_deg = dec_deg
        else:
            wcs = WCS(headers)
            # The WCS object uses 0-based indices where the integer coordinates
            # land on pixel centers. Therefore the dead center of the image has
            # pixel coordinates as below. For instance, in an image 2 pixels
            # wide, the horizontal center is where the two pixels touch, which
            # has an X coordinate of 0.5.
            center = wcs.pixel_to_world((width - 1) / 2, (height - 1) / 2)
            center_ra_deg = center.ra.deg
            center_dec_deg = center.dec.deg

        # Now, assign the fields

        self.data_set_type = DataSetType.SKY
        self.width_factor = 2
        self.center_x = ra_deg
        self.center_y = dec_deg
        self.rotation_deg = rot_rad * 180 / math.pi

        if self.projection != ProjectionType.TOAST:
            if self.tile_levels > 0:  # are we tiled?
                self.projection = ProjectionType.TAN
                self.bottoms_up = False
                self.offset_x = (width / 2 - refpix_x) * scale_x
                self.offset_y = (refpix_y - height / 2) * scale_y
                self.base_degrees_per_tile = scale_y * 256 * 2**self.tile_levels
            else:
                self.projection = ProjectionType.SKY_IMAGE
                self.bottoms_up = cd_sign == -1
                self.offset_x = refpix_x
                self.offset_y = height - refpix_y
                self.base_degrees_per_tile = scale_y

                if self.bottoms_up:
                    self.rotation_deg = -self.rotation_deg

        if place is not None:
            place.set_ra_dec(center_ra_deg / 15.0, center_dec_deg)
            place.rotation_deg = (
                0.0  # I think this is better than propagating the image rotation?
            )
            # It is hardcoded that in sky mode, zoom_level = height of client FOV * 6.
            place.zoom_level = height * scale_y * fov_factor * 6

        return self

    def wcs_headers_from_position(self, height=None):
        """
        Compute a set of WCS headers for this ImageSet's positional information.

        Parameters
        ----------
        height : optional int
            The height of the underlying image, in pixels. This quantity is
            needed to compute WCS headers correctly for untiled (``SKY_IMAGE``
            projection) images. If this quantity is needed but not provided,
            a ValueError will be raised. Note that the :class:`ImageSet` class
            does *not* store this quantity.

        Returns
        -------
        A string-keyed dict-like containing FITS/WCS header keywords such as
        ``CTYPE1``, ``CRPIX1``, etc.

        Notes
        -----
        At the moment, this function only works for ImageSets with a projection
        type of ``SKY_IMAGE``. Support for other projections *might* be added
        later, if the need arises. Note, however, that tiled images have their
        sizes adjusted to be powers of 2, and the "actual" size of the source
        imagery is not necessarily preserved.
        """

        rv = {
            "CTYPE1": "RA---TAN",
            "CTYPE2": "DEC--TAN",
            "CRVAL1": self.center_x,
            "CRVAL2": self.center_y,
        }

        if self.projection != ProjectionType.SKY_IMAGE:
            raise NotImplementedError(
                "wcs_headers_from_position() only works if projection=SKY_IMAGE"
            )

        if height is None:
            raise ValueError(
                "must provide `height` to compute WCS headers for untiled images"
            )

        rv["CRPIX1"] = self.offset_x + 0.5
        rv["CRPIX2"] = height - self.offset_y + 0.5

        # The WWT rotation angle is 180 degrees away from the usual angle
        # that you would use for a rotation matrix, which is why we negate
        # these trig values:
        parity = -1 if self.bottoms_up else 1
        c = -math.cos(parity * self.rotation_deg * math.pi / 180)
        s = -math.sin(parity * self.rotation_deg * math.pi / 180)

        # | CD1_1 CD1_2 | = scale * | p 0 | * |  cos(theta) sin(theta) |
        # | CD2_1 CD2_2 |           | 0 1 |   | -sin(theta) cos(theta) |

        rv["CD1_1"] = c * self.base_degrees_per_tile * parity
        rv["CD1_2"] = s * self.base_degrees_per_tile * parity
        rv["CD2_1"] = -s * self.base_degrees_per_tile
        rv["CD2_2"] = c * self.base_degrees_per_tile

        return rv
