#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import logging
import os.path

# Third party modules.
import numpy as np

# Local modules.

# Globals and constants variables.

class BasePattern(object):
    def __init__(self):
        self._scanPoints = []

        self._initData()

    def _initData(self):
        raise NotImplementedError

    def getScanPoints(self):
        self._generateScanPoints()
        return self._scanPoints

    def setScanPoints(self, scanPoints):
        self._scanPoints = scanPoints

    def addScanPoints(self, scanPoints):
        self._scanPoints.extend(scanPoints)

    def addScanPoint(self, scanPoint):
        self._scanPoints.append(scanPoint)

    def reset(self):
        self._scanPoints = []

    def write(self, filepath, generateScanPoints=True, overwrite=True):
        if not os.path.isfile(filepath) or overwrite:
            lines = self._generateLines(generateScanPoints)

            outputFile = open(filepath, 'wb')
            outputFile.writelines(lines)
            outputFile.close()
            del outputFile

    def _generateLines(self, generateScanPoints=True):
        if generateScanPoints:
            self._generateScanPoints()

        if len(self._scanPoints) == 0:
            logging.error("Empty scan points list.")
            return []

        self._uniqueScanPoints()

        lines = self._generateLinesImplemetation()
        return lines

    def _generateLinesImplemetation(self):
        raise NotImplementedError

    def _generateScanPoints(self):
        raise NotImplementedError

    def _uniqueScanPoints(self):
        uniqueScanPoints = set(self._scanPoints)
        self._scanPoints = sorted(uniqueScanPoints)

    def _getRange_nm(self, width, step, centerPosition):
        minimum = -width / 2.0 + centerPosition
        maximum = width / 2.0 + centerPosition

        range = np.arange(minimum, maximum + step, step)

        return range

    def getNumberPoints(self):
        self._generateScanPoints()
        return len(self._scanPoints)

