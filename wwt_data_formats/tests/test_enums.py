# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the .NET Foundation
# Licensed under the MIT License.

import pytest

from .. import enums


def test_classification_numerics():
    """
    This is a kind of silly test-that-I-copy-pasted-correctly test, but the
    intended numerics Just Are What They Are, so I'm not sure what else to do.
    """
    assert enums.Classification.STAR.to_numeric() == 1 << 0
    assert enums.Classification.SUPERNOVA.to_numeric() == 1 << 1
    assert enums.Classification.BLACK_HOLE.to_numeric() == 1 << 2
    assert enums.Classification.NEUTRON_STAR.to_numeric() == 1 << 3
    assert enums.Classification.DOUBLE_STAR.to_numeric() == 1 << 4
    assert enums.Classification.MULTIPLE_STARS.to_numeric() == 1 << 5
    assert enums.Classification.ASTERISM.to_numeric() == 1 << 6
    assert enums.Classification.CONSTELLATION.to_numeric() == 1 << 7
    assert enums.Classification.OPEN_CLUSTER.to_numeric() == 1 << 8
    assert enums.Classification.GLOBULAR_CLUSTER.to_numeric() == 1 << 9
    assert enums.Classification.NEBULOUS_CLUSTER.to_numeric() == 1 << 10
    assert enums.Classification.NEBULA.to_numeric() == 1 << 11
    assert enums.Classification.EMISSION_NEBULA.to_numeric() == 1 << 12
    assert enums.Classification.PLANETARY_NEBULA.to_numeric() == 1 << 13
    assert enums.Classification.REFLECTION_NEBULA.to_numeric() == 1 << 14
    assert enums.Classification.DARK_NEBULA.to_numeric() == 1 << 15
    assert enums.Classification.GIANT_MOLECULAR_CLOUD.to_numeric() == 1 << 16
    assert enums.Classification.SUPERNOVA_REMNANT.to_numeric() == 1 << 17
    assert enums.Classification.INTERSTELLAR_DUST.to_numeric() == 1 << 18
    assert enums.Classification.QUASAR.to_numeric() == 1 << 19
    assert enums.Classification.GALAXY.to_numeric() == 1 << 20
    assert enums.Classification.SPIRAL_GALAXY.to_numeric() == 1 << 21
    assert enums.Classification.IRREGULAR_GALAXY.to_numeric() == 1 << 22
    assert enums.Classification.ELLIPTICAL_GALAXY.to_numeric() == 1 << 23
    assert enums.Classification.KNOT.to_numeric() == 1 << 24
    assert enums.Classification.PLATE_DEFECT.to_numeric() == 1 << 25
    assert enums.Classification.CLUSTER_OF_GALAXIES.to_numeric() == 1 << 26
    assert enums.Classification.OTHER_NGC.to_numeric() == 1 << 27
    assert enums.Classification.UNIDENTIFIED.to_numeric() == 1 << 28
    assert enums.Classification.SOLAR_SYSTEM.to_numeric() == 1 << 29

    with pytest.raises(ValueError):
        enums.Classification.UNFILTERED.to_numeric()

    with pytest.raises(ValueError):
        enums.Classification.STELLAR.to_numeric()

    with pytest.raises(ValueError):
        enums.Classification.STELLAR_GROUPINGS.to_numeric()

    with pytest.raises(ValueError):
        enums.Classification.NEBULAE.to_numeric()

    with pytest.raises(ValueError):
        enums.Classification.GALACTIC.to_numeric()

    with pytest.raises(ValueError):
        enums.Classification.OTHER.to_numeric()


def test_dst_numerics():
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
