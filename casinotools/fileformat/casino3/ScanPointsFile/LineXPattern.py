#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.ScanPointsFile.BasePattern as BasePattern

# Globals and constants variables.

class LineXPattern(BasePattern.BasePattern):
    def _initData(self):
        self._range_nm = 10.0
        self._step_nm = 5.0
        self._centerPoint_nm = (0.0, 0.0)

    def setRange_nm(self, range_nm):
        self._range_nm = range_nm

    def setStep_nm(self, step_nm):
        self._step_nm = step_nm

    def setCenterPoint_nm(self, centerPoint_nm):
        self._centerPoint_nm = centerPoint_nm

    def generateFilename(self, basename):
        filename = "%s.txt" % (basename)

        return filename

    def _generateScanPoints(self):
        y = self._centerPoint_nm[1]
        self._scanPoints = []
        for x in self._getRangeX_nm():
            point = (x, y)
            self._scanPoints.append(point)

    def _getRangeX_nm(self):
        step_nm = self._step_nm
        return self._getRange_nm(self._range_nm, step_nm, self._centerPoint_nm[0])
