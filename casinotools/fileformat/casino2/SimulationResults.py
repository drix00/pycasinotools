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
import struct
import os

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.ElementIntensity as ElementIntensity
import casinotools.fileformat.casino2.GraphData as GraphData

# Globals and constants variables.

class SimulationResults(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, isSkipReadingData=False):
        self._isSkipReadingData = isSkipReadingData
        self.DENR = None
        self.DZMaxRetro = None

    def read(self, file, options, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = b"*DISTDATA%%%%%%"
        self.findTag(file, tagID)

        self._readBseIntensity(file, options, version)

        tagID = b"*REGULARDIST%%%"
        self.findTag(file, tagID)

        self._readMaximumDepth(file, options, version)

        self._readBackscatteredEnergy(file, options, version)

        self._readBackscatteredEnergyT(file, options, version)

        self._readSurfaceRadiusBse(file, options, version)

        self._readDncr(file, options)

        if version >= 22:
            self._readDepositedEnergy(file, options)

        if version >= 25:
            self._readBackscatteredAngle(file, options, version)

        if version >= 26:
            self._readBseAngleEnergie(file, options, version)

    def _readBseIntensity(self, file, options, version):
        # Intensity distributions
        tagID = b"*INTENSITYDIST%"
        self.findTag(file, tagID)
        self.BE_Intensity_Size = self.readInt(file)
        self.BE_Intensity = self.readDoubleList(file, self.BE_Intensity_Size)
        if version >= 25 and options.UseEnBack:
            self.BE_Intensity_En = self.readDoubleList(file, self.BE_Intensity_Size)
        self.eT = self.readLong(file)
        self._elementIntensityList = []
        for dummy in range(self.eT):
            element = ElementIntensity.ElementIntensity()
            element.read(file)
            self._elementIntensityList.append(element)

    def _readMaximumDepth(self, file, options, version):
        tagID = b"*DZMAX%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDZmax:
            if version >= 2040601:
                flag = self.readInt(file)
                if flag == 1:
                    self.DZMax = GraphData.GraphData(file=file)
                    self.DZMaxRetro = GraphData.GraphData(file=file)
            else:
                numberPoints = self.readLong(file)
                self.NbPointDZMax = numberPoints
                if numberPoints > 0:
                    self.DZMax = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Z Max", "Depth (nm)",
                        "Hits (Normalized)")
                    self.DZMaxRetro = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Z Max", "Depth (nm)",
                        "Hits (Normalized)")
                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        self.DZMax.add(value)

                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        self.DZMaxRetro.add(value)

                else:
                    numberPoints *= -1

    def isBackscatteredMaximumDepthDistribution(self):
        return not self.DZMaxRetro is None

    def getBackscatteredMaximumDepthDistribution(self):
        return self.DZMaxRetro

    def getBackscatteredMaximumDepthRange(self, fractionLimit=0.999):
        range_nm = _computeDepthRange(self.getBackscatteredMaximumDepthDistribution(), fractionLimit)
        return range_nm

    def _readBackscatteredEnergy(self, file, options, version):
        tagID = b"*DENR%%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDenr:
            values = None
            if version >= 2040601:
                flag = self.readInt(file)
                if flag == 1:
                    values = GraphData.GraphData(file=file)
            else:
                numberPoints = self.readLong(file)
                self.NbPointDENR = numberPoints
                if numberPoints > 0:
                    values = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Backscattered Energy", "Energy (KeV)",
                        "Hits (Normalized)")
                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        values.add(value)

                else:
                    numberPoints *= -1
            self.DENR = values

    def isBackscatteredEnergyDistribution(self):
        return not self.DENR is None

    def getBackscatteredEnergyDistribution(self):
        return self.DENR

    def _readBackscatteredEnergyT(self, file, options, version):
        tagID = b"*DENT%%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDent:
            values = None
            if version >= 2040601:
                flag = self.readInt(file)
                if flag == 1:
                    values = GraphData.GraphData(file=file)
            else:
                numberPoints = self.readLong(file)
                self.NbPointDENT = numberPoints
                if numberPoints > 0:
                    values = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Backscattered Energy", "Energy (KeV)",
                        "Hits (Normalized)")
                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        values.add(value)

                else:
                    numberPoints *= -1
            self.DENT = values

    def isTransmittedEnergyDistribution(self):
        return not self.DENT is None

    def getTransmittedEnergyDistribution(self):
        return self.DENT

    def _readSurfaceRadiusBse(self, file, options, version):
        tagID = b"*DRSR%%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDrsr:
            if version >= 2040601:
                flag = self.readInt(file)
                if flag == 1:
                    self.DrasRetro = GraphData.GraphData(file=file)
                    self.DrasRetroEnr = GraphData.GraphData(file=file)
            else:
                numberPoints = self.readLong(file)
                self.NbPointDRSR = numberPoints
                if numberPoints > 0:
                    self.DrasRetro = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Surface Radius of BE", "Radius (nm)",
                        "Hits (Normalized) / nm")
                    self.DrasRetroEnr = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Energy of Surface Radius of BE", "Radius (nm)",
                        "KeV / nm")
                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        self.DrasRetro.add(value)

                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        self.DrasRetroEnr.add(value)

                else:
                    numberPoints *= -1

    def isSurfaceRadiusBseDistribution(self):
        return not self.DrasRetro is None

    def getSurfaceRadiusBseDistribution(self):
        return self.DrasRetro

    def _readDncr(self, file, options):
        tagID = b"*DNCR%%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDncr:
            numberPoints = self.readLong(file)
            if numberPoints > 0:
                values = []
                for dummy in range(numberPoints):
                    value = self.readDouble(file)
                    values.append(value)

            else:
                numberPoints *= -1
            self.NbPointDNCR = numberPoints
            self.DNCR = values

    def _readDepositedEnergy(self, file, options):
        tagID = b"*DEPOS%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDEpos:
            self.NbPointDEpos_X = self.readLong(file)
            self.NbPointDEpos_Y = self.readLong(file)
            self.NbPointDEpos_Z = self.readLong(file)
            self.DEpos_maxE = self.readDouble(file)
            if self.NbPointDEpos_X > 0:
                values = []
                numberPoints = self.NbPointDEpos_X * self.NbPointDEpos_Y * self.NbPointDEpos_Z

                if not self._isSkipReadingData:
                    values = self.readDoubleList(file, numberPoints)
#                    for dummy in range(numberPoints):
#                        value = self.readDouble(file)
#                        values.append(value)
                else:
                    offset = struct.calcsize("d") * numberPoints
                    file.seek(offset, os.SEEK_CUR)

                self.DEpos = values
            else:
                self.NbPointDEpos_X *= -1
                self.NbPointDEpos_Y *= -1
                self.NbPointDEpos_Z *= -1

    def getNumberPointsEnergyAbsorbed(self):
        return self.NbPointDEpos_X * self.NbPointDEpos_Y * self.NbPointDEpos_Z

    def getNumberPointsEnergyAbsorbedX(self):
        return self.NbPointDEpos_X

    def getNumberPointsEnergyAbsorbedY(self):
        return self.NbPointDEpos_Y

    def getNumberPointsEnergyAbsorbedZ(self):
        return self.NbPointDEpos_Z

    def getMaximumEnergyAbsorbed_keV(self):
        return self.DEpos_maxE

    def getEnergyAbsorbed_keV(self):
        return self.DEpos

    def _readBackscatteredAngle(self, file, options, version):
        tagID = b"*DBANG%%%%%%%%%"
        self.findTag(file, tagID)
        if options.FDbang:
            if version >= 2040601:
                flag = self.readInt(file)
                if flag == 1:
                    self.Dbang = GraphData.GraphData(file=file)
                    if options.UseEnBack:
                        flag = self.readInt(file)
                        if flag == 1:
                            self.DEnBang = GraphData.GraphData(file=file)
            else:
                numberPoints = self.readLong(file)
                if numberPoints > 0:
                    self.Dbang = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Backscattered Angle", "Angle (degree)",
                        "Hits (Normalized)")
                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        self.Dbang.add(value)

                    if options.UseEnBack:
                        self.DEnBang = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                            0, 0, "Detected Backscattered Angle", "Angle (degree)",
                            "Hits (Normalized)")
                        for dummy in range(numberPoints):
                            value = self.readDouble(file)
                            self.DEnBang.add(value)

                else:
                    numberPoints *= -1
                self.NbPointDBANG = numberPoints

    def isBackscatteredAngleDistribution(self):
        return not self.Dbang is None

    def getBackscatteredAngleDistribution(self):
        return self.Dbang

    def _readBseAngleEnergie(self, file, options, version):
        tagID = b"*DANGLEENERGY%%"
        self.findTag(file, tagID)
        if options.FDAngleVSEnergie:
            if version >= 2040601:
                flag = self.readInt(file)
                if flag == 1:
                    self.DAngleVSEnergie = GraphData.GraphData(file=file)
                    if options.UseEnBack:
                        flag = self.readInt(file)
                        if flag == 1:
                            self.DEnAngleVSEnergie = GraphData.GraphData(file=file)
            else:
                numberPoints = self.readLong(file)
                if numberPoints > 0:
                    self.DAngleVSEnergie = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                        0, 0, "Backscattered Angle", "Angle (degree)",
                        "Hits (Normalized)")
                    for dummy in range(numberPoints):
                        value = self.readDouble(file)
                        self.DAngleVSEnergie.add(value)

                    if options.UseEnBack:
                        self.DEnAngleVSEnergie = GraphData.GraphData(numberPoints, 0.0, options.RkoMax,
                            0, 0, "Detected Backscattered Angle", "Angle (degree)",
                            "Hits (Normalized)")
                        for dummy in range(numberPoints):
                            value = self.readDouble(file)
                            self.DEnAngleVSEnergie.add(value)

                else:
                    numberPoints *= -1
                self.NbPointDAngleVSEnergie = numberPoints

def _computeDepthRange(distribution, fractionLimit):
    positions = distribution.getPositions()
    values = distribution.getValues()

    total = sum(values)

    partialTotal = 0.0
    for position, value in zip(positions, values):
        partialTotal += value
        fraction = partialTotal / total
        if fraction >= fractionLimit:
            return position

    depth = positions[-1]
    message = "Depth range not found, fraction smaller (%.f) than fraction limit (%.f), return last depth (%.f)" % (fraction, fractionLimit, depth)
    logging.warning(message)
    return depth
