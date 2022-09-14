# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the .NET Foundation
# Licensed under the MIT License.

import os
import pytest

from .. import plate
from . import work_in_tempdir


def test_basic_v1_plate(work_in_tempdir):
    with plate.V1PlateWriter(open("test.plate", "wb"), 1) as pw:
        assert pw.append_bytes(1, 1, 1, b"111") == 3
        assert pw.append_bytes(1, 1, 0, b"110") == 3
        assert pw.append_bytes(1, 0, 1, b"101") == 3
        assert pw.append_bytes(1, 0, 0, b"100") == 3
        assert pw.append_bytes(0, 0, 0, b"000") == 3

        pw.close()

        with pytest.raises(Exception):
            pw.append_bytes(0, 0, 0, b"000")

    # 8 bytes * (5 tiles + 1 header) + 3 bytes * 5 tiles =>
    assert os.stat("test.plate").st_size == 63

    with plate.V1PlateReader(open("test.plate", "rb")) as pr:
        assert pr.read_tile(1, 1, 1) == b"111"
        assert pr.read_tile(1, 1, 0) == b"110"
        assert pr.read_tile(1, 0, 1) == b"101"
        assert pr.read_tile(1, 0, 0) == b"100"
        assert pr.read_tile(0, 0, 0) == b"000"

        with pytest.raises(ValueError):
            pr.read_tile(-1, 0, 0)

        with pytest.raises(ValueError):
            pr.read_tile(2, 0, 0)

        with pytest.raises(ValueError):
            pr.read_tile(1, -1, 0)

        with pytest.raises(ValueError):
            pr.read_tile(1, 0, 2)

        pr.close()

        with pytest.raises(Exception):
            pr.read_tile(1, 0, 0)
