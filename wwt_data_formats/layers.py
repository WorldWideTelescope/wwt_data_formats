# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Serialized information about graphical "layers" in the WWT engine.

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
LayerContainerReader
LayerContainerXml
'''.split()

from traitlets import Bool, Float, Instance, List, Unicode, Union

from . import LockedXmlTraits, XmlSer
from .filecabinet import FileCabinetReader
from .imageset import ImageSet


class LayerContainerReader(object):
    """A collection of layers and reference frames."""

    _reader = None
    _info = None

    def __init__(self, stream):
        self._reader = FileCabinetReader(stream)

        for fn in self._reader.filenames():
            if fn.endswith('.wwtxml') and '\\' not in fn:
                b = self._reader.read_file(fn)
                text = b.decode('utf-8-sig')
                self._info = LayerContainerXml.from_text(text)

        if self._info is None:
            raise Exception('found no ".wwtxml" file in WWTL file cabinet')


    def close(self):
        self._reader.close()
        self._reader = None


    @classmethod
    def from_file(cls, path):
        """Deserialize layers from a WWTL "file cabinet" file.

        Parameters
        ----------
        path : string
          The path of the file-cabinet file.

        Returns
        -------
        An initialized instance of the class.

        """
        f = open(path, 'rb')
        return cls(f)


    @property
    def layers(self):
        return self._info.layers


    def read_layer_file(self, layer, extension):
        """Read a data file associated with a layer in this container.

        Parameters
        ----------
        layer : :class:`Layer`
            One of the layer objects found in this container.
        extension : string
            The file extension of the associated data file, including
            a leading period. For instance, ".txt".

        Returns
        -------
        The contents of the data file as a :class:`bytes` object.

        """
        # In most examples I've seen, the layer file is in a subdirectory
        # grouped by the layer's UUID. But in one example (David Weigel
        # LMC WWTL file, June 2020), it's not in the subdirectory.

        fn = self._info.id + '\\' + layer.id + extension

        if fn in self._reader.filenames():
            return self._reader.read_file(fn)
        return self._reader.read_file(layer.id + extension)


class LayerContainerXml(LockedXmlTraits):
    """The XML serialization of the layer collection information."""

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
