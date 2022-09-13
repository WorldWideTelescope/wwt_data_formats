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
""".split()

from struct import unpack


class V1PlateReader(object):
    """Reader for the "V1" plate file format.

    Unlike most of the other WWT data formats implemented in this package,
    plate files are stored in a simple binary structure, not XML."""

    _stream = None
    _levels: int

    def __init__(self, stream):
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
        self._stream.close()
        self._stream = None

    def read_tile(self, level, x, y):
        """Read the specified tile position into memory in its entirety and
        return its contents.

        Returns bytes."""

        if self._stream is None:
            raise Exception("cannot read a closed FileCabinetReader")

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
