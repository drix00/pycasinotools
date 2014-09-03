#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.
ENERGIES = "Energies"
NUMBER_ELECTRONS = "NumberElectrons"
FILENAMES = "Filenames"
SCAN_POINT_FILES = "scanPointFiles"
SCAN_POINT = "scanPoint"
ERASE_ALL_SCANPOINTS = "eraseAllScanpoints"
FOCAL_PLANE_Z_LIST = "FocalPlaneZList"
SEMI_ANGLES_rad = "SemiAngles_rad"
BEAM_RADIUS_nm = "BeamRadius_nm"
SPHERE_RADIUS_nm = "SphereRadius_nm"
SPHERE_POSITION_Z_nm = "SpherePositionZ"
PLANE_POSITION_Z_nm = "PlanePositionZ"
REPETITION = "Repetition"
TOTAL_CROSS_SECTION = "TotalCrossSection"
PARTIAL_CROSS_SECTION = "PartialCrossSection"
SECONDARY_ELECTRON = "secondaryElectron"
FOCAL_POSITION_Z_nm = "focalPositionZ_nm"

class SimulationParameters(dict):
    def __init__(self):
        self._keywords = set()

    def setBasename(self, basename):
        self._basename = basename

    def getBasename(self):
        return self._basename

    def setEnergies(self, values):
        self._set(ENERGIES, values)

    def getEnergies(self):
        return self[ENERGIES]

    def setNumberElectrons(self, values):
        self._set(NUMBER_ELECTRONS, values)

    def getNumberElectrons(self):
        return self[NUMBER_ELECTRONS]

    def setFilenames(self, values):
        self._set(FILENAMES, values)

    def getFilenames(self):
        return self[FILENAMES]

    def setScanPointFiles(self, values):
        self._set(SCAN_POINT_FILES, values)

    def getScanPointFiles(self):
        return self[SCAN_POINT_FILES]

    def setScanPointList(self, values):
        self._set(SCAN_POINT, values)

    def getScanPointList(self):
        return self[SCAN_POINT]

    def setSemiAngles_mrad(self, values):
        values = [value*1.0e-3 for value in values]
        self._set(SEMI_ANGLES_rad, values)

    def getSemiAngles_mrad(self):
        values = [value*1.0e3 for value in self[SEMI_ANGLES_rad]]
        return values

    def setBeamDiameters_nm(self, values):
        values = [value/2.0 for value in values]
        self._set(BEAM_RADIUS_nm, values)

    def getBeamDiameters_nm(self):
        values = [value*2.0 for value in self[BEAM_RADIUS_nm]]
        return values

    def setBeamRadius_nm(self, values):
        values = [value for value in values]
        self._set(BEAM_RADIUS_nm, values)

    def getBeamRadius_nm(self):
        values = [value for value in self[BEAM_RADIUS_nm]]
        return values

    def setSphereRadius_nm(self, shapeName, values):
        self._set((SPHERE_RADIUS_nm, shapeName), values)

    def getSphereRadius_nm(self, shapeName):
        return self[(SPHERE_RADIUS_nm, shapeName)]

    def setSpherePositionZs_nm(self, shapeName, values):
        self._set((SPHERE_POSITION_Z_nm, shapeName), values)

    def getSpherePositionZs_nm(self, shapeName):
        return self[(SPHERE_POSITION_Z_nm, shapeName)]

    def setPlanePositionZs_nm(self, shapeName, values):
        self._set((PLANE_POSITION_Z_nm, shapeName), values)

    def getPlanePositionZs_nm(self, shapeName):
        return self[(PLANE_POSITION_Z_nm, shapeName)]

    def setRepetition(self, repetition):
        repetitionStr = "%s" % (repetition)
        size = len(repetitionStr)
        format = "%%0%ii" % (size)
        values = [format % (i) for i in range(1,repetition+1)]
        self._set(REPETITION, values)

    def getRepetition(self):
        return self[REPETITION]

    def setCrossSection(self, values):
        self._set(TOTAL_CROSS_SECTION, values)
        self._set(PARTIAL_CROSS_SECTION, values)

    def getTotalCrossSection(self):
        return self[TOTAL_CROSS_SECTION]

    def getPartialCrossSection(self):
        return self[PARTIAL_CROSS_SECTION]

    def setSecondaryElectrons(self, values):
        self._set(SECONDARY_ELECTRON, values)

    def setSecondaryElectron(self, value):
        self._set(SECONDARY_ELECTRON, int(value))

    def getSecondaryElectrons(self):
        return self[SECONDARY_ELECTRON]

    def setFocalPositionZ_nm(self, value):
        self._set(FOCAL_PLANE_Z_LIST, value)

    def _set(self, keyword, values):
        try:
            len(values)
        except TypeError:
            values = [values]

        self[keyword] = list(values)
        self._keywords.add(keyword)
