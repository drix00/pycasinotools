#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import logging

# Third party modules.

# Local modules.
import SimulationParameters

# Globals and constants variables.

class CasinoSimulationExperiment(dict):
    def __init__(self, names, values):
        self._keywords = [SimulationParameters.FILENAMES,
                          SimulationParameters.ERASE_ALL_SCANPOINTS,
                          SimulationParameters.SCAN_POINT_FILES,
                          SimulationParameters.SCAN_POINT,
                          SimulationParameters.ENERGIES,
                          SimulationParameters.BEAM_RADIUS_nm,
                          SimulationParameters.SEMI_ANGLES_rad,
                          SimulationParameters.SPHERE_RADIUS_nm,
                          SimulationParameters.SPHERE_POSITION_Z_nm,
                          SimulationParameters.PLANE_POSITION_Z_nm,
                          SimulationParameters.NUMBER_ELECTRONS,
                          SimulationParameters.FOCAL_PLANE_Z_LIST,
                          SimulationParameters.REPETITION,
                          SimulationParameters.TOTAL_CROSS_SECTION,
                          SimulationParameters.PARTIAL_CROSS_SECTION,
                          SimulationParameters.SECONDARY_ELECTRON]

        self._createFormatList()

        for name, value in zip(names, values):
            self[name] = value

        self._checkKeywords()

    def _createFormatList(self):
        self._formatList = {}
        self._formatList[SimulationParameters.ENERGIES] = ("E", "%s", _convertEnergy, "keV")
        self._formatList[SimulationParameters.FILENAMES] = ("", "%s", _removeExtension, "")
        self._formatList[SimulationParameters.ERASE_ALL_SCANPOINTS] = ("", "%s", str, "")
        self._formatList[SimulationParameters.SCAN_POINT_FILES] = ("", "%s", _convertScanPointsFile, "")
        self._formatList[SimulationParameters.SCAN_POINT] = ("", "%s", _convertScanPoint, "")
        self._formatList[SimulationParameters.NUMBER_ELECTRONS] = ("N", "%s", _convertNumberElectron, "e")
        self._formatList[SimulationParameters.FOCAL_PLANE_Z_LIST] = ("fz", "%s", _convertFocalPlaneZ, "nm")
        self._formatList[SimulationParameters.BEAM_RADIUS_nm] = ("br", "%0.2f", float, "nm")
        self._formatList[SimulationParameters.SEMI_ANGLES_rad] = ("a", "%s", _convert_rad2mrad, "mrad")
        self._formatList[SimulationParameters.SPHERE_RADIUS_nm] = ("sr", "%s", _convertNumber, "nm")
        self._formatList[SimulationParameters.SPHERE_POSITION_Z_nm] = ("pz", "%s", _convertNumber, "nm")
        self._formatList[SimulationParameters.PLANE_POSITION_Z_nm] = ("pz", "%s", _convertNumber, "nm")
        self._formatList[SimulationParameters.REPETITION] = ("Id", "%s", str, "X")
        self._formatList[SimulationParameters.TOTAL_CROSS_SECTION] = ("TCS", "%s", str, "")
        self._formatList[SimulationParameters.PARTIAL_CROSS_SECTION] = ("PCS", "%s", str, "")
        self._formatList[SimulationParameters.SECONDARY_ELECTRON] = ("", "%s", _convertSE, "")

    def _checkKeywords(self):
        keywords = self.keys()

        for keyword in keywords:
            if type(keyword) == tuple:
                keyword = keyword[0]
            if keyword not in self._formatList:
                logging.warning("No format data for keyword: %s", keyword)
            if keyword not in self._keywords:
                logging.warning("No order data for keyword: %s", keyword)

    def getName(self, basename="CasinoSimulationExperiment"):
        name = self._generateName(basename)
        return name

    def _generateName(self, basename):
        keywords = self._getKeywords()

        name = basename
        for keyword in keywords:
            text = ""
            if keyword == SimulationParameters.SPHERE_RADIUS_nm or keyword == SimulationParameters.SPHERE_POSITION_Z_nm or keyword == SimulationParameters.PLANE_POSITION_Z_nm:
                for keywordSelf in self:
                    if type(keywordSelf) == tuple:
                        if keyword == keywordSelf[0]:
                            prefix, format, conversion, suffix = self._formatList[keyword]
                            text = "_" + prefix + format % (conversion(self[keywordSelf])) + suffix
            elif keyword == SimulationParameters.ERASE_ALL_SCANPOINTS:
                continue
            elif keyword == SimulationParameters.SCAN_POINT_FILES:
                continue
            else:
                if keyword in self:
                    prefix, format, conversion, suffix = self._formatList[keyword]
                    text = "_" + prefix + format % (conversion(self[keyword])) + suffix
                    if keyword == SimulationParameters.FILENAMES:
                        if basename != '' and basename in text:
                            text = text.replace("_"+basename, '')

            name += text

        if basename == "":
                name = name[1:]
        return name

    def _getKeywords(self):
        if len(self._keywords) > 0:
            return self._keywords
        else:
            return sorted(self.keys())

    def getFilename(self):
        return self[SimulationParameters.FILENAMES]

    def generateEnergyLabel(self, value):
        keyword = SimulationParameters.ENERGIES
        prefix, format, conversion, suffix = self._formatList[keyword]
        label = prefix + format % (conversion(value)) + suffix
        return label

    def generateNumberElectronsLabel(self, value):
        keyword = SimulationParameters.NUMBER_ELECTRONS
        prefix, format, conversion, suffix = self._formatList[keyword]
        label = prefix + format % (conversion(value)) + suffix
        return label

def _convertEnergy(energy_keV):
    return "%s" % (energy_keV)

def _removeExtension(filepath):
    basename, dummyExtension = os.path.splitext(filepath)
    return basename

def _convertScanPointsFile(filepath):
    basename = _removeExtension(filepath)
    basename = os.path.basename(basename)
    basename = basename.replace("ScanPointsScript_", "")
    return basename

def _convertScanPoint(scanPoint):
    assert len(scanPoint) == 3

    text = ""
    text += "fx%+.1fnm" % (scanPoint[0])
    text += "_fy%+.1fnm" % (scanPoint[1])
    text += "_fz%+.1fnm" % (scanPoint[2])

    return text

def _convertNumberElectron(numberElectrons):
    if numberElectrons < 1.0e3:
        return "%i" % (numberElectrons)
    elif numberElectrons < 1.0e6 and (numberElectrons % 1000) == 0:
        return "%ik" % (numberElectrons*1.0e-3)
    elif numberElectrons < 1.0e9 and (numberElectrons % 1000000) == 0:
        return "%iM" % (numberElectrons*1.0e-6)
    else:
        logging.debug("Not rule for converting number of electrons: %i", numberElectrons)
        return "%i" % (numberElectrons)

def _convertSE(value):
    if value == True:
        return "wSE"
    elif value == False:
        return "woSE"

def _convertFocalPlaneZ(focalPlaneZ):
    return "%+.1f" % focalPlaneZ

def _convertNumber(value):
    if type(value) == float:
        return "%f" % value
    else:
        return "%i"    % value

def _convert_rad2mrad(value):
    if type(value) == float:
        return "%.1f" % (value*1.0e3)
    else:
        return "%i"    % (int(value*1.0e3))
