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
from traitlets import Float, Instance, Unicode, UseEnum

from . import LockedXmlTraits, XmlSer
from .enums import Classification, Constellation, DataSetType
from .imageset import ImageSet

class Place(LockedXmlTraits):
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
    xmeta = Instance(
        Namespace,
        args = (),
        help = 'XML metadata - a namespace object for attaching arbitrary text to serialize',
    ).tag(xml=XmlSer.ns_to_attr('X'))

    def _tag_name(self):
        return 'Place'
