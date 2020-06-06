# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Various enumerations

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
Bandpass
Classification
Constellation
DataSetType
FolderType
ProjectionType
SerEnum
'''.split()

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
    GAMMA = 'Gamma'
    XRAY = 'XRay'
    ULTRAVIOLET = 'Ultraviolet'
    VISIBLE = 'Visible'
    HYDROGEN_ALPHA = 'HydrogenAlpha'
    INFRARED = 'IR'
    MICROWAVE = 'Microwave'
    RADIO = 'Radio'
    VISIBLE_NIGHT = 'VisibleNight'


class Classification(SerEnum):
    UNSPECIFIED = ''
    STAR = 'Star'
    SUPERNOVA = 'Supernova'
    BLACKHOLE = 'BlackHole'
    NEUTRON_STAR = 'NeutronStar'
    DOUBLE_STAR = 'DoubleStar'
    MULTIPLE_STARS = 'MultipleStars'
    ASTERISM = 'Asterism'
    CONSTELLATION = 'Constellation'
    OPEN_CLUSTER = 'OpenCluster'
    GLOBULAR_CLUSTER = 'GlobularCluster'
    NEBULOUS_CLUSTER = 'NebulousCluster'
    NEBULA = 'Nebula'
    EMISSION_NEBULA = 'EmissionNebula'
    PLANETARY_NEBULA = 'PlanetaryNebula'
    REFLECTION_NEBULA = 'ReflectionNebula'
    DARK_NEBULA = 'DarkNebula'
    GIANT_MOLECULAR_CLOUD = 'GiantMolecularCloud'
    SUPERNOVA_REMNANT = 'SupernovaRemnant'
    INTERSTELLAR_DUST = 'InterstellarDust'
    QUASAR = 'Quasar'
    GALAXY = 'Galaxy'
    SPIRAL_GALAXY = 'SpiralGalaxy'
    IRREGULAR_GALAXY = 'IrregularGalaxy'
    ELLIPTICAL_GALAXY = 'EllipticalGalaxy'
    KNOT = 'Knot'
    PLATE_DEFECT = 'PlateDefect'
    CLUSTER_OF_GALAXIES = 'ClusterOfGalaxies'
    OTHER_NGC = 'OtherNGC'
    UNIDENTIFIED = 'Unidentified'
    SOLARS_YSTEM = 'SolarSystem'
    UNFILTERED = 'Unfiltered'
    STELLAR = 'Stellar'
    STELLAR_GROUPINGS = 'StellarGroupings'
    NEBULAE = 'Nebulae'
    GALACTIC = 'Galactic'
    OTHER = 'Other'

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
    EARTH = 'Earth'
    PLANET = 'Planet'
    SKY = 'Sky'
    PANORAMA = 'Panorama'
    SOLAR_SYSTEM = 'SolarSystem'
    SANDBOX = 'Sandbox'


class FolderType(SerEnum):
    UNSPECIFIED = ''
    EARTH = 'Earth'
    PLANET = 'Planet'
    SKY = 'Sky'
    PANORAMA = 'Panorama'


class ProjectionType(SerEnum):
    MERCATOR = 'Mercator'
    EQUIRECTANGULAR = 'Equirectangular'
    HEALPIX = 'Healpix'
    TAN = 'Tan'
    TOAST = 'Toast'
    SPHERICAL = 'Spherical'
    SKY_IMAGE = 'SkyImage'
    PLOTTED = 'Plotted'

    @classmethod
    def from_text(cls, text):
        if text == 'Tangent':
            return cls.TAN
        return cls(text)
