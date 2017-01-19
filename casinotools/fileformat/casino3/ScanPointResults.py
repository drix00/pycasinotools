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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.TransmittedAngles as TransmittedAngles
import casinotools.fileformat.casino3.RegionIntensityInfo as RegionIntensityInfo
import casinotools.fileformat.casino3.Trajectory as Trajectory
import casinotools.fileformat.casino3.GraphData as GraphData
import casinotools.fileformat.casino3.EnergyMatrix as EnergyMatrix
import casinotools.fileformat.casino3.DiffusedEnergyMatrix as DiffusedEnergyMatrix
import casinotools.fileformat.casino3.Version as Version
import casinotools.fileformat.casino3.PointSpreadFunctionMatrix as PointSpreadFunctionMatrix

# Globals and constants variables.

class ScanPointResults(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file, options):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = b"*SCANPTRUNTIME%"
        if self.findTag(file, tagID):
            self._version = self.readInt(file)

            self._x = self.readDouble(file)
            self._y = self.readDouble(file)
            self._z = self.readDouble(file)

            self._initialEnergy_keV = self.readDouble(file)
            self._rkoMax = self.readDouble(file)
            self._rkoMaxW = self.readDouble(file)

            self._numberSimulatedTrajectories = self.readInt(file)
            self._beingProcessed = self.readInt(file)

            self._backscatteredCoefficient = self.readDouble(file)
            self._backscatteredDetectedCoefficient = self.readDouble(file)
            self._secondaryCoefficient = self.readDouble(file)
            self._transmittedCoefficient = self.readDouble(file)
            self._transmittedDetectedCoefficient = self.readDouble(file)
            self._numberBackscatteredElectrons = self.readInt(file)
            self._numberBackscatteredElectronsDetected = self.readDouble(file)
            self._numberSecondaryElectrons = self.readInt(file)

            self._transmittedAngles = TransmittedAngles.TransmittedAngles()
            self._transmittedAngles.read(file)

            self._numberResults = self.readInt(file)
            self._regionIntensityInfos = []
            for dummy in range(self._numberResults):
                regionIntensityInfo = RegionIntensityInfo.RegionIntensityInfo()
                regionIntensityInfo.read(file)
                self._regionIntensityInfos.append(regionIntensityInfo)

            self._isDZMax = self.readBool(file)
            if self._isDZMax:
                self.dzMax = GraphData.GraphData(file)

            self._isDZMaxRetro = self.readBool(file)
            if self._isDZMaxRetro:
                self.dzMaxRetro = GraphData.GraphData(file)

            self._isDENR = self.readBool(file)
            if self._isDENR:
                self.DENR = GraphData.GraphData(file)

            self._isDENT = self.readBool(file)
            if self._isDENT:
                self.DENT = GraphData.GraphData(file)

            self._isDrasRetro = self.readBool(file)
            if self._isDrasRetro:
                self.DrasRetro = GraphData.GraphData(file)

            self._isDrasRetroEnr = self.readBool(file)
            if self._isDrasRetroEnr:
                self.DrasRetroEnr = GraphData.GraphData(file)

            self._isDEnergy_Density = self.readBool(file)
            if self._isDEnergy_Density:
                self.DEnergy_Density_Max_Energy = self.readDouble(file)
                self._DEnergy_Density = EnergyMatrix.EnergyMatrix(options, self.getPosition())
                self._DEnergy_Density.read(file)

            self._isDDiffusedEnergy_Density = self.readBool(file)
            if self._isDDiffusedEnergy_Density:
                self._DDiffusedEnergy_Density = DiffusedEnergyMatrix.DiffusedEnergyMatrix(options, self.getPosition())
                self._DDiffusedEnergy_Density.read(file)

            self._isDbang = self.readBool(file)
            if self._isDbang:
                self.Dbang = GraphData.GraphData(file)

            self._isDEnBang = self.readBool(file)
            if self._isDEnBang:
                self.DEnBang = GraphData.GraphData(file)

            if self._version >= Version.SIM_OPTIONS_VERSION_3_3_0_0 and self._version < Version.SIM_OPTIONS_VERSION_3_3_0_4:
                self._isPsf = self.readBool(file)
                if self._isPsf:
                    self._pointSpreadFunctionMatrix = PointSpreadFunctionMatrix.PointSpreadFunctionMatrix(options, self.getPosition())
                    self._pointSpreadFunctionMatrix.read(file)
                else:
                    self._pointSpreadFunctionMatrix = None
            else:
                self._isPsf = False

            self._numberTrajectories = self.readInt(file)
            self._trajectories = []
            for dummy in range(self._numberTrajectories):
                trajectory = Trajectory.Trajectory()
                trajectory.read(file)
                self._trajectories.append(trajectory)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", file.tell())

    def getPosition(self):
        return (self._x, self._y, self._z)

    def getTransmittedCoefficient(self):
        return self._transmittedCoefficient

    def getTransmittedDetectedCoefficient(self):
        return self._transmittedDetectedCoefficient

    def getTransmittedDetectedElectrons(self, betaMin=None, betaMax=None):
        if betaMin == None and betaMax == None:
            return self._transmittedDetectedCoefficient * self._numberSimulatedTrajectories
        else:
            return self._transmittedAngles.getTransmittedDetectedElectrons(betaMin, betaMax)

    def getTransmittedAngles(self):
        return self._transmittedAngles.getAngles()

    def getTransmittedBinnedAngles(self):
        return self._transmittedAngles.getBinnedAngles()

    def getNumberSimulatedTrajectories(self):
        return self._numberSimulatedTrajectories

    def getInitialEnergy_keV(self):
        return self._initialEnergy_keV

    def getBackscatteredCoefficient(self):
        return self._backscatteredCoefficient

    def getBackscatteredDetectedCoefficient(self):
        return self._backscatteredDetectedCoefficient

    def getNumberBackscatteredDetectedElectrons(self):
        return self._numberBackscatteredElectronsDetected

    def getNumberBackscatteredElectrons(self):
        return self._numberBackscatteredElectrons

    def getSecondaryElectronCoefficient(self):
        return self._secondaryCoefficient

    def getDepositedEnergies_keV(self, regionInfoIndex):
        try:
            regionIntensityInfo = self._regionIntensityInfos[regionInfoIndex]
            return regionIntensityInfo.getEnergyIntensity()
        except IndexError as message:
            logging.debug(message)
            return 0.0

    def getNumberSavedTrajectories(self):
        return self._numberTrajectories

    def getSavedTrajectory(self, index):
        return self._trajectories[index]

    def getSavedTrajectories(self):
        return self._trajectories

    def getMaximumEnergyAbsorbed_keV(self):
        return self.DEnergy_Density_Max_Energy

    def getEnergyAbsorbed_keV(self):
        return self._DEnergy_Density

    def isPsfs(self):
        return self._isPsf

    def getPointSpreadFunctionMatrix(self):
        return self._pointSpreadFunctionMatrix
