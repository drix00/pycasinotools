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

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.ScanPointsFile.BasePattern as BasePattern
import casinotools.fileformat.casino3.ScanPointsFile.RectanglePattern as RectanglePattern

# Globals and constants variables.

class LinesPattern(BasePattern.BasePattern):
    def _initData(self):
        self._lineSpacing_nm = 10.0
        self._lineWidth_nm = 10.0
        self._lineHeight_nm = 100.0
        self._beamStep_nm = 5.0
        self._numberLines = 1
        self._centerPoint_nm = (0.0, 0.0)

    def setLineSpacing_nm(self, lineSpacing_nm):
        self._lineSpacing_nm = lineSpacing_nm

    def setLineWidth_nm(self, lineWidth_nm):
        self._lineWidth_nm = lineWidth_nm

    def setLineHeight_nm(self, lineHeight_nm):
        self._lineHeight_nm = lineHeight_nm

    def setBeamStep_nm(self, beamStep_nm):
        self._beamStep_nm = beamStep_nm

    def setNumberLines(self, numberLines):
        if numberLines % 2 == 0:
            numberLines += 1
            logging.warning("Number of lines need to by odd, set to %i", numberLines)

        self._numberLines = numberLines

    def setCenterPoint_nm(self, centerPoint_nm):
        self._centerPoint_nm = centerPoint_nm

    def generateFilename(self, basename):
        filename = "%s.txt" % (basename)

        return filename

    def _generateScanPoints(self):
        rectangle = RectanglePattern.RectanglePattern()
        rectangle.setWidth_nm(self._lineWidth_nm)
        rectangle.setHeight_nm(self._lineHeight_nm)
        rectangle.setBeamStep_nm(self._beamStep_nm)
        rectangle.setCenterPoint_nm(self._centerPoint_nm)

        self.addScanPoints(rectangle.getScanPoints())

        numberLinesLeft = (self._numberLines - 1) / 2
        numberLinesRight = (self._numberLines - 1) / 2

        for index in range(1, numberLinesRight + 1, 1):
            x_nm, y_nm = self._centerPoint_nm
            x_nm += index * (self._lineSpacing_nm + self._lineWidth_nm)
            centerPoint_nm = x_nm, y_nm
            rectangle.setCenterPoint_nm(centerPoint_nm)
            self.addScanPoints(rectangle.getScanPoints())

        for index in range(1, numberLinesLeft + 1, 1):
            x_nm, y_nm = self._centerPoint_nm
            x_nm -= index * (self._lineSpacing_nm + self._lineWidth_nm)
            centerPoint_nm = x_nm, y_nm
            rectangle.setCenterPoint_nm(centerPoint_nm)
            self.addScanPoints(rectangle.getScanPoints())
