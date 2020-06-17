# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Serialized information about graphical "layers" in the WWT enginge.

Not implemented:

- GreatCircleRouteLayer
- GroundOverlayLayer
- KmlLayer
- Object3d
- OrbitLayer
- SpreadSheetLayer
- TimeSeriesLayer
- VoTableLayer
- WmsLayer

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
ImageSetLayer
Layer
LayerContainer
'''.split()

from traitlets import Bool, Float, Instance, List, Unicode, Union

from . import LockedXmlTraits, XmlSer
from .imageset import ImageSet

class LayerContainer(LockedXmlTraits):
    """A collection of layers and reference frames."""

    id = Unicode('').tag(xml=XmlSer.attr('ID'))
    """A UUID-format randomized identifier for this layer collection.

    Data files associated with this layer collection that come in the WWTL
    cabinet file will be placed in a subdirectory whose name is this ID.

    """

    # ignore ReferenceFrames for now

    layers = List(
        trait = Union([
            Instance('wwt_data_formats.layers.ImageSetLayer', args=()),
        ]),
        default_value = ()
    ).tag(xml=XmlSer.wrapped_inner_list('Layers'))
    "A list of the layers stored in this container."

    def _tag_name(self):
        return 'LayerContainer'


class Layer(LockedXmlTraits):
    """Generic parent class for serializable WWT layers."""

    id = Unicode('').tag(xml=XmlSer.attr('Id'))
    """A UUID-format randomized identifier for this layer collection.

    Data files associated with this layer collection that come in the WWTL
    cabinet file will be placed in a subdirectory whose name is this ID.

    """

    layer_type = Unicode('').tag(xml=XmlSer.attr('Type'))
    "A textual representation of this layer's type."

    name = Unicode('').tag(xml=XmlSer.attr('Name'))
    "A user-facing name for this layer."

    reference_frame = Unicode('').tag(xml=XmlSer.attr('ReferenceFrame'))
    "The name of the reference frame relative to which this layer is positioned."

    opacity = Float(1.0).tag(xml=XmlSer.attr('Opacity'))

    # Skipping: Color, StartTime, Endtime, FadeSpan, FadeType

    def _tag_name(self):
        return 'Layer'

    def _layertype_name(self):
        raise NotImplementedError()

    def _check_elem_is_this_type(self, elem):
        return elem.attrib.get('Type', '') == self._layertype_name()


class ImageSetLayer(Layer):
    extension = Unicode('').tag(xml=XmlSer.attr('Extension'))
    """The filename extension for the underlying image if this is a SkyImage
    layer. This includes the period, e.g. ".tif"."""

    override_default = Bool(False).tag(xml=XmlSer.attr('OverrideDefault'))

    image_set = Instance(ImageSet).tag(xml=XmlSer.inner('ImageSet'))

    # Skipping: ScaleType, MinValue, MaxValue

    def _layertype_name(self):
        return 'TerraViewer.ImageSetLayer'
