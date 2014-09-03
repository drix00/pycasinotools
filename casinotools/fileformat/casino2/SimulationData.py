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
import casinotools.fileformat.casino2.SimulationOptions as SimulationOptions
import casinotools.fileformat.casino2.RegionOptions as RegionOptions
import casinotools.fileformat.casino2.TrajectoriesData as TrajectoriesData
import casinotools.fileformat.casino2.SimulationResults as SimulationResults

# Globals and constants variables.
HEADER = b"WinCasino Simulation File"
TAG_VERSION = b"*VERSION%%%%%%%"
TAG_STATUS = b"*STATUS%%%%%%%%"
TAG_SAVE_SETUP = b"*SAVESETUP%%%%%"

from casinotools.fileformat.casino2.Element import \
    LINE_K, LINE_L, LINE_M, GENERATED, EMITTED #@UnusedImport

class SimulationData(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, isSkipReadingData=False):
        self._isSkipReadingData = isSkipReadingData
        self._header = HEADER
        self._version = 2040601
        self._regionOptions = None
        self._simulationOptions = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())
        self._header = self.readStrLength(file, 26)

        logging.debug("File pos: %i", file.tell())
        tagID = TAG_VERSION
        if self.findTag(file, tagID):
            logging.debug("File pos: %i", file.tell())
            self._version = self.readInt(file)

        tagID = TAG_STATUS
        if self.findTag(file, tagID):
            self._status = self.readStrLength(file, 1)

        tagID = TAG_SAVE_SETUP
        if self.findTag(file, tagID):
            self._saveSimulations = self.readInt(file)
            self._saveRegions = self.readInt(file)
            self._saveTrajectories = self.readInt(file)
            self._saveDistributions = self.readInt(file)

        if self._saveSimulations:
            self._readSimulationOptions(file)

        if self._saveRegions:
            self._readRegionOptions(file)

        if self._saveRegions and self._saveTrajectories:
            self._readTrajectories(file)

        if self._saveDistributions:
            self._readSimulationResults(file)

    def _readSimulationOptions(self, file):
        self._simulationOptions = SimulationOptions.SimulationOptions()
        self._simulationOptions.read(file, self._version)

    def _readRegionOptions(self, file):
        if self._simulationOptions.FEmissionRX:
            self._regionOptions = RegionOptions.RegionOptions(self._simulationOptions.NbreCoucheRX)
        else:
            self._regionOptions = RegionOptions.RegionOptions(0)

        self._regionOptions.read(file)

    def _readTrajectories(self, file):
        self._trajectoriesData = TrajectoriesData.TrajectoriesData(self._isSkipReadingData)
        self._trajectoriesData.read(file)

    def _readSimulationResults(self, file):
        self._simulationResults = SimulationResults.SimulationResults(self._isSkipReadingData)
        self._simulationResults.read(file, self._simulationOptions, self._version)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        self.writeStrLength(file, self._header, 26)

        tagID = TAG_VERSION
        self.addTagOld(file, tagID)
        self.writeInt(file, self._version)

        tagID = TAG_STATUS
        self.addTagOld(file, tagID)
        self.writeStrLength(file, self._status, 1)

        tagID = TAG_SAVE_SETUP
        self.addTagOld(file, tagID)
        self.writeInt(file, self._saveSimulations)
        self.writeInt(file, self._saveRegions)
        self.writeInt(file, self._saveTrajectories)
        self.writeInt(file, self._saveDistributions)

        if self._saveSimulations:
            self._writeSimulationOptions(file)

        if self._saveRegions:
            self._writeRegionOptions(file)

        if self._saveRegions and self._saveTrajectories:
            self._writeTrajectories(file)

        if self._saveDistributions:
            self._writeSimulationResults(file)

    def _writeSimulationOptions(self, file):
        self._simulationOptions.write(file)

    def _writeRegionOptions(self, file):
        self._regionOptions.write(file)

    def _writeTrajectories(self, file):
        raise NotImplementedError

    def _writeSimulationResults(self, file):
        raise NotImplementedError

    def getVersion(self):
        return self._version

    def getSimulationOptions(self):
        return self._simulationOptions

    def setSimulationOptions(self, simulationOptions):
        self._simulationOptions = simulationOptions

    def getRegionOptions(self):
        return self._regionOptions

    def setRegionsOptions(self, regionOptions):
        self._regionOptions = regionOptions

    def getSimulationResults(self):
        return self._simulationResults

    def getTrajectoriesData(self):
        return self._trajectoriesData

    def getTotalXrayIntensities(self):
        """
        Returns a :class:`dict` with the intensities (generated and emitted) of
        all the lines and elements in the simulation.
        The dictionary is structured as followed: atomic number, line,
        :const:`EMITTED` or :const:`GENERATED`.
        The lines can either be :const:`LINE_K`, :const:`LINE_L`, :const:`LINE_M`.

        :rtype: class:`dict`
        """
        intensities = {}

        for region in self.getRegionOptions().getRegions():
            for element in region.getElements():
                z = element.getAtomicNumber()
                delta = element.getTotalXrayIntensities()

                intensities.setdefault(z, {})

                for line in delta.keys():
                    if line in intensities[z]:
                        intensities[z][line][GENERATED] += delta[line][GENERATED]
                        intensities[z][line][EMITTED] += delta[line][EMITTED]
                    else:
                        intensities[z].setdefault(line, {})
                        intensities[z][line][GENERATED] = delta[line][GENERATED]
                        intensities[z][line][EMITTED] = delta[line][EMITTED]

        return intensities
