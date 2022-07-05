# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Various enumerations

"""
from __future__ import absolute_import, division, print_function

__all__ = """
Bandpass
Classification
Constellation
DataSetType
FolderType
ProjectionType
SerEnum
""".split()

from enum import Enum


class SerEnum(Enum):
    """A helper for enumerations that are serialized and deserialized from text.
    In some WWT cases, multiple textualizations have historically been used
    for the same value.

    """

    @classmethod
    def from_text(cls, text):
        """The default implementation here just looks up the appropriate enum instance
        from its value.

        """
        return cls(text)


class Bandpass(SerEnum):
    GAMMA = "Gamma"
    XRAY = "XRay"
    ULTRAVIOLET = "Ultraviolet"
    VISIBLE = "Visible"
    HYDROGEN_ALPHA = "HydrogenAlpha"
    INFRARED = "IR"
    MICROWAVE = "Microwave"
    RADIO = "Radio"
    VISIBLE_NIGHT = "VisibleNight"


class Classification(SerEnum):
    UNSPECIFIED = ""
    STAR = "Star"
    SUPERNOVA = "Supernova"
    BLACK_HOLE = "BlackHole"
    NEUTRON_STAR = "NeutronStar"
    DOUBLE_STAR = "DoubleStar"
    MULTIPLE_STARS = "MultipleStars"
    ASTERISM = "Asterism"
    CONSTELLATION = "Constellation"
    OPEN_CLUSTER = "OpenCluster"
    GLOBULAR_CLUSTER = "GlobularCluster"
    NEBULOUS_CLUSTER = "NebulousCluster"
    NEBULA = "Nebula"
    EMISSION_NEBULA = "EmissionNebula"
    PLANETARY_NEBULA = "PlanetaryNebula"
    REFLECTION_NEBULA = "ReflectionNebula"
    DARK_NEBULA = "DarkNebula"
    GIANT_MOLECULAR_CLOUD = "GiantMolecularCloud"
    SUPERNOVA_REMNANT = "SupernovaRemnant"
    INTERSTELLAR_DUST = "InterstellarDust"
    QUASAR = "Quasar"
    GALAXY = "Galaxy"
    SPIRAL_GALAXY = "SpiralGalaxy"
    IRREGULAR_GALAXY = "IrregularGalaxy"
    ELLIPTICAL_GALAXY = "EllipticalGalaxy"
    KNOT = "Knot"
    PLATE_DEFECT = "PlateDefect"
    CLUSTER_OF_GALAXIES = "ClusterOfGalaxies"
    OTHER_NGC = "OtherNGC"
    UNIDENTIFIED = "Unidentified"
    SOLAR_SYSTEM = "SolarSystem"

    # These are bitmasks for matching different broad categories numerically:

    UNFILTERED = "Unfiltered"  # 0x3FFF_FFFF = 1073741823; everything
    STELLAR = "Stellar"  # 0x0000_003F = 63
    STELLAR_GROUPINGS = "StellarGroupings"  # 0x0000_07F0 = 2032; overlaps STELLAR
    NEBULAE = "Nebulae"  # 0x0007_FC00 = 523264; overlaps STELLAR_GROUPINGS with NEBULOUS_CLUSTER
    GALACTIC = "Galactic"  # 0x07F8_0000 = 133693440
    OTHER = "Other"  # 0x1A00_0000 = 436207616

    def to_numeric(self):
        """
        Convert this Classification to its WWT-internal numeric expression.
        """
        v = _classification_to_numeric_map.get(self)
        if v is None:
            raise ValueError(
                f"cannot safely represent WWT Classification `{self}` numerically"
            )
        return v


_classification_to_numeric_map = {
    Classification.STAR: 1 << 0,
    Classification.SUPERNOVA: 1 << 1,
    Classification.BLACK_HOLE: 1 << 2,
    Classification.NEUTRON_STAR: 1 << 3,
    Classification.DOUBLE_STAR: 1 << 4,
    Classification.MULTIPLE_STARS: 1 << 5,
    Classification.ASTERISM: 1 << 6,
    Classification.CONSTELLATION: 1 << 7,
    Classification.OPEN_CLUSTER: 1 << 8,
    Classification.GLOBULAR_CLUSTER: 1 << 9,
    Classification.NEBULOUS_CLUSTER: 1 << 10,
    Classification.NEBULA: 1 << 11,
    Classification.EMISSION_NEBULA: 1 << 12,
    Classification.PLANETARY_NEBULA: 1 << 13,
    Classification.REFLECTION_NEBULA: 1 << 14,
    Classification.DARK_NEBULA: 1 << 15,
    Classification.GIANT_MOLECULAR_CLOUD: 1 << 16,
    Classification.SUPERNOVA_REMNANT: 1 << 17,
    Classification.INTERSTELLAR_DUST: 1 << 18,
    Classification.QUASAR: 1 << 19,
    Classification.GALAXY: 1 << 20,
    Classification.SPIRAL_GALAXY: 1 << 21,
    Classification.IRREGULAR_GALAXY: 1 << 22,
    Classification.ELLIPTICAL_GALAXY: 1 << 23,
    Classification.KNOT: 1 << 24,
    Classification.PLATE_DEFECT: 1 << 25,
    Classification.CLUSTER_OF_GALAXIES: 1 << 26,
    Classification.OTHER_NGC: 1 << 27,
    Classification.UNIDENTIFIED: 1 << 28,
    Classification.SOLAR_SYSTEM: 1 << 29,
}


class Constellation(SerEnum):
    UNSPECIFIED = ""
    ANDROMEDA = "AND"
    ANTLIA = "ANT"
    APUS = "APS"
    AQUARIUS = "AQR"
    AQUILA = "AQL"
    ARA = "ARA"
    ARIES = "ARI"
    AURIGA = "AUR"
    BOOTES = "BOO"
    CAELUM = "CAE"
    CAMELOPARDALIS = "CAM"
    CANCER = "CNC"
    CANES_VENATICI = "CVN"
    CANIS_MAJOR = "CMA"
    CANIS_MINOR = "CMI"
    CAPRICORNUS = "CAP"
    CARINA = "CAR"
    CASSIOPEIA = "CAS"
    CENTAURUS = "CEN"
    CEPHEUS = "CEP"
    CETUS = "CET"
    CHAMAELEON = "CHA"
    CIRCINUS = "CIR"
    COLUMBA = "COL"
    COMA_BERENICES = "COM"
    CORONA_AUSTRALIS = "CRA"
    CORONA_BOREALIS = "CRB"
    CORVUS = "CRV"
    CRATER = "CRT"
    CRUX = "CRU"
    CYGNUS = "CYG"
    DELPHINUS = "DEL"
    DORADO = "DOR"
    DRACO = "DRA"
    EQUULEUS = "EQU"
    ERIDANUS = "ERI"
    FORNAX = "FOR"
    GEMINI = "GEM"
    GRUS = "GRU"
    HERCULES = "HER"
    HOROLOGIUM = "HOR"
    HYDRA = "HYA"
    HYDRUS = "HYI"
    INDUS = "IND"
    LACERTA = "LAC"
    LEO = "LEO"
    LEO_MINOR = "LMI"
    LEPUS = "LEP"
    LIBRA = "LIB"
    LUPUS = "LUP"
    LYNX = "LYN"
    LYRA = "LYR"
    MENSA = "MEN"
    MICROSCOPIUM = "MIC"
    MONOCEROS = "MON"
    MUSCA = "MUS"
    NORMA = "NOR"
    OCTANS = "OCT"
    OPHIUCHUS = "OPH"
    ORION = "ORI"
    PAVO = "PAV"
    PEGASUS = "PEG"
    PERSEUS = "PER"
    PHOENIX = "PHE"
    PICTOR = "PIC"
    PISCES = "PSC"
    PISCIS_AUSTRINUS = "PSA"
    PUPPIS = "PUP"
    PYXIS = "PYX"
    RETICULUM = "RET"
    SAGITTA = "SGE"
    SAGITTARIUS = "SGR"
    SCORPIUS = "SCO"
    SCULPTOR = "SCL"
    SCUTUM = "SCT"
    SERPENS_CAPUT = "SER1"
    SERPENS_CAUDA = "SER2"
    SEXTANS = "SEX"
    TAURUS = "TAU"
    TELESCOPIUM = "TEL"
    TRIANGULUM = "TRI"
    TRIANGULUM_AUSTRALE = "TRA"
    TUCANA = "TUC"
    URSA_MAJOR = "UMA"
    URSA_MINOR = "UMI"
    VELA = "VEL"
    VIRGO = "VIR"
    VOLANS = "VOL"
    VULPECULA = "VUL"


class DataSetType(SerEnum):
    EARTH = "Earth"
    PLANET = "Planet"
    SKY = "Sky"
    PANORAMA = "Panorama"
    SOLAR_SYSTEM = "SolarSystem"
    SANDBOX = "Sandbox"

    def to_numeric(self):
        """
        Convert this DataSetType to its WWT-internal numeric expression.
        """
        return _datasettype_to_numeric_map[self]


# see `enum ImageSetType` in the C#
_datasettype_to_numeric_map = {
    DataSetType.EARTH: 0,
    DataSetType.PLANET: 1,
    DataSetType.SKY: 2,
    DataSetType.PANORAMA: 3,
    DataSetType.SOLAR_SYSTEM: 4,
    DataSetType.SANDBOX: 5,
}


class FolderType(SerEnum):
    UNSPECIFIED = ""
    EARTH = "Earth"
    PLANET = "Planet"
    SKY = "Sky"
    PANORAMA = "Panorama"


class ProjectionType(SerEnum):
    MERCATOR = "Mercator"
    EQUIRECTANGULAR = "Equirectangular"
    HEALPIX = "Healpix"
    TAN = "Tan"
    TOAST = "Toast"
    SPHERICAL = "Spherical"
    SKY_IMAGE = "SkyImage"
    PLOTTED = "Plotted"

    @classmethod
    def from_text(cls, text):
        if text == "Tangent":
            return cls.TAN
        return cls(text)

    def to_numeric(self):
        """
        Convert this ProjectionType to its WWT-internal numeric expression.
        """
        return _projectiontype_to_numeric_map[self]


# see `enum ProjectionType` in the C#
_projectiontype_to_numeric_map = {
    ProjectionType.MERCATOR: 0,
    ProjectionType.EQUIRECTANGULAR: 1,
    ProjectionType.TAN: 2,
    ProjectionType.TOAST: 3,
    ProjectionType.SPHERICAL: 4,
    ProjectionType.SKY_IMAGE: 5,
    ProjectionType.PLOTTED: 6,
    ProjectionType.HEALPIX: 7,
}
