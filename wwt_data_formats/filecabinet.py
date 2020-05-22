# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
FileCabinetReader
FileCabinetWriter
'''.split()

from collections import namedtuple, OrderedDict
from xml.etree import ElementTree as etree

from . import stringify_xml_doc

ReaderFileInfo = namedtuple('ReaderFileInfo', 'name offset size')


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
        # searching for the text of the form `HeaderSize="0x000001b2"`.
        # TODO: explicit handling if the magic string isn't found or if the
        # header size is implausible.

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

            # TODO: handle names with bad characters, implausible offsets and sizes, etc.

            if name in self._files:
                raise Exception('duplicated File record "{}" in FileCabinet'.format(name))

            self._files[name] = ReaderFileInfo(name, header_size + rel_offset, size)


    def close(self):
        """Close the underlying stream, making this object essentially unusable."""
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


WriterFileInfo = namedtuple('WriterFileInfo', 'name size contents')


class FileCabinetWriter(object):
    """Writer for a simple container format for other files.

    One day, we should support the ability to stream data into a cabinet
    without having to grossly buffer everything in memory. But today is not
    that day.

    """
    _files = None

    def __init__(self):
        self._files = OrderedDict()


    def add_file_with_data(self, name, data):
        """Add a file whose contents are stored in an in-memory buffer.

        The *data* argument should be a bytes object.

        """
        if not isinstance(data, bytes):
            raise ValueError('the data argument must be an instance of the bytes type')

        if name in self._files:
            raise ValueError('a file named \"{}\" has already been added'.format(name))

        size = len(data)
        self._files[name] = WriterFileInfo(name, size, data)


    def filenames(self):
        """Return an iterable of the names of the files in this cabinet."""
        return self._files.keys()


    def emit(self, stream):
        """Write out the contents of this cabinet to the target stream.

        """
        # Create the header structure.

        SIZE_PLACEHOLDER = '0xZYXWVUTS'
        cabinet = etree.Element('FileCabinet')
        cabinet.set('HeaderSize', SIZE_PLACEHOLDER)

        files = etree.SubElement(cabinet, 'Files')
        offset = 0

        for info in self._files.values():
            f = etree.SubElement(files, 'File')
            f.set('Name', info.name)
            f.set('Size', str(info.size))
            f.set('Offset', str(offset))
            offset += info.size

        # Serialize and patch in the actual header size. With a
        # non-pathological XML serialization, the HeaderSize item will occur
        # within the first SIZE_REGION bytes while the first filename will
        # occur beyond the first SIZE_REGION bytes, meaning that we'll be
        # resistant if someone tries to break us by using a filename that
        # includes SIZE_PLACEHOLDER.

        SIZE_REGION = 90
        header = stringify_xml_doc(cabinet, indent=True)
        header = header.encode('utf-8')
        size_ascii = '0x{:08x}'.format(len(header)).encode('us-ascii')
        filled_size = header[:SIZE_REGION].replace(SIZE_PLACEHOLDER.encode('us-ascii'), size_ascii)
        header = filled_size + header[SIZE_REGION:]

        stream.write(header)

        # The rest is straightforward.

        for info in self._files.values():
            stream.write(info.contents)
