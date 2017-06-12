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
import casinotools.fileformat.casino3.ScanPointResults as ScanPointResults
import casinotools.fileformat.casino3.EnergyMatrix as EnergyMatrix
import casinotools.fileformat.casino3.DiffusedEnergyMatrix as DiffusedEnergyMatrix

# Globals and constants variables.

class SimulationResults(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

    def read(self, file, options):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._numberSimulations = self.readInt(file)

        for dummy in range(self._numberSimulations):
            self._readRuntimeState(file)

            self._readSimulationResults(file, options)

            self._readScanPoints(file, options)

        return None

    def _readRuntimeState(self, file):
        tagID = b"*RUNTIMESTATE%%"
        if self.findTag(file, tagID):
            self._version = self.readInt(file)

            if self._version == 20031202:
                self._readSimulationState(file)

    def _readSimulationState(self, file):
        tagID = b"*SIMSTATE%%%%%%"
        if self.findTag(file, tagID):
            self._initialEnergy_keV = self.readDouble(file)
            self._rkoMax = self.readDouble(file)

    def _readSimulationResults(self, file, options):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_read_simulation_results", file.tell())
        tagID = b"*SIMRESULTS%%%%"
        if self.findTag(file, tagID):
            self._versionSimulationResults = self.readInt(file)

            self._isTotalEnergyDensitySaved = self.readBool(file)
            if self._isTotalEnergyDensitySaved:
                self._DEnergy_Density = EnergyMatrix.EnergyMatrix(options, options._optionsDist.DEpos_Center)
                self._DEnergy_Density.read(file)

            self._isDiffusedTotalEnergyDensitySaved = self.readBool(file)
            if self._isDiffusedTotalEnergyDensitySaved:
                self._DDiffusedEnergy_Density = DiffusedEnergyMatrix.DiffusedEnergyMatrix(options, options._optionsDist.DEpos_Center)
                self._DDiffusedEnergy_Density.read(file)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_read_simulation_results", file.tell())
        tagID = b"*SIMRESULTSEND"
        if not self.findTag(file, tagID):
            raise IOError

    def _readScanPoints(self, file, options):
        self._numberScanPoints = self.readInt(file)

        self._scanPoints = []
        for dummy in range(self._numberScanPoints):
            scanPoint = ScanPointResults.ScanPointResults()
            scanPoint.read(file, options)
            self._scanPoints.append(scanPoint)

    def getScanPointsResults(self):
        return self._scanPoints

    def getScanPointsResultsFromIndex(self, index):
        return self._scanPoints[index]

    def getFirstScanPointResults(self):
        return self.getScanPointsResultsFromIndex(0)

    def getTotalDepositedEnergies_keV(self):
        return self._DEnergy_Density
