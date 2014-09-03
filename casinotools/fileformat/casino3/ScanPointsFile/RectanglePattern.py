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
import numpy as np

# Local modules.
import casinotools.fileformat.casino3.ScanPointsFile.BasePattern as BasePattern

# Globals and constants variables.

class RectanglePattern(BasePattern.BasePattern):
    def _initData(self):
        self.setNumberPoints(0)
        self.setWidth_nm(0)
        self.setHeight_nm(0)
        self.setCenterPoint_nm((0.0, 0.0))
        self._numberPointsY = None
        self._numberPointsZ = None

        self._separation_nm = None

    def setNumberPoints(self, value):
        self._numberPoints = int(value)

    def setWidth_nm(self, value, numberPoints=None):
        self._widthMax_nm = float(value)
        self._numberPointsY = numberPoints

    def setHeight_nm(self, value, numberPoints=None):
        self._heightMax_nm = float(value)
        self._numberPointsZ = numberPoints

    def setBeamStep_nm(self, beamStep_nm):
        self._beamStep_nm = beamStep_nm

    def setCenterPoint_nm(self, point_nm):
        assert len(point_nm) == 2
        self._centerPoint_nm = point_nm

    def _generateScanPoints(self):
            self.reset()
            for x in self._getRangeX_nm():
                for y in self._getRangeY_nm():
                    scanPoint = (x, y)
                    self.addScanPoint(scanPoint)

    def _getRangeX_nm(self):
        xSep = self._beamStep_nm
        xMin = -self._widthMax_nm / 2.0 + xSep / 2.0 + self._centerPoint_nm[0]
        xMax = self._widthMax_nm / 2.0 + xSep / 2.0 + self._centerPoint_nm[0]

        range_nm = np.arange(xMin, xMax, xSep)

        return range_nm

    def _getRangeY_nm(self):
        ySep = self._beamStep_nm
        yMin = -self._heightMax_nm / 2.0 + ySep / 2.0 + self._centerPoint_nm[1]
        yMax = self._heightMax_nm / 2.0 + ySep / 2.0 + self._centerPoint_nm[1]

        range_nm = np.arange(yMin, yMax, ySep)

        return range_nm
