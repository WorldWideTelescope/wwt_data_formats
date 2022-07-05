# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the .NET Foundation
# Licensed under the MIT License.

from .. import enums


def test_dst_numerics():
    """
    This is a kind of silly test-that-I-copy-pasted-correctly test, but the
    intended numerics Just Are What They Are, so I'm not sure what else to do.
    """
    assert enums.DataSetType.EARTH.to_numeric() == 0
    assert enums.DataSetType.PLANET.to_numeric() == 1
    assert enums.DataSetType.SKY.to_numeric() == 2
    assert enums.DataSetType.PANORAMA.to_numeric() == 3
    assert enums.DataSetType.SOLAR_SYSTEM.to_numeric() == 4
    assert enums.DataSetType.SANDBOX.to_numeric() == 5


def test_projection_numerics():
    assert enums.ProjectionType.MERCATOR.to_numeric() == 0
    assert enums.ProjectionType.EQUIRECTANGULAR.to_numeric() == 1
    assert enums.ProjectionType.TAN.to_numeric() == 2
    assert enums.ProjectionType.TOAST.to_numeric() == 3
    assert enums.ProjectionType.SPHERICAL.to_numeric() == 4
    assert enums.ProjectionType.SKY_IMAGE.to_numeric() == 5
    assert enums.ProjectionType.PLOTTED.to_numeric() == 6
    assert enums.ProjectionType.HEALPIX.to_numeric() == 7
