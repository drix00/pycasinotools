#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import math
import os

# Third party modules.
import numpy as np

# Local modules.
import casinotools.fileformat.casino3.ScanPointsFile.BasePattern as BasePattern

# Globals and constants variables.
LINESCAN_TYPE_X = "linescanTypeX"
LINESCAN_TYPE_XY = "linescanTypeXY"

class ScanPointsFile(BasePattern.BasePattern):
    def _initData(self):
        self.setNumberPoints(0)
        self.setWidth_nm(0)
        self.setHeight_nm(0)
        self.setCenterPoint((0.0, 0.0))
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

    def setCenterPoint(self, point):
        assert len(point) == 2
        self._centerPoint = point

    def _generateScanPoints(self):
        if self._heightMax_nm == 0.0:
            self._generateLinescanX()
        elif self._widthMax_nm == 0.0:
            self._generateLinescanY()
        else:
            self._generateAreascanXY()

    def _generateLinescanX(self):
        self._computeSeparationX_nm()

        y = self._centerPoint[1]
        self._scanPoints = []
        for x in self._getRangeX_nm():
            point = (x, y)
            self._scanPoints.append(point)

    def _generateLinescanY(self):
        self._computeSeparationY_nm()

        x = self._centerPoint[0]
        self._scanPoints = []
        for y in self._getRangeY_nm():
            point = (x, y)
            self._scanPoints.append(point)

    def _getRangeX_nm(self):
        xSep = self._separation_nm
        xMin = -self._widthMax_nm / 2.0 + xSep / 2.0 + self._centerPoint[0]
        xMax = self._widthMax_nm / 2.0 + xSep / 2.0 + self._centerPoint[0]

        range_nm = np.arange(xMin, xMax, xSep)

        return range_nm

    def _getRangeY_nm(self):
        ySep = self._separation_nm
        yMin = -self._heightMax_nm / 2.0 + ySep / 2.0 + self._centerPoint[1]
        yMax = self._heightMax_nm / 2.0 + ySep / 2.0 + self._centerPoint[1]

        range_nm = np.arange(yMin, yMax, ySep)

        return range_nm

    def _getRangeX2_nm(self):
        xSep = self._widthMax_nm / self._numberPointsY
        xMin = -self._widthMax_nm / 2.0 + xSep / 2.0 + self._centerPoint[0]
        xMax = self._widthMax_nm / 2.0 + xSep / 2.0 + self._centerPoint[0]

        range_nm = np.arange(xMin, xMax, xSep)

        return range_nm

    def _getRangeY2_nm(self):
        ySep = self._heightMax_nm / self._numberPointsZ
        yMin = -self._heightMax_nm / 2.0 + ySep / 2.0 + self._centerPoint[1]
        yMax = self._heightMax_nm / 2.0 + ySep / 2.0 + self._centerPoint[1]

        range_nm = np.arange(yMin, yMax, ySep)

        return range_nm

    def _generateAreascanXY(self):
        if self._numberPoints != 0:
            self._computeSeparation_nm()

            self._scanPoints = []
            for x in self._getRangeX_nm():
                for y in self._getRangeY_nm():
                    point = (x, y)
                    self._scanPoints.append(point)
        elif self._numberPointsY != None and self._numberPointsZ != None:
            self._scanPoints = []
            for x in self._getRangeX2_nm():
                for y in self._getRangeY2_nm():
                    point = (x, y)
                    self._scanPoints.append(point)
        else:
            raise NotImplementedError

    def _computeSeparationX_nm(self):
        if self._numberPoints == 0 and self._pixelSize_nm is not None:
            self._separation_nm = self._pixelSize_nm
        elif self._numberPoints != 0:
            self._separation_nm = self._widthMax_nm / self._numberPoints

    def _computeSeparationY_nm(self):
        if self._numberPoints == 0 and self._pixelSize_nm is not None:
            self._separation_nm = self._pixelSize_nm
        elif self._numberPoints != 0:
            self._separation_nm = self._heightMax_nm / self._numberPoints

    def _computeSeparation_nm(self):
        totalArea_nm2 = self._widthMax_nm * self._heightMax_nm
        pointArea_nm2 = totalArea_nm2 / self._numberPoints

        self._separation_nm = math.sqrt(pointArea_nm2)

    def _isLineValid(self, line):
        if len(line) == 0:
            return False

        if (line[-1] != os.linesep) and (line[-1] != "\n") and (line[-1] != "\r") and (line[-1] != "\r\n"):
            return False

        try:
            items = line.split(',')
            dummyNumber1 = float(items[0].strip())
            dummyNumber2 = float(items[1].strip())
        except:
            return False

        if len(line) > 30:
            return False

        return True

    def _generateLinesImplemetation(self):
        """
        Only two coordinates is used, for import in the CASINO GUI.
        """
        lines = []
        for point_nm in self._scanPoints:
            line = "%f, %f\n" % point_nm
            lines.append(line)

        return lines

class ScanPointsFileScript(ScanPointsFile):
    def _initData(self):
        self.setNumberPoints(0)
        self.setWidth_nm(0)
        self.setHeight_nm(0)
        self.setCenterPoint((0.0, 0.0, 0.0))
        self._numberPointsY = None
        self._numberPointsZ = None

        self._pixelSize_nm = None
        self._separation_nm = None

    def setCenterPoint(self, point):
        assert len(point) == 3
        self._centerPoint = point

    def setPixelSize_nm(self, pixelSize_nm):
        self._pixelSize_nm = pixelSize_nm

    def setLinescanX(self):
        if self._numberPoints == 0 and self._widthMax_nm != None:
            numberPoints = self._widthMax_nm / self._pixelSize_nm
            self.setNumberPoints(numberPoints)
        else:
            width_nm = self._pixelSize_nm * self._numberPoints
            self.setWidth_nm(width_nm)
            self.setHeight_nm(0)

    def setLinescanY(self):
        height_nm = self._pixelSize_nm * self._numberPoints
        self.setWidth_nm(0)
        self.setHeight_nm(height_nm)

    def setLinescanXY(self):
        numberPointsPerDirection = int(math.sqrt(self._numberPoints))

        height_nm = self._pixelSize_nm * numberPointsPerDirection
        width_nm = self._pixelSize_nm * numberPointsPerDirection
        self.setWidth_nm(width_nm)
        self.setHeight_nm(height_nm)

    def _generateLinescanX(self):
        self._computeSeparationX_nm()

        y = self._centerPoint[1]
        z = self._centerPoint[2]
        self._scanPoints = []
        for x in self._getRangeX_nm():
            point = (x, y, z)
            self._scanPoints.append(point)

    def _generateLinescanY(self):
        self._computeSeparationY_nm()

        x = self._centerPoint[0]
        z = self._centerPoint[2]
        self._scanPoints = []
        for y in self._getRangeY_nm():
            point = (x, y, z)
            self._scanPoints.append(point)

    def _generateAreascanXY(self):
        z = self._centerPoint[2]
        if self._numberPoints != 0:
            self._computeSeparation_nm()

            self._scanPoints = []
            for x in self._getRangeX_nm():
                for y in self._getRangeY_nm():
                    point = (x, y, z)
                    self._scanPoints.append(point)
        elif self._numberPointsY != None and self._numberPointsZ != None:
            self._scanPoints = []
            for x in self._getRangeX2_nm():
                for y in self._getRangeY2_nm():
                    point = (x, y, z)
                    self._scanPoints.append(point)
        else:
            raise NotImplementedError

    def _generateLinesImplemetation(self):
        """
        With three coordinates is used, for import in the CASINO script console.
        """
        lines = []
        for point_nm in self._scanPoints:
            line = "%f %f %f\n" % point_nm
            lines.append(line)

        return lines
