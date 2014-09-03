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
import casinotools.fileformat.casino3.ScanPointsFile.LineXPattern as LineXPattern

# Globals and constants variables.

class ImageXZPattern(BasePattern.BasePattern):
    def _initData(self):
        self.setStepX_nm(5.0)
        self.setRangeX_nm(10.0)
        self.setStepZ_nm(100.0)
        self.setRangeZ_nm(100.0)
        self.setCenterPoint_nm((0.0, 0.0))

    def setStepX_nm(self, step_nm):
            self._stepX_nm = step_nm

    def setRangeX_nm(self, range_nm):
            self._rangeX_nm = range_nm

    def setStepZ_nm(self, step_nm):
            self._stepZ_nm = step_nm

    def setRangeZ_nm(self, range_nm):
            self._rangeZ_nm = range_nm

    def setCenterPoint_nm(self, centerPoint_nm):
        self._centerPoint_nm = centerPoint_nm

    def generateFilename(self, basename):
        filename = "%s.txt" % (basename)

        return filename

    def _generateScanPoints(self):
            for z in self._getRangeZ():
                    line = LineXPattern.LineXPattern()
                    line.setRange_nm(self._rangeX_nm)
                    line.setStep_nm(self._stepX_nm)
                    lineCenterPoint = (self._centerPoint_nm[0], z)
                    line.setCenterPoint_nm(lineCenterPoint)

                    self.addScanPoints(line.getScanPoints())

    def _getRangeZ(self):
        step_nm = self._stepZ_nm
        return self._getRange_nm(self._rangeZ_nm, step_nm, self._centerPoint_nm[1])
