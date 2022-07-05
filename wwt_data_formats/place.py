# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2022 the .NET Foundation
# Licensed under the MIT License.

"""
A place that a WWT user can visit.
"""

from __future__ import absolute_import, division, print_function

__all__ = """
Place
""".split()

from argparse import Namespace
from collections import namedtuple
from traitlets import Float, Instance, Int, Unicode, UseEnum

from . import LockedXmlTraits, XmlSer
from .abcs import UrlContainer
from .enums import Classification, Constellation, DataSetType
from .imageset import ImageSet


class Place(LockedXmlTraits, UrlContainer):
    """A place that can be visited."""

    data_set_type = UseEnum(DataSetType, default_value=DataSetType.EARTH).tag(
        xml=XmlSer.attr("DataSetType")
    )
    name = Unicode("").tag(xml=XmlSer.attr("Name"))
    ra_hr = Float(0.0).tag(xml=XmlSer.attr("RA"), xml_if_sky_type_is=True)
    dec_deg = Float(0.0).tag(xml=XmlSer.attr("Dec"), xml_if_sky_type_is=True)
    latitude = Float(0.0).tag(xml=XmlSer.attr("Lat"), xml_if_sky_type_is=False)
    longitude = Float(0.0).tag(xml=XmlSer.attr("Lng"), xml_if_sky_type_is=False)

    constellation = UseEnum(Constellation, default_value=Constellation.UNSPECIFIED).tag(
        xml=XmlSer.attr("Constellation")
    )
    """
    The constellation associated with this place's sky position, if it has one.
    Use :meth:`set_ra_dec` to compute this correctly (according to WWT).
    """

    classification = UseEnum(
        Classification, default_value=Classification.UNSPECIFIED
    ).tag(xml=XmlSer.attr("Classification"))
    magnitude = Float(0.0).tag(xml=XmlSer.attr("Magnitude"))
    distance = Float(0.0).tag(xml=XmlSer.attr("Distance"), xml_omit_zero=True)
    angular_size = Float(0.0).tag(xml=XmlSer.attr("AngularSize"))
    zoom_level = Float(0.0).tag(xml=XmlSer.attr("ZoomLevel"))
    rotation_deg = Float(0.0).tag(xml=XmlSer.attr("Rotation"))
    angle = Float(0.0).tag(xml=XmlSer.attr("Angle"))
    opacity = Float(100.0).tag(xml=XmlSer.attr("Opacity"))
    dome_alt = Float(0.0).tag(xml=XmlSer.attr("DomeAlt"), xml_omit_zero=True)
    dome_az = Float(0.0).tag(xml=XmlSer.attr("DomeAz"), xml_omit_zero=True)
    background_image_set = Instance(ImageSet, allow_none=True).tag(
        xml=XmlSer.wrapped_inner("BackgroundImageSet")
    )
    foreground_image_set = Instance(ImageSet, allow_none=True).tag(
        xml=XmlSer.wrapped_inner("ForegroundImageSet")
    )
    image_set = Instance(ImageSet, allow_none=True).tag(xml=XmlSer.inner("ImageSet"))
    thumbnail = Unicode("").tag(xml=XmlSer.attr("Thumbnail"))

    description = Unicode("").tag(xml=XmlSer.text_elem("Description"))
    """
    A description of the place, using HTML markup.

    This field is not actually used in the stock WWT clients, but it is wired up
    and loaded from the XML.
    """

    annotation = Unicode("").tag(xml=XmlSer.attr("Annotation"))
    """
    Annotation metadata for the place.

    This field is only used in the web engine and web client app. The web client
    app expects this field to contain a comma-separated list of key-value pairs,
    where each pair is delimited with colons:

    .. code-block::

        key1:val1,key2:val2,key3:val3

    The webclient includes some unfinished support for this field to be used to
    create circular annotations with YouTube video links. If your WTML file will
    not be viewed in the webclient, you can use this field to convey arbitrary
    textual data to the WWT Web Engine JavaScript/TypeScript layer.

    """

    msr_community_id = Int(0).tag(xml=XmlSer.attr("MSRCommunityId"), xml_omit_zero=True)
    """The ID number of the WWT Community that this content came from."""

    msr_component_id = Int(0).tag(xml=XmlSer.attr("MSRComponentId"), xml_omit_zero=True)
    """The ID number of this content item on the WWT Communities system."""

    permission = Int(0).tag(xml=XmlSer.attr("Permission"), xml_omit_zero=True)
    "TBD."

    xmeta = Instance(
        Namespace,
        args=(),
        help="XML metadata - a namespace object for attaching arbitrary text to serialize",
    ).tag(xml=XmlSer.ns_to_attr("X"))

    def _tag_name(self):
        return "Place"

    def mutate_urls(self, mutator):
        if self.thumbnail:
            self.thumbnail = mutator(self.thumbnail)

        if self.background_image_set:
            self.background_image_set.mutate_urls(mutator)

        if self.foreground_image_set:
            self.foreground_image_set.mutate_urls(mutator)

        if self.image_set:
            self.image_set.mutate_urls(mutator)

    def as_imageset(self):
        """Return an ImageSet for this place if one is defined.

        Returns
        -------
        Either :class:`wwt_data_formats.imageset.ImageSet` or None.

        Notes
        -----
        If the :attr:`foreground_image_set` of this :class:`Place` is not
        None, it is returned. Otherwise, if its :attr:`image_set` is not
        None, that is returned. Otherwise, None is returned.

        """
        if self.foreground_image_set is not None:
            return self.foreground_image_set
        return self.image_set

    def set_ra_dec(self, ra_hr, dec_deg):
        """
        Update the sky coordinates associated with this Place and associated
        metadata.

        Parameters
        ----------
        ra_hr : number
            The right ascension, in hours
        dec_deg : number
            The declination, in degrees

        Returns
        -------
        Self, for chaining.

        Notes
        -----
        Beyond simply setting the associated fields, this method will set the
        :attr:`data_set_type` to Sky, compute the correct setting for
        :attr:`constellation`, and clear :attr:`latitude` and :attr:`longitude`.
        The constellation computation is done by emulating WWT's internal
        computation, which may give different results than other methods in
        (literal) corner cases. In cases where precision matters and WWT
        compatibility does not, :func:`astropy.coordinates.get_constellation`
        should be preferred.
        """
        db = _get_iau_constellations()
        self.ra_hr = ra_hr
        self.dec_deg = dec_deg
        self.data_set_type = DataSetType.SKY
        self.latitude = 0
        self.longitude = 0
        self.constellation = db.find_constellation_for_point(ra_hr, dec_deg)
        return self

    def update_constellation(self):
        """
        Update the constellation associated with this Place to agree with its
        current RA and declination, if set.

        Returns
        -------
        Self, for chaining.

        Notes
        -----
        If this object has a :attr:`data_set_type` of Sky, this method will
        update :attr:`constellation` to be correct given its :attr:`ra_hr` and
        :attr:`dec_deg`, and clear :attr:`latitude` and :attr:`longitude`.
        Otherwise, the constellation, RA, and Dec will be cleared.

        The constellation computation is done by emulating WWT's internal
        computation, which may give different results than other methods in
        (literal) corner cases. In cases where precision matters and WWT
        compatibility does not, :func:`astropy.coordinates.get_constellation`
        should be preferred.
        """

        if self.data_set_type == DataSetType.SKY:
            db = _get_iau_constellations()
            self.latitude = 0
            self.longitude = 0
            self.constellation = db.find_constellation_for_point(
                self.ra_hr, self.dec_deg
            )
        else:
            self.ra_hr = 0
            self.dec_deg = 0
            self.constellation = Constellation.UNSPECIFIED

        return self


Radec = namedtuple("Radec", "ra_hr dec_deg")


class ConstellationDatabase(object):
    _shapes = None

    def __init__(self, data_stream):
        # This implementation emulates the WWT `Constellations()` constructor
        # with `boundry=true` and `noInterpollation=true`, which is what is used
        # for the constellation-containment tests (`constellationCheck` AKA
        # `Containment`). We have also edited the `constellations.txt` file,
        # pulled from
        # `http://www.worldwidetelescope.org/data/constellations.txt`, to remove
        # the `I` (interpolated) entries, which increase the size of the data
        # file substantially and are ignored in the check mode, and to convert
        # leading spaces to trailing spaces, especially with separated sign
        # characters.

        prev_abbrev = ""
        cur_points = None
        shapes = {}

        for line in data_stream:
            ra_hr = float(line[:10])
            dec_deg = float(line[11:22])
            abbrev = line[23:27].strip()  # "SER1" and "SER2" are 4 letters

            if abbrev != prev_abbrev:
                cur_points = []
                shapes[Constellation(abbrev)] = cur_points
                prev_abbrev = abbrev
                prev_ra = 0.0

            if ra_hr - prev_ra > 12:
                ra_hr -= 24
            elif ra_hr - prev_ra < -12:
                ra_hr += 24

            cur_points.append(Radec(ra_hr, dec_deg))
            prev_ra = ra_hr

        self._shapes = shapes

    def find_constellation_for_point(self, ra_hr, dec_deg):
        """
        Find the constellation corresponding to a given RA and Dec.

        ra_hr : RA in hours
        dec_deg : dec in degrees
        """
        # This implementation from WWT's `FindConstellationForPoint()` function,
        # with a correction for Apus/Octans. The basic approach is to use the
        # "even-odd rule" (https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule),
        # with some special-casing to deal with the fact that we are in a
        # spherical coordinate system (including the data preprocessing in the
        # constructor above).

        if dec_deg > 88.402:
            return Constellation.URSA_MINOR

        for constellation, points in self._shapes.items():
            inside = False
            j = len(points) - 1

            for i in range(len(points)):
                c = points[i].dec_deg <= dec_deg and dec_deg < points[j].dec_deg
                c = c or points[j].dec_deg <= dec_deg and dec_deg < points[i].dec_deg

                if c:
                    # The WWT specification for Octans ends up spanning more
                    # than 24 hours in RA, with the postprocessed RA data having
                    # the form [0.1022, 3.3394, ... 23.4665, 24.1044]. This
                    # leads to a failure of this algorithm for points in the
                    # southernmost portion of Apus. We can fix things by
                    # wrapping around the i'th RA when needed.

                    eff_i_ra = points[i].ra_hr
                    if points[j].ra_hr - eff_i_ra > 12:
                        eff_i_ra += 24

                    x = (points[j].ra_hr - eff_i_ra) * (dec_deg - points[i].dec_deg)
                    x /= points[j].dec_deg - points[i].dec_deg
                    if ra_hr < x + eff_i_ra:
                        inside = not inside

                j = i

            if inside:
                return constellation

        if ra_hr > 0:
            return self.find_constellation_for_point(ra_hr - 24, dec_deg)

        # "Ursa Minor is tricky since it wraps around the poles. I[t] can evade
        # the point in rect test."

        if dec_deg > 65.5:
            return Constellation.URSA_MINOR

        if dec_deg < -65.5:
            return Constellation.OCTANS

        return Constellation.UNSPECIFIED


_iau_constellation_data = None


def _get_iau_constellations():
    import os.path

    global _iau_constellation_data

    if _iau_constellation_data is None:
        data = os.path.join(os.path.dirname(__file__), "data", "iau_constellations.txt")
        with open(data, "rt") as f:
            _iau_constellation_data = ConstellationDatabase(f)

    return _iau_constellation_data
