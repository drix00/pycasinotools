#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import struct
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.Tags as Tags
import casinotools.fileformat.casino3.SimulationData as SimulationData
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.
SIMULATION_CONFIGURATIONS = "sim"
SIMULATION_RESULTS = "cas"

SAVEFILE_HEADER_MAXCHAR = 1024

V30103040 = 30103040
V30103070 = 30103070
V30104060 = 30104060
V30107002 = 30107002

class SaveContent(object):
    def __init__(self):
        self.sample = False
        self.options = False
        self.scanPointPositions = False
        self.results = False
        self.runtime = False

class File(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, filepath, isModifiable=False):
        self._filepath = filepath
        self._isModifiable = isModifiable

        self._simulationList = []
        self._saveContent = SaveContent()
        self._file = None

        self._version = None
        self.open()

    def _open(self, filepath):
        logging.debug("Filepath to be open in %s: %s", self.__class__.__name__, filepath)
        if self._isModifiable:
            file = open(filepath, 'r+b')
        else:
            file = open(filepath, 'rb')
        return file

    def _openWriting(self, filepath):
        logging.debug("Filepath to be open in %s: %s", self.__class__.__name__, filepath)
        file = open(filepath, 'wb')
        return file

    def getFileType(self):
        type = self._getFileTypeFromFileTag()

        self.reset()

        if type == None:
            type = self._getFileTypeFromExtension()

        return type

    def _getFileTypeFromFileTag(self):
        extension = self._readExtension(self._file)

        if extension.lower() == SIMULATION_CONFIGURATIONS:
            return SIMULATION_CONFIGURATIONS
        elif extension.lower() == SIMULATION_RESULTS:
            return SIMULATION_RESULTS

    def _getFileTypeFromExtension(self):
        extension = os.path.splitext(self._filepath)[-1]

        if extension.lower() == '.' + SIMULATION_CONFIGURATIONS:
            return SIMULATION_CONFIGURATIONS
        elif extension.lower() == '.' + SIMULATION_RESULTS:
            return SIMULATION_RESULTS

    def reset(self):
        self._file.seek(0)

    def getFilepath(self):
        return self._filepath

    def setFilepath(self, filepath):
        self._filepath = filepath

    def open(self):
        self._file = self._open(self._filepath)

        self._type = self.getFileType()

        if self._type == SIMULATION_CONFIGURATIONS:
            self._openSim()
        elif self._type == SIMULATION_RESULTS:
            self._openCas()

    def _openSim(self):
        self._saveContent.sample = True
        self._saveContent.options = True
        self._saveContent.scanPointPositions = True

        self._readCasinoFile(self._file)

    def _openCas(self):
        self._saveContent.sample = True
        self._saveContent.options = True
        self._saveContent.scanPointPositions = True
        self._saveContent.results = True

        self._readCasinoFile(self._file)

    def _readCasinoFile(self, file):
        self._fileVersion = self._extractFileVersion(file)

        self._readWithFileVersion(file, self._fileVersion)

    def _extractFileVersion(self, file):
        if Tags.limitedSearchTag(file, b"V3.1.3.4", SAVEFILE_HEADER_MAXCHAR, Tags.TAG_LENGTH):
            return V30103040
        elif Tags.limitedSearchTag(file, b"V3.1.3.7", SAVEFILE_HEADER_MAXCHAR, Tags.TAG_LENGTH):
            return V30103070
        elif Tags.limitedSearchTag(file, b"%SAVE_HEADER%", SAVEFILE_HEADER_MAXCHAR, Tags.TAG_LENGTH):
            return V30104060

    def _readWithFileVersion(self, file, fileVersion):
        if fileVersion >= V30104060:
            self.reset()
            self._version = self._readVersion(file)

        self._numberSimulations = 1
        if self._version >= 30107002:
            self._numberSimulations = self.readInt(file)

        self._simulationList = []
        for i in range(self._numberSimulations):
            logging.debug("Read simulation %i", i)
            simulation = self._readOneSimulation(file)
            self._simulationList.append(simulation)

    def _readOneSimulation(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_readOneSimulation", file.tell())
        simulationData = SimulationData.SimulationData()

        if self._saveContent.sample:
            simulationData.readSample(file)

        if self._saveContent.options:
            simulationData.readOptions(file)

        if self._saveContent.scanPointPositions:
            simulationData.readScanPointPositions(file)

        if self._saveContent.results:
            simulationData.readResults(file)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_readOneSimulation", file.tell())
        return simulationData

    def openFile(self):
        if self._file.closed:
            self._file = open(self._filePathname, 'rb')

    def closeFile(self):
        if self._file is not None:
            self._file.close()

################################################################################
    def _readExtension(self, file):
        logging.debug("File position: %i", file.tell())
        extension = ""

        tagID = b"ext="
        if Tags.limitedSearchTag(file, tagID, SAVEFILE_HEADER_MAXCHAR, Tags.TAG_LENGTH):
            logging.debug("File position: %i", file.tell())
            format = "3s"
            size = struct.calcsize(format)
            buffer = file.read(size)
            items = struct.unpack_from(format, buffer)
            extension = items[0].decode('ascii')

        return extension

    def _readVersion(self, file):
        version = 0

        tagID = b"%SAVE_HEADER%"
        if Tags.limitedSearchTag(file, tagID, SAVEFILE_HEADER_MAXCHAR, Tags.TAG_LENGTH):
            version = self.readInt(file)

        return version

    def save(self, filepath):
        file = self._openWriting(filepath)
        self.write(file)

    def write(self, file):
        self._writeSim(file)

    def _writeSim(self, file):
        self._saveContent.sample = True
        self._saveContent.options = True
        self._saveContent.scanPointPositions = True

        self._writeCasinoFile(file)

    def _writeCasinoFile(self, file):
        self._writeExtension(file, SIMULATION_CONFIGURATIONS)
        self._writeVersion(file, V30107002)
        self._writeNumberSimulations(file)

        for simulationData in self._simulationList:
            self._writeOneSimulation(file, simulationData)

    def _writeExtension(self, file, extension):
        self.addTag(file, "ext=")
        size = len(extension)
        self.writeStrLength(file, extension, size)

    def _writeVersion(self, file, version):
        self.addTag(file, "%SAVE_HEADER%")
        self.writeInt(file, version)

    def _writeNumberSimulations(self, file):
        assert self._numberSimulations == 1
        assert self._numberSimulations == len(self._simulationList)

        self.writeInt(file, self._numberSimulations)

    def _writeOneSimulation(self, file, simulationData):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_writeOneSimulation", file.tell())

        self.writeInt(file, V30107002)

        if self._saveContent.sample:
            simulationData.writeSample(file)

        if self._saveContent.options:
            simulationData.writeOptions(file)

        if self._saveContent.scanPointPositions:
            simulationData.writeScanPointPositions(file)

        if self._saveContent.results:
            simulationData.writeResults(file)

        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_writeOneSimulation", file.tell())

    def getNumberSimulations(self):
        return self._numberSimulations

    def getSimulations(self):
        return self._simulationList

    def getFirstSimulation(self):
        return self._simulationList[0]

    def getOptions(self):
        return self._simulationList[0].getOptions()

    def getResults(self):
        return self._simulationList[0].getResultList()

    def getScanPointResults(self):
        return self._simulationList[0].getResultList().getScanPointsResults()

    def getFirstSphereShape(self):
        sample = self._simulationList[0].getSample()
        firstSphereShape = sample.getFirstSphereShape()
        return firstSphereShape

    def getAllShapes(self):
        sample = self._simulationList[0].getSample()
        shapes = sample.getShapes()
        return shapes

    def getAllRegions(self):
        sample = self._simulationList[0].getSample()
        regions = sample.getRegions()
        return regions

    def getVersion(self):
        if self._version is None:
            return self._fileVersion
        else:
            return self._version

    def export(self, exportFile):
        self._exportFilename(exportFile)
        self._exportFileType(exportFile)
        self._exportFileVersion(exportFile)

        self._exportHeader(exportFile)
        self._exportNumberSimulations(exportFile)
        self._exportSimulations(exportFile)

    def _exportFilename(self, exportFile):
        filename = os.path.basename(self._filepath)
        line = "Filename: %s" % (filename)
        self.writeLine(exportFile, line)

        line = "Filepath: %s" % (self._filepath)
        self.writeLine(exportFile, line)

    def _exportFileType(self, exportFile):
        line = "File type: %s" % (self._type)
        self.writeLine(exportFile, line)

    def _exportFileVersion(self, exportFile):
        version = self.getVersion()
        versionString = self._extractVersionString(version)
        line = "File version: %s (%i)" % (versionString, version)
        self.writeLine(exportFile, line)

    def _exportHeader(self, exportFile):
        line = "-"*80
        self.writeLine(exportFile, line)

        line = "%s" % ("Simulations")
        self.writeLine(exportFile, line)

        line = "-"*40
        self.writeLine(exportFile, line)

    def _exportNumberSimulations(self, exportFile):
        line = "Number of simulations: %s" % (self._numberSimulations)
        self.writeLine(exportFile, line)

    def _exportSimulations(self, exportFile):
        simulationID = 0
        for simulation in self._simulationList:
            simulationID += 1
            line = "Simulation: %i" % (simulationID)
            self.writeLine(exportFile, line)

            simulation.export(exportFile)

def _run():
    from pkg_resources import resource_filename #@UnresolvedImport
    #filepathCas = Files.getCurrentModulePath(__file__, "../../test_data/casino3.x/WaterAuTop_wSE.cas")
    filepathCas = resource_filename(__file__, "/Volumes/drix01/resultsUdeS/Simulations/Microfluidic/SecondaryElectrons/WaterAuTop_wSE_100e_CS5.cas")
    #filepathCas = Files.getCurrentModulePath(__file__, "/Volumes/drix01/resultsUdeS/Simulations/articles/3dStem/shotNoise/Au_C_thin_1Me.cas")
    #filepathCas = Files.getCurrentModulePath(__file__, "/Volumes/drix01/resultsUdeS/Simulations/articles/3dStem/shotNoise/Au_C_thin_100ke.cas")
    #filepathCas = Files.getCurrentModulePath(__file__, "/Volumes/drix01/resultsUdeS/Simulations/articles/3dStem/shotNoise/Au_C_thin_10ke.cas")
    #filepathCas = Files.getCurrentModulePath(__file__, "/Volumes/drix01/resultsUdeS/Simulations/ResistLines/SiSubstrateThreeLines_PointsEdep.cas")

    file = File(filepathCas)
    print("File name: %s" % (file._file.name))
    print("File descriptor: %i" % (file._file.fileno()))
    print("File type: %s" % (file.getFileType()))
    print("File version: %i" % (file._version))
    print("Number of simualtions: %i" % (file._numberSimulations))
    scanPointResults = file.getResults().getScanPointsResultsFromIndex(0)
    print("Number of saved trajectories: %i" % (scanPointResults.getNumberSavedTrajectories()))
    firstTrajectory = scanPointResults.getSavedTrajectory(0)
    print("Number of collisions in first saved trajectory: %i" % (firstTrajectory.getNumberScatteringEvents()))
    scatteringEvent = firstTrajectory.getScatteringEvent(-1)
    print("Last collision type: %s" % (scatteringEvent.getCollisionType()))
    file.closeFile()

def runProfile():
    import cProfile
    cProfile.run('_run()', 'Casino3.x_File.prof')

def runDebug():
    logging.getLogger().setLevel(logging.DEBUG)
    _run()

if __name__ == '__main__': #pragma: no cover
    runProfile()
