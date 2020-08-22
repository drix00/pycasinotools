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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools
import casinotools.fileformat.casino3.transmitted_angles as TransmittedAngles
import casinotools.fileformat.casino3.region_intensity_info as RegionIntensityInfo
import casinotools.fileformat.casino3.trajectory as Trajectory
import casinotools.fileformat.casino3.graph_data as GraphData
import casinotools.fileformat.casino3.energy_matrix as EnergyMatrix
import casinotools.fileformat.casino3.diffused_energy_matrix as DiffusedEnergyMatrix
import casinotools.fileformat.casino3.version as Version
import casinotools.fileformat.casino3.point_spread_function_matrix as PointSpreadFunctionMatrix

# Globals and constants variables.

class ScanPointResults(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file, options):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = b"*SCANPTRUNTIME%"
        if self.find_tag(file, tagID):
            self._version = self.read_int(file)

            self._x = self.read_double(file)
            self._y = self.read_double(file)
            self._z = self.read_double(file)

            self._initialEnergy_keV = self.read_double(file)
            self._rkoMax = self.read_double(file)
            self._rkoMaxW = self.read_double(file)

            self._numberSimulatedTrajectories = self.read_int(file)
            self._beingProcessed = self.read_int(file)

            self._backscatteredCoefficient = self.read_double(file)
            self._backscatteredDetectedCoefficient = self.read_double(file)
            self._secondaryCoefficient = self.read_double(file)
            self._transmittedCoefficient = self.read_double(file)
            self._transmittedDetectedCoefficient = self.read_double(file)
            self._numberBackscatteredElectrons = self.read_int(file)
            self._numberBackscatteredElectronsDetected = self.read_double(file)
            self._numberSecondaryElectrons = self.read_int(file)

            self._transmittedAngles = TransmittedAngles.TransmittedAngles()
            self._transmittedAngles.read(file)

            self._numberResults = self.read_int(file)
            self._regionIntensityInfos = []
            for dummy in range(self._numberResults):
                regionIntensityInfo = RegionIntensityInfo.RegionIntensityInfo()
                regionIntensityInfo.read(file)
                self._regionIntensityInfos.append(regionIntensityInfo)

            self._isDZMax = self.read_bool(file)
            if self._isDZMax:
                self.dzMax = GraphData.GraphData(file)

            self._isDZMaxRetro = self.read_bool(file)
            if self._isDZMaxRetro:
                self.dzMaxRetro = GraphData.GraphData(file)

            self._isDENR = self.read_bool(file)
            if self._isDENR:
                self.DENR = GraphData.GraphData(file)

            self._isDENT = self.read_bool(file)
            if self._isDENT:
                self.DENT = GraphData.GraphData(file)

            self._isDrasRetro = self.read_bool(file)
            if self._isDrasRetro:
                self.DrasRetro = GraphData.GraphData(file)

            self._isDrasRetroEnr = self.read_bool(file)
            if self._isDrasRetroEnr:
                self.DrasRetroEnr = GraphData.GraphData(file)

            self._isDEnergy_Density = self.read_bool(file)
            if self._isDEnergy_Density:
                self.DEnergy_Density_Max_Energy = self.read_double(file)
                self._DEnergy_Density = EnergyMatrix.EnergyMatrix(options, self.getPosition())
                self._DEnergy_Density.read(file)

            self._isDDiffusedEnergy_Density = self.read_bool(file)
            if self._isDDiffusedEnergy_Density:
                self._DDiffusedEnergy_Density = DiffusedEnergyMatrix.DiffusedEnergyMatrix(options, self.getPosition())
                self._DDiffusedEnergy_Density.read(file)

            self._isDbang = self.read_bool(file)
            if self._isDbang:
                self.Dbang = GraphData.GraphData(file)

            self._isDEnBang = self.read_bool(file)
            if self._isDEnBang:
                self.DEnBang = GraphData.GraphData(file)

            if self._version >= Version.SIM_OPTIONS_VERSION_3_3_0_0 and self._version < Version.SIM_OPTIONS_VERSION_3_3_0_4:
                self._isPsf = self.read_bool(file)
                if self._isPsf:
                    self._pointSpreadFunctionMatrix = PointSpreadFunctionMatrix.PointSpreadFunctionMatrix(options, self.getPosition())
                    self._pointSpreadFunctionMatrix.read(file)
                else:
                    self._pointSpreadFunctionMatrix = None
            else:
                self._isPsf = False

            self._numberTrajectories = self.read_int(file)
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
