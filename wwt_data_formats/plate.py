# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the .NET Foundation
# Licensed under the MIT License.

"""The "plate" container formats for binary files.

"Plate files" are used in some parts of WWT to assemble large numbers of small
files into one big file. In particular, most of the original core WWT tile data
assets are compiled into plate files.

There are three variants of the plate file format. The oldest variant (let's
call it V0) needs external information in order to be read correctly and is not
yet supported here.

The next version (let's call it V1) has an eight-byte header followed by all
file location information in a fixed structure. Offsets are 32 bits, and so the
total file size is limited to 4 GiB. The densely-populated header is not
efficient for sparsely-populated tile pyramids. The reference implementation for
the V1 format is in `PlateTilePyramid.cs`_.

.. _PlateTilePyramid.cs: https://github.com/WorldWideTelescope/wwt-website/blob/master/src/WWT.PlateFiles/PlateTilePyramid.cs

The last version (V2) uses a hash table format. The V2 format is more efficient
for sparsely-populated tile pyramids, and supports files that are (much) larger
than 4 GiB. The reference implementation for the V2 format is in
`PlateFile2.cs`_. The V2 format is used by WWT's HiRISE data.

.. _PlateFile2.cs: https://github.com/WorldWideTelescope/wwt-website/blob/master/src/WWT.PlateFiles/PlateFile2.cs

"""

__all__ = """
V1PlateReader
V1PlateWriter
""".split()

from io import BytesIO
from struct import pack, unpack
from typing import BinaryIO, List


class V1PlateReader(object):
    """Reader for the "V1" WWT plate file format.

    Parameters
    ----------
    stream : readable, seekable, bytes-based file-like object
        The underlying data stream. If you explicitly :meth:`close` this object,
        it will close the underlying stream.

    Notes
    -----
    Unlike most of the other WWT data formats implemented in this package, plate
    files are stored in a simple binary structure, not XML."""

    _stream: BinaryIO
    _levels: int

    def __init__(self, stream: BinaryIO):
        self._stream = stream

        # We must have random access to the stream.
        stream.seek(0)
        magic, levels = unpack("<II", stream.read(8))

        if magic != 0x7E69AD43:
            if magic == 0x17914242:
                raise Exception("input stream is a V2 plate file, not V1")
            raise Exception("input stream does not look like a V1 plate file (nor V2)")

        self._levels = levels

    def close(self):
        """Close the underlying stream, making this object essentially unusable."""
        if self._stream is not None:
            self._stream.close()
            self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()
        return False

    def read_tile(self, level: int, x: int, y: int) -> bytes:
        """Read the specified tile position into memory in its entirety and
        return its contents.

        Parameters
        ----------
        level : int
            The level of the tile to read
        x : int
            The X position of the tile to read
        y : int
            The Y position of the tile to read

        Returns
        -------
        data : bytes
            The data for the specified tile position."""

        if self._stream is None:
            raise Exception("cannot read a closed V1PlateReader")

        if level < 0 or level > self._levels:
            raise ValueError(f"invalid `level` {level}")

        n = 2**level

        if x < 0 or x >= n or y < 0 or y >= n:
            raise ValueError(f"invalid tile position L{level}X{x}Y{y}")

        # This is the total number of tiles in all levels from 0 to `level - 1`,
        # plus one to account for the header item:
        index = (4**level - 1) // 3 + 1

        # The offset of this tile within the level:
        index += n * y + x

        self._stream.seek(8 * index)
        offset, length = unpack("<II", self._stream.read(8))

        self._stream.seek(offset)
        return self._stream.read(length)


class V1PlateWriter(object):
    """Writer for the "V1" WWT plate file format.

    Parameters
    ----------
    stream : writeable, seekable, bytes-based file-like object
        The underlying data destination. This object becomes responsible for
        closing the stream.
    levels : int
        The number of tile levels to allocate for this plate file. Must be
        nonnegative.

    Notes
    -----
    This file format assumes that tile data will be densely populated up to the
    specified number of levels (although missing entries are allowed). The
    maximum final file size is 4 GiB.

    This object is usable as a context manager, and should be explicitly closed.

    Unlike most of the other WWT data formats implemented in this package, plate
    files are stored in a simple binary structure, not XML."""

    _stream: BinaryIO
    _levels: int
    _next_offset: int
    _filedata: List[bytes]

    def __init__(self, stream: BinaryIO, levels: int):
        self._stream = stream
        self._levels = levels

        if levels < 0:
            raise ValueError(f"illegal `levels` value {levels!r}")

        # We must have random access to the stream.
        stream.seek(0)
        stream.write(pack("<II", 0x7E69AD43, levels))

        # Total number of tiles in all levels:
        n_tiles = (4 ** (levels + 1) - 1) // 3

        # Default all tiles to empty:
        self._filedata = [pack("<II", 0, 0)] * n_tiles

        # Reserve space for the file data (and the 8 header bytes):
        self._next_offset = (n_tiles + 1) * 8
        stream.seek(self._next_offset)

    def close(self):
        """Close the writer.

        This writes out the index of tile data and closes
        the underlying stream, making this object unusable
        for future I/O."""

        if self._stream is None:
            return  # should only happen if we already close()d, which is OK

        self._stream.seek(8)

        for entry in self._filedata:
            self._stream.write(entry)

        self._stream.close()
        self._stream = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()
        return False

    def append_stream(self, level: int, x: int, y: int, stream: BinaryIO):
        """Append a tile to the plate file, getting data from a file-like
        object.

        Parameters
        ----------
        level : int
            The level of the tile to write
        x : int
            The X position of the tile to write
        y : int
            The Y position of the tile to write
        stream : readable, bytes-based file-like object
            The source of tile data.

        Returns
        -------
        length : int
            The number of bytes read from *stream* and written to the plate
            file.

        Notes
        -----
        This method reads *stream* until end of file, but does not take
        responsibility for closing it."""

        if self._stream is None:
            raise Exception("cannot write a closed V1PlateWriter")

        if level < 0 or level > self._levels:
            raise ValueError(f"invalid `level` {level}")

        n = 2**level

        if x < 0 or x >= n or y < 0 or y >= n:
            raise ValueError(f"invalid tile position L{level}X{x}Y{y}")

        if self._next_offset >= 4294967296:  # that's 2**32
            raise Exception(
                "cannot append to V1PlateWriter: 4-gibibyte size limit exceeded"
            )

        # This is basically `shutil.copyfileobj()`, but that doesn't tell
        # us the total length written.

        length = 0

        while True:
            b = stream.read(65536)
            if not b:
                break

            self._stream.write(b)
            length += len(b)

        if length >= 4294967296:  # that's 2**32
            raise Exception(
                "error appending to V1PlateWriter: 4-gibibyte file size limit exceeded"
            )

        # Now we can add the filedata entry.
        #
        # This is the total number of tiles in all levels from 0 to `level - 1`:
        index = (4**level - 1) // 3

        # The offset of this tile within the level:
        index += n * y + x

        self._filedata[index] = pack("<II", self._next_offset, length)
        self._next_offset += length
        return length

    def append_bytes(self, level: int, x: int, y: int, data: bytes):
        """Append a tile to the plate file, getting data from a bytes buffer.

        Parameters
        ----------
        level : int
            The level of the tile to write
        x : int
            The X position of the tile to write
        y : int
            The Y position of the tile to write
        data : bytes
            The tile data.

        Returns
        -------
        length : int
            The number of bytes written to the plate file, which is the length
            of *data*."""
        return self.append_stream(level, x, y, BytesIO(data))
