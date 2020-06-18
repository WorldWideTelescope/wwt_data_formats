# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

"""A place that a WWT user can visit.

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
Place
'''.split()

from argparse import Namespace
from traitlets import Float, Instance, Int, Unicode, UseEnum

from . import LockedXmlTraits, XmlSer
from .abcs import UrlContainer
from .enums import Classification, Constellation, DataSetType
from .imageset import ImageSet

class Place(LockedXmlTraits, UrlContainer):
    """A place that can be visited."""

    data_set_type = UseEnum(
        DataSetType,
        default_value = DataSetType.EARTH
    ).tag(xml=XmlSer.attr('DataSetType'))
    name = Unicode('').tag(xml=XmlSer.attr('Name'))
    ra_hr = Float(0.0).tag(xml=XmlSer.attr('RA'))
    dec_deg = Float(0.0).tag(xml=XmlSer.attr('Dec'))
    latitude = Float(0.0).tag(xml=XmlSer.attr('Lat'))
    longitude = Float(0.0).tag(xml=XmlSer.attr('Lng'))
    constellation = UseEnum(
        Constellation,
        default_value = Constellation.UNSPECIFIED
    ).tag(xml=XmlSer.attr('Constellation'))
    classification = UseEnum(
        Classification,
        default_value = Classification.UNSPECIFIED
    ).tag(xml=XmlSer.attr('Classification'))
    magnitude = Float(0.0).tag(xml=XmlSer.attr('Magnitude'))
    distance = Float(0.0).tag(xml=XmlSer.attr('Distance'))
    angular_size = Float(0.0).tag(xml=XmlSer.attr('AngularSize'))
    zoom_level = Float(0.0).tag(xml=XmlSer.attr('ZoomLevel'))
    rotation_deg = Float(0.0).tag(xml=XmlSer.attr('Rotation'))
    angle = Float(0.0).tag(xml=XmlSer.attr('Angle'))
    opacity = Float(100.0).tag(xml=XmlSer.attr('Opacity'))
    dome_alt = Float(0.0).tag(xml=XmlSer.attr('DomeAlt'))
    dome_az = Float(0.0).tag(xml=XmlSer.attr('DomeAz'))
    background_image_set = Instance(ImageSet, allow_none=True).tag(xml=XmlSer.wrapped_inner('BackgroundImageSet'))
    foreground_image_set = Instance(ImageSet, allow_none=True).tag(xml=XmlSer.wrapped_inner('ForegroundImageSet'))
    image_set = Instance(ImageSet, allow_none=True).tag(xml=XmlSer.inner('ImageSet'))
    thumbnail = Unicode('').tag(xml=XmlSer.attr('Thumbnail'))
    msr_community_id = Int(0).tag(xml=XmlSer.attr('MSRCommunityId'))
    """The ID number of the WWT Community that this content came from."""

    msr_component_id = Int(0).tag(xml=XmlSer.attr('MSRComponentId'))
    """The ID number of this content item on the WWT Communities system."""

    permission = Int(0).tag(xml=XmlSer.attr('Permission'))
    "TBD."

    xmeta = Instance(
        Namespace,
        args = (),
        help = 'XML metadata - a namespace object for attaching arbitrary text to serialize',
    ).tag(xml=XmlSer.ns_to_attr('X'))

    def _tag_name(self):
        return 'Place'

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
