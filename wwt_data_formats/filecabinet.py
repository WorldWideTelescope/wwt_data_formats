# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the AAS WorldWide Telescope project
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
FileCabinetReader
'''.split()

from collections import namedtuple
from xml.etree import ElementTree as etree

FileInfo = namedtuple('FileInfo', 'name offset size')


class FileCabinetReader(object):
    """Reader for a simple container format for other files.

    Unlike most of the other WWT data formats implemented in this package, the
    file cabinet is not an XML serialization of a data structure. Instead,
    it's a container format for bundling files together.

    """
    _stream = None
    _files = None

    def __init__(self, stream):
        self._stream = stream
        self._files = {}

        # We assume that the stream is going to be accessed randomly. There
        # might be cases in which the access is sequential, in which case we
        # could avoid the seeks and operate on pipes and the like, but we'll
        # cross that bridge if/when we get there -- this format is simple.

        stream.seek(0)

        # It seems safest to figure out the bounds of the header by
        # searching for the text of the form `HeaderSize="0x000001b2"`

        header = stream.read(256)
        idx = header.index(b'HeaderSize="')
        size_hex = header[idx+12:idx+22]
        header_size = int(size_hex, 16)

        # Now we can read the full header and parse it.

        stream.seek(0)
        header = stream.read(header_size)
        header_doc = etree.fromstring(header)

        for file in header_doc.find('Files').iterfind('File'):
            name = file.get('Name')
            rel_offset = file.get('Offset')
            size = file.get('Size')

            if name is None or rel_offset is None or size is None:
                raise Exception('incomplete File record in FileCabinet')

            try:
                rel_offset = int(rel_offset)
                size = int(size)
            except Exception as e:
                raise Exception('malformed Offset or Size in File record in FileCabinet')

            if name in self._files:
                raise Exception('duplicated File record "{}" in FileCabinet'.format(name))

            self._files[name] = FileInfo(name, header_size + rel_offset, size)


    def close(self):
        """Close the underlying stream. Make this object essentially unusable."""
        self._stream.close()
        self._stream = None


    def filenames(self):
        """Return an iterable of the names of the files in this cabinet."""
        return self._files.keys()


    def read_file(self, filename):
        """Read the specified file into memory in its entirety and return its contents.

        Returns bytes.
        """
        if self._stream is None:
            raise Exception('cannot read file "{}" with a closed FileCabinetReader'.format(filename))

        info = self._files.get(filename)
        if info is None:
            raise Exception('no such file "{}" in FileCabinet'.format(filename))

        self._stream.seek(info.offset)
        return self._stream.read(info.size)
