# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
Place
'''.split()

from xml.etree import ElementTree as etree


class Place(object):
    """A place that can be visited."""

    data_set_type = 'Earth'
    name = ''
    ra_hr = 0.0
    dec_deg = 0.0
    latitude = 0.0
    longitude = 0.0
    constellation = ''
    classification = ''
    magnitude = 0.0
    distance = 0.0
    angular_size = 0.0
    zoom_level = 0.0
    rotation_deg = 0.0
    angle = 0.0
    opacity = 100.0
    dome_alt = 0.0
    dome_az = 0.0
    description = ''
    background_image_set = None
    foreground_image_set = None
    image_set = None
    thumbnail = None
    msr_community_id = None
    msr_component_id = None
    permission = None

    def to_xml(self):
        """Seralize this object to XML.

        Returns
        -------
        elem : xml.etree.ElementTree.Element
          A ``Place`` XML element serializing the object.

        """
        place = etree.Element('Place')
        place.set('Name', self.name)
        place.set('DataSetType', self.data_set_type)
        place.set('RA', str(self.ra_hr))
        place.set('Dec', str(self.dec_deg))
        place.set('Lat', str(self.latitude))
        place.set('Lng', str(self.longitude))
        place.set('Constellation', self.constellation)
        place.set('Classification', self.classification)
        place.set('Magnitude', str(self.magnitude))
        place.set('Distance', str(self.distance))
        place.set('AngularSize', str(self.angular_size))
        place.set('ZoomLevel', str(self.zoom_level))
        place.set('Rotation', str(self.rotation_deg))
        place.set('Angle', str(self.angle))
        place.set('Opacity', str(self.opacity))
        place.set('DomeAlt', str(self.dome_alt))
        place.set('DomeAz', str(self.dome_az))

        if self.background_image_set is not None:
            wrapper = etree.SubElement(place, 'BackgroundImageSet')
            wrapper.append(self.background_image_set.to_xml())

        if self.foreground_image_set is not None:
            wrapper = etree.SubElement(place, 'ForegroundImageSet')
            wrapper.append(self.foreground_image_set.to_xml())

        if self.image_set is not None:
            place.append(self.image_set.to_xml())

        return place
