#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import os.path
import logging
import csv
import stat
import shutil
import math

# Third party modules.
from scipy.constants import elementary_charge
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import scipy.io as sio

# Local modules.
import pyHendrixDemersTools.Files as Files
import pyHendrixDemersTools.serialization.SerializationPickle as SerializationPickle
import casinotools.scripting.casino3.CasinoSimulationExperimentSet as CasinoSimulationExperimentSet
import casinotools.scripting.casino3.ScriptFile as ScriptFile
import casinotools.scripting.casino3.BatchFile as BatchFile
from  casinotools.analysis.casino3 import export_simulation_parameters
import casinotools.fileformat.casino3.File as CasinoFile
from casinotools.analysis.casino3.transmitted_electrons import Result

# Globals and constants variables.

class AnalyzeCasinoSimulation(object):
    INPUTS_FOLDER = "inputs"
    SCRIPTS_FOLDER = "scripts"
    RESULTS_FOLDER = "results"

    PARAMETERS_NAME = {0: "name", 1: "sample", 2: "beamDistribution",
                       3: "thickness (nm)", 4: "focalPositionZ (nm)",
                       5: "energy (keV)", 6: "beamRadius (nm)",
                       7: "semiAngle (mrad)", 8: "numberElectrons"}

    def __init__(self, overwrite=True, basepath=None, relativePath=None, simulationPath=None, configurationFilepath=None):
        if configurationFilepath == None:
            self._configurationFilepath = Files.getCurrentModulePath(__file__, "pyUdeS.cfg")
        else:
            self._configurationFilepath = configurationFilepath

        self._output = None
        self._overwrite = overwrite
        self.resetCache = True
        self._useSerialization = True

        if simulationPath is not None:
            self._simulationPath = os.path.normpath(simulationPath)
        else:
            self._simulationPath = None

        if basepath is not None:
            self._basepath = os.path.normpath(basepath)
        else:
            self._basepath = None

        if relativePath is not None:
            self._relativePath = os.path.normpath(relativePath)
        else:
            self._relativePath = None

        self._createAllFolders(self.getSimulationPath())

        self._resultFilepaths = []
        self._simulationResultsList = []
        self._serializationExtension = '.ser'

        self._isCreatingBackup = True

        self._initData()

    def getAnalysisName(self):
        raise NotImplementedError

    def getProgramPath(self):
        return Files.getBinPath(self._configurationFilepath, "casino3/latest")

    def getSimulationPath(self):
        try:
            if self._simulationPath is not None:
                return self._simulationPath
            elif self._relativePath is not None:
                path = Files.getResultsSherbrookePath(self._configurationFilepath)
                path = os.path.join(path, "Simulations", self._relativePath)
            elif self._basepath is not None:
                name = self.getAnalysisName()
                path = Files.getResultsSherbrookePath(self._configurationFilepath)
                path = os.path.join(path, "Simulations", self._basepath, "%s" % (name))
            else:
                name = self.getAnalysisName()
                path = Files.getResultsSherbrookePath(self._configurationFilepath, "Simulations/%s" % (name))

            if not os.path.isdir(path):
                os.makedirs(path)
            return path
        except NotImplementedError:
            return None

    def getInputPath(self):
        path = os.path.join(self.getSimulationPath(), self.INPUTS_FOLDER)
        return path

    def getScriptsPath(self):
        path = os.path.join(self.getSimulationPath(), self.SCRIPTS_FOLDER)
        return path

    def _createAllFolders(self, basePath):
        if basePath is not None:
            if not os.path.isdir(basePath):
                os.makedirs(basePath)

            newPaths = [self.INPUTS_FOLDER, self.SCRIPTS_FOLDER, self.RESULTS_FOLDER]
            for newPath in newPaths:
                path = os.path.join(basePath, newPath)
                if not os.path.isdir(path):
                    os.makedirs(path)

    def _initData(self):
        pass

    def generateScripts(self):
        self._processScriptsFolder()

        self.createScanPointsFiles()

        self.createScripts()

    def createScanPointsFiles(self):
        logging.warning("createScanPointsFiles not implemented in derived class.")

    def checkInputFilesCorrectness(self):
        path = self.getInputPath()
        simulationFilenames = self.getAllSimulationFilenames()

        for simulationFilename in simulationFilenames:
            print "Simulation filename: %s" % (simulationFilename)

            filepath = os.path.join(path, simulationFilename)
            exportSimulationParameters = export_simulation_parameters.ExportSimulationParameters()
            data = exportSimulationParameters.getRegionCompositionData(filepath)

            for regionName, composition in data:
                print "%-20s: %s" % (regionName, composition)

            data = exportSimulationParameters.getShapePositionDimensionData(filepath)
            for name, shapeType, position_nm, dimension_nm in data:
                print "%-20s (%s): %s %s" % (name, shapeType, position_nm, dimension_nm)

    def _processScriptsFolder(self):
        if self._overwrite:
            path = os.path.join(self.getSimulationPath(), self.SCRIPTS_FOLDER)
            for filepath in Files.findAllFiles(path, '*.txt'):
                if os.path.isfile(filepath):
                    logging.debug("Remove script file: %s", filepath)
                    os.remove(filepath)

    def createScripts(self):
        raise NotImplementedError

    def getAllSimulationFilenames(self):
        path = os.path.join(self.getSimulationPath(), self.INPUTS_FOLDER)

        filenames = []
        for filename in os.listdir(path):
            if filename.endswith('.sim'):
                filenames.append(filename)

        return filenames

    def getSimulationFilenamesPattern(self, pattern):
        path = os.path.join(self.getSimulationPath(), self.INPUTS_FOLDER)

        filenames = []
        for filename in os.listdir(path):
            if filename.endswith('.sim') and pattern in filename:
                filenames.append(filename)

        return filenames

    def getScanPointFilenamesPattern(self, pattern, folder="inputs"):
        path = os.path.join(self.getSimulationPath(), folder)

        filenames = []
        for filename in os.listdir(path):
            if filename.endswith('.txt') and pattern in filename:
                filenames.append(filename)

        return filenames

    def getAllSimulationResultsFilepaths(self):
        path = os.path.join(self.getSimulationPath(), self.RESULTS_FOLDER)

        filepaths = []
        for filename in os.listdir(path):
            if filename.endswith('.cas') or filename.endswith(self._serializationExtension):
                if filename.endswith(self._serializationExtension):
                    filename = filename.replace(self._serializationExtension, '.cas')
                filepath = os.path.join(path, filename)
                filepaths.append(filepath)

        return filepaths

    def getSimulationResultsFilepathsPattern(self, pattern):
        path = os.path.join(self.getSimulationPath(), self.RESULTS_FOLDER)

        filepaths = []
        for filename in os.listdir(path):
            if filename.endswith('.cas') or filename.endswith(self._serializationExtension):
                if filename.endswith(self._serializationExtension):
                    filename = filename.replace(self._serializationExtension, '.cas')

                if pattern in filename:
                    filepath = os.path.join(path, filename)
                    filepaths.append(filepath)

        filepaths = sorted(set(filepaths))

        return filepaths

    def _createScripts(self, basename, simulationParameters, optionsPathDefaultFilepath=None, batchBasename=None, batchFile=None):
        logging.debug("_createScripts")

        totalNumberSimulations = 0
        doneNumberSimulations = 0
        todoNumberSimulations = 0

        experimentSet = CasinoSimulationExperimentSet.CasinoSimulationExperimentSet(simulationParameters)
        experimentSet.createAllExperiments()

        scriptFilenames = []
        for experiment in experimentSet.nextExperiment():
            simulationFilename = experiment.getFilename()
            simulationFilepath = os.path.join(self.getSimulationPath(), self.INPUTS_FOLDER, simulationFilename)
            if not self._isFileExist(simulationFilepath):
                logging.warning("Simulation file does not exist: %s", simulationFilepath)
            else:
                totalNumberSimulations += 1
                scriptFilename, resultFilepath = self._createScriptFile(basename, experiment)
                if not self._isAllResultFileExist(resultFilepath, simulationFilepath):
                    scriptFilenames.append(scriptFilename)
                    todoNumberSimulations += 1
                else:
                    doneNumberSimulations += 1
                    self._resultFilepaths.append(resultFilepath)
                    self._removeDoneScriptFiles(scriptFilename)

        scriptFilenames = sorted(scriptFilenames)

        if batchBasename is None:
                batchBasename = basename
        batchBasename = "Batch_%s" % (batchBasename)
        if batchFile == None:
            self._createBatchFile(scriptFilenames, batchBasename, optionsPathDefaultFilepath, todoNumberSimulations, doneNumberSimulations)
        else:
            self._addToBatchFile(scriptFilenames, batchFile, optionsPathDefaultFilepath, todoNumberSimulations, doneNumberSimulations)

        assert (doneNumberSimulations+todoNumberSimulations) == totalNumberSimulations
        logging.debug("%s", basename)
        if totalNumberSimulations > 0:
            percentage = 100.0*doneNumberSimulations/float(totalNumberSimulations)
        else:
            percentage = 0.0
        logging.debug("Simulation done: %i/%i (%.1f%%)", doneNumberSimulations, totalNumberSimulations, percentage)

        if totalNumberSimulations > 0:
            percentage = 100.0*todoNumberSimulations/float(totalNumberSimulations)
        else:
            percentage = 0.0
        logging.debug("Simulation todo: %i/%i (%.1f%%)", todoNumberSimulations, totalNumberSimulations, percentage)

    def _removeDoneScriptFiles(self, scriptFilename):
        scriptFilepath = os.path.join(self.getScriptsPath(), scriptFilename)
        if os.path.isfile(scriptFilepath):
            logging.debug("Remove script file: %s", scriptFilepath)
            os.remove(scriptFilepath)

    def _isFileExist(self, filename):
        # todo: Check if this method is correct?
        filepath = os.path.join(self.getProgramPath(), self.RESULTS_FOLDER, filename)
        return os.path.isfile(filepath)

    def _createScriptFile(self, basename, experiment):
        scriptFile = ScriptFile.ScriptFile(basename, self._overwrite)
        scriptFile.setExperiment(experiment)

        scriptFile.setPath(os.path.join(self.getSimulationPath(), self.SCRIPTS_FOLDER))

        simulationsPath = os.path.join(self.getSimulationPath(), self.INPUTS_FOLDER)
        scriptFile.setSimulationPath(simulationsPath)

        resultsPath = os.path.join(self.getSimulationPath(), self.RESULTS_FOLDER)
        scriptFile.setResultsPath(resultsPath)

        scriptFile.createFile()

        scriptFilename = scriptFile.getScriptFilename()
        resultFilepath = scriptFile.getResultsFilepath()

        return scriptFilename, resultFilepath

    def _isAllResultFileExist(self, resultFilepath, simulationFilepath):
        resultSerializedFilepath = resultFilepath.replace('.cas', '_numpy.npz')

        if os.path.isfile(resultFilepath) and not self.isOlderThan(resultFilepath, simulationFilepath):
            logging.debug("Done: %s", resultFilepath)
            return True
        else:
            logging.debug("missing: %s", resultFilepath)

        if os.path.isfile(resultSerializedFilepath) and not self.isOlderThan(resultSerializedFilepath, simulationFilepath):
            logging.debug("Done: %s", resultSerializedFilepath)
            return True
        else:
            logging.debug("missing: %s", resultSerializedFilepath)

        return False

    def isOlderThan(self, resultFilepath, simulationFilepath):
        if not os.path.isfile(resultFilepath):
            return True

        statMainFile = os.stat(resultFilepath)
        statOtherFile = os.stat(simulationFilepath)

        if statOtherFile[stat.ST_MTIME] > statMainFile[stat.ST_MTIME]:
            return True
        elif statOtherFile[stat.ST_CTIME] > statMainFile[stat.ST_MTIME] and statOtherFile[stat.ST_CTIME] > statMainFile[stat.ST_CTIME]:
            return True
        else:
            return False

    def _createBatchFile(self, scriptFilenames, batchBasename, optionsPathDefaultFilepath=None, todoNumberSimulations=0, doneNumberSimulations=0):
        batchFile = BatchFile.BatchFile(self._overwrite)
        batchFile.setPath(self.getProgramPath())
        batchFile.setBasename(batchBasename)
        batchFile.setScriptPath(os.path.join(self.getSimulationPath(), self.SCRIPTS_FOLDER))
        batchFile.setScriptFilenames(scriptFilenames, todoNumberSimulations, doneNumberSimulations)
        batchFile.setOptionsPathDefaultFilepath(optionsPathDefaultFilepath)

        self._batchFilepath = batchFile.createFile()

    def _addToBatchFile(self, scriptFilenames, batchFile, optionsPathDefaultFilepath=None, todoNumberSimulations=0, doneNumberSimulations=0):
        batchFile.setPath(self.getProgramPath())
        batchFile.setScriptPath(os.path.join(self.getSimulationPath(), self.SCRIPTS_FOLDER))
        batchFile.addScriptFilenames(scriptFilenames, todoNumberSimulations, doneNumberSimulations)
        batchFile.setOptionsPathDefaultFilepath(optionsPathDefaultFilepath)

        self._batchFilepath = batchFile.createFile(isWarning=False)

    def computeNumberElectrons(self, current_nA, pixelDwellTime_us):
        current_A = current_nA*1.0e-9
        pixelDwellTime_s = pixelDwellTime_us*1.0e-6
        numberElectrons = int(current_A*pixelDwellTime_s/elementary_charge)

        return numberElectrons

    def getResultFilepaths(self):
        if self._resultFilepaths == []:
            self._resultFilepaths = self.getAllSimulationResultsFilepaths()
        return self._resultFilepaths

    def getResultsPath(self):
        resultsPath = os.path.join(self.getSimulationPath(), self.RESULTS_FOLDER)
        return    resultsPath

    def readResults(self, resultFilepaths=None, serializationFilename="", isResultsKeep=True):
        logging.info("readResults")

        if resultFilepaths is None:
            self._resultFilepaths = []
        else:
            self._resultFilepaths = resultFilepaths

        self._readAllResults(serializationFilename, isResultsKeep)

    def _readAllResults(self, serializationFilename="", isResultsKeep=True):
        if self._useSerialization:
            if serializationFilename == "":
                serializationFilename = self.getAnalysisName() + ".ser"
            self._readAllResultsSerialization(serializationFilename, isResultsKeep)
        else:
            self._readAllResultsNoSerialization(isResultsKeep)

    def _readResultsSerialization(self, serializationFilename):
        logging.info("_readAllResultsSerialization")

        simulationsResults = SerializationPickle.SerializationPickle()
        simulationsResults.setPathname(self.getResultsPath())
        simulationsResults.setFilename(serializationFilename)

        if self.resetCache:
            simulationsResults.deleteFile()

        simulationResultsList = {}
        if simulationsResults.isFile():
            simulationResultsList = simulationsResults.load()

        self._simulationResultsList = simulationResultsList
        logging.info("Number of simulation results: %i", len(self._simulationResultsList))

    def _readAllResultsSerialization(self, serializationFilename, isResultsKeep):
        logging.info("_readAllResultsSerialization")

        simulationsResults = SerializationPickle.SerializationPickle()
        simulationsResults.setPathname(self.getResultsPath())
        simulationsResults.setFilename(serializationFilename)

        if self._isCreatingBackup:
            simulationsResults.backupFile()

        newResults = False
        if self.resetCache:
            simulationsResults.deleteFile()

        simulationResultsList = {}
        if simulationsResults.isFile():
            simulationResultsList = simulationsResults.load()

        filepaths = self.getResultFilepaths()
        total = len(filepaths)
        for index, filepath in enumerate(filepaths):
            try:
                parameters = self._extractParametersFromFilepath(filepath)
                if simulationsResults.isOlderThan(filepath) or parameters not in simulationResultsList:
                    logging.info("Processing file %i/%i", (index+1), total)
                    if os.path.isfile(filepath):
                        logging.info(filepath)
                        simulationResultsList[parameters] = self._readResults(filepath)
                        newResults = True
                        simulationsResults.save(simulationResultsList)
                    else:
                        logging.warning("File not found: %s", filepath)
            except UnboundLocalError, message:
                logging.error("UnboundLocalError in %s for %s", "_readAllResultsSerialization", filepath)
                logging.error(message)
            except ValueError, message:
                logging.error("ValueError in %s for %s", "_readAllResultsSerialization", filepath)
                logging.error(message)
            except AssertionError, message:
                logging.error("AssertionError in %s for %s", "_readAllResultsSerialization", filepath)
                logging.error(message)


        if newResults:
            simulationsResults.save(simulationResultsList)

        if isResultsKeep:
            self._simulationResultsList = simulationResultsList
            logging.info("Number of simulation results: %i", len(self._simulationResultsList))
        else:
            del simulationResultsList

    def _readAllResultsNoSerialization(self, isResultsKeep):
        logging.info("_readAllResultsNoSerialization")

        simulationResultsList = {}

        filepaths = self.getResultFilepaths()
        total = len(filepaths)
        for index, filepath in enumerate(filepaths):
            try:
                logging.info("Processing file %i/%i", (index+1), total)
                logging.info(filepath)
                parameters = self._extractParametersFromFilepath(filepath)
                simulationResults = self._readResults(filepath)
                if isResultsKeep:
                    simulationResultsList[parameters] = simulationResults

                del simulationResults

            except ValueError, message:
                logging.error("ValueError in %s for %s", "_readAllResultsNoSerialization", filepath)
                logging.error(message)
            except UnboundLocalError, message:
                logging.error("UnboundLocalError in %s for %s", "_readAllResultsNoSerialization", filepath)
                logging.error(message)

        if isResultsKeep:
            self._simulationResultsList = simulationResultsList
            logging.info("Number of simulation results: %i", len(self._simulationResultsList))
        else:
            del simulationResultsList

    def _extractParametersFromFilepath(self, filepath):
        raise NotImplementedError

    def _readResults(self, filepath):
        raise NotImplementedError

    def _readTransmittedElectronsLinescanXResults(self, filepath):
        if os.path.isfile(filepath):
            logging.info(filepath)

            casinoFile = CasinoFile.File(filepath)
            casinoFile.openFile()
            result = Result()
            result.setSimulations(casinoFile.getSimulations())

            x = result.getXList()
            betaMin_mrad = self._betaMin_mrad
            betaMax_mrad = self._betaMax_mrad
            y = result.getDetectedTransmittedElectrons(betaMin_mrad, betaMax_mrad)

            data = (x, y)
            casinoFile.closeFile()
            del casinoFile

        else:
            logging.warning("File not found: %s", filepath)

        return data

    def _generateFilenameScanRange(self, basename, scanRanges, rangeLabel=''):
        filenames = []
        for scanRange in scanRanges:
            filename = "%s_%s%ipts.sim" % (basename, rangeLabel, scanRange)
            filenames.append(filename)

        return filenames

    def _extractBeamDistribution(self, text):
        """
        bG
        """

        if text.startswith('b') and (text.endswith('G') or text.endswith('U')):
            value = text[1:]
            return value
        else:
            raise ValueError

    def _extractNumberPoints(self, text):
        """
        201pts
        """

        if text.endswith('pts'):
            value = text[:-3]
            return value
        else:
            raise ValueError

    def _extractEnergy(self, text):
        """
        E200.0keV
        """

        if text.startswith('E') and text.endswith('keV'):
            value = text[1:-3]
            return value
        else:
            raise ValueError

    def _extractBeamDiameter(self, text):
        """
        db0.1nm
        """

        if text.startswith('db') and text.endswith('nm'):
            value = text[2:-2]
            return value
        else:
            raise ValueError

    def _extractBeamRadius(self, text):
        """
        br0.1nm
        """

        if text.startswith('br') and text.endswith('nm'):
            value = text[2:-2]
            return value
        else:
            raise ValueError

    def _extractSemiAngle(self, text):
        """
        a0.0mrad
        """

        if text.startswith('a') and text.endswith('mrad'):
            value = text[1:-4]
            return value
        else:
            raise ValueError

    def _extractSphereRadius(self, text):
        """
        sr0.5nm
        """

        if text.startswith('sr') and text.endswith('nm'):
            value = text[2:-2]
            return value
        else:
            raise ValueError

    def _extractSpherePositionZ(self, text):
        """
        pz652nm
        """

        if text.startswith('pz') and text.endswith('nm'):
            value = text[2:-2]
            return value
        else:
            raise ValueError

    def _extractPlaneThickness(self, text):
        """
        pz1000nm
        """

        if text.startswith('pz') and text.endswith('nm'):
            value = text[2:-2]
            return value
        else:
            raise ValueError

    def _extractFocalPositionZ(self, text):
        """
        fz-1000.0nm
        """

        if text.startswith('fz') and text.endswith('nm'):
            value = text[2:-2]
            return value
        else:
            raise ValueError

    def _extractNumberElectrons(self, text):
        """
        N1ke
        """

        if text.startswith('N') and text.endswith('e'):
            value = text[1:-1]
            return value
        else:
            raise ValueError

    def _extractThickness_nm(self, text):
        """
        T1000nm
        """

        if text.startswith('T') and text.endswith('nm'):
            value = text[1:-2]
            return value
        else:
            raise ValueError

    def _generateBeamDistribution(self, value):
        """
        bG
        """
        text = "b%s" % (value)
        return text

    def _generateNumberPoints(self, value):
        """
        201pts
        """

        text = "%spts" % (value)
        return text

    def _generateRange(self, value):
        """
        r2000nm
        """

        text = "r%snm" % (value)
        return text

    def _generateEnergy(self, value):
        """
        E200.0keV
        """

        text = "E%skeV" % (value)
        return text

    def _generateBeamDiameter(self, value):
        """
        db0.1nm
        """
        text = "db%snm" % (value)
        return text

    def _generateSemiAngle(self, value):
        """
        a0.0mrad
        """

        text = "a%smrad" % (value)
        return text

    def _generateSphereRadius(self, value):
        """
        sr0.5nm
        """
        text = "sr%snm" % (value)
        return text

    def _generateSpherePositionZLabel(self, value):
        """
        pz652nm
        """
        text = "pz%snm" % (value)
        return text

    def _generatePlaneThickness(self, value):
        """
        pz1000nm
        """
        text = "pz%snm" % (value)
        return text

    def _generateFocalPositionZ(self, value):
        """
        fz-1000.0nm
        """
        text = "fz%snm" % (value)
        return text

    def _generateNumberElectrons(self, value):
        """
        N1ke
        """
        text = "N%se" % (value)
        return text

    def _extractSampleRotation(self, text):
        """
        t-45deg
        """

        if text.startswith('t') and text.endswith('deg'):
            value = text[1:-3]
            return value
        else:
            raise ValueError

    def _extractDistance(self, text):
        """
        d800nm
        """

        if text.startswith('d') and text.endswith('nm'):
            value = text[1:-2]
            return value
        else:
            raise ValueError

    def getParametersList(self):
        return self._simulationResultsList.keys()

    def getResults(self, parameters):
        return self._simulationResultsList[parameters]

    def _saveFigure(self, graphicFilepath):
        for extension in ['.png', '.pdf']:
            plt.savefig(graphicFilepath+extension)

    def _exportFigureData(self, graphicFilepath, x ,y, rowHeader=["X (nm)", "Number detected electrons"]):
        csvFilepath, dummyExtension = os.path.splitext(graphicFilepath)
        csvFilepath += ".csv"

        writer = csv.writer(open(csvFilepath, 'wb'))

        writer.writerow(rowHeader)

        for row in zip(x, y):
            writer.writerow(row)

    def _logParameters(self):
        parametersSet = {}
        parametersList = self._simulationResultsList.keys()

        listType = None
        for parameters in parametersList:
            if isinstance(parameters, list):
                listType = 'list'
                for index, parameter in enumerate(parameters):
                    parametersSet.setdefault(index, set())
                    parametersSet[index].add(parameter)
            elif isinstance(parameters, dict):
                listType = 'dict'
                for key in parameters:
                    parametersSet.setdefault(key, set())
                    parametersSet[key].add(parameters[key])

        if listType == 'list':
            logging.info("Number of parameters: %i", len(parametersSet))
            for parameterIndex in sorted(parametersSet):
                parameterList = ", ".join(sorted(parametersSet[parameterIndex]))
                print "%s : %s" % (self.PARAMETERS_NAME[parameterIndex], parameterList)
        elif listType == 'dict':
            logging.info("Number of parameters: %i", len(parametersSet))
            for key in sorted(parametersSet):
                parameterList = ", ".join(sorted(parametersSet[key]))
                print "%s : %s" % (key, parameterList)

    def _computeHistogramList(self, verticalPositions_nm, positions_nm, normalizationFactor=None):
        histogramList = []
        for verticalPosition_nm in verticalPositions_nm:
            xArray, yArray = self._extractPositionsArrays_nm(positions_nm, verticalPosition_nm)
            histogram, xedges, yedges = np.histogram2d(xArray, yArray, bins=self._bins, range=self._range)

            if normalizationFactor is not None:
                histogram = histogram/float(normalizationFactor)

            histogramList.append(histogram)

            if False:
                self._createDebugHistogramImage(histogram, xedges, yedges)

        return histogramList

    def _extractPositionsArrays_nm(self, positions_nm, verticalPosition_nm):
        condition = positions_nm[:,2] == verticalPosition_nm
        condition = np.reshape(np.repeat(condition, 3), (-1, 3))
        tempPositions_nm = np.reshape(np.extract(condition, positions_nm), (-1, 3))

        xArray = tempPositions_nm[:,0]
        yArray = tempPositions_nm[:,1]

        return xArray, yArray

    def _extractScanPointsInformationFromScanPointsFile(self, filename, demiRange=True):
        filepath = os.path.join(self.getInputPath(), filename)
        logging.info("Nominal input filepath: %s", filepath)

        lines = open(filepath, 'rb').readlines()

        logging.info("Number of lines: %i", len(lines))

        maxX = 0.0
        minX = 1.0e20
        maxY = 0.0
        minY = 1.0e20

        setX = set()
        setY = set()
        xArray = []
        yArray = []

        for line in lines:
            x, y, _z = line.split()

            x = float(x)
            y = float(y)

            setX.add(x)
            setY.add(y)

            xArray.append(x)
            yArray.append(y)

            maxX = max(maxX, x)
            minX = min(minX, x)

            maxY = max(maxY, y)
            minY = min(minY, y)

        rangeX = (maxX - minX)/2.0
        rangeY = (maxY - minY)/2.0

        numberBinsX = len(setX)
        numberBinsY = len(setY)

        if demiRange:
            # Range have to be 1/2 of the images.
            rangeX /= 2.0
            rangeY /= 2.0

            numberBinsX = int(numberBinsX/2)
            numberBinsY = int(numberBinsY/2)

        self._range = [[-rangeX, rangeX], [-rangeY, rangeY]]

        self._setX = np.linspace(-rangeX, rangeX, numberBinsX)
        self._setY = np.linspace(-rangeX, rangeX, numberBinsY)

        self._bins = [numberBinsX, numberBinsY]
        histogram, xedges, yedges = np.histogram2d(xArray, yArray, bins=self._bins, range=self._range)

        print histogram.shape, xedges.shape, yedges.shape
        print histogram[0][0]
        print histogram[-1][-1]
        print xedges[0]
        print xedges[-1]
        print yedges[0]
        print yedges[-1]

        if False:
            extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
            plt.imshow(histogram, extent=extent, interpolation='nearest')
            plt.colorbar()
            plt.show()

    def _writeFocalDataSetDataFile(self, verticalPositions_nm, histogramList, filepath):
        logging.info("Create file: %s", filepath)
        writer = csv.writer(open(filepath, 'wb'))

        row = ["x (nm)", "y (nm)", "z (nm)", "Intensity"]
        writer.writerow(row)

        for indexZ, dummy_verticalPosition_nm in enumerate(verticalPositions_nm):
            for indexX in xrange(self._bins[0]):
                for indexY in xrange(self._bins[1]):
                    row = [indexX, indexY, indexZ, histogramList[indexZ][indexX, indexY]]
                    writer.writerow(row)

    def _writeFocalDataSetDataFileMatlab(self, verticalPositions_nm, histogramList, filepath):
        filepath, dummyExtension = os.path.splitext(filepath)
        filepath += '.mlab'
        logging.info("Create file: %s", filepath)

        matrix3D = np.zeros((self._bins[0], self._bins[1], len(verticalPositions_nm)))
        for indexZ, dummy_verticalPosition_nm in enumerate(verticalPositions_nm):
            for indexX in xrange(self._bins[0]):
                for indexY in xrange(self._bins[1]):
                    matrix3D[indexX, indexY, indexZ] = histogramList[indexZ][indexX, indexY]

        sio.savemat(filepath, {'matrix3D':matrix3D}, oned_as='column')

    def _createFocalDataSetImageFile(self, verticalPositions_nm, histogramList, filepath, keepAll=True):
        masterImageFilepath, dummyExtension = os.path.splitext(filepath)
        masterImageFilepath += '.tiff'

        path, filename = os.path.split(filepath)
        filename, dummyExtension = os.path.splitext(filename)
        imagePath = os.path.join(path, filename)
        imagePath = Files.createPath(imagePath)

        for index, verticalPosition_nm in enumerate(verticalPositions_nm):
            imageFilename = filename + '_z%.1f.tiff' % (verticalPosition_nm)
            imageFilepath = os.path.join(imagePath, imageFilename)

            imageFilepathOld, dummyExtension = os.path.splitext(filepath)
            imageFilepathOld += '_z%.1f.tiff' % (verticalPosition_nm)
            if os.path.isfile(imageFilepathOld):
                os.rename(imageFilepathOld, imageFilepath)

            if self._overwrite or not os.path.isfile(imageFilepath):
                values = histogramList[index]
                logging.debug("min: %f", np.min(values))
                logging.debug("max: %f", np.max(values))
                image = Image.fromarray(np.float32(values))

                image.save(imageFilepath)
                if index == 0:
                    image.save(masterImageFilepath)
                else:
                    try:
                        cmd = "convert -depth 32 -define quantum:format=floating-point %s -depth 32 -define quantum:format=floating-point %s -depth 32 -define quantum:format=floating-point -adjoin %s" % (masterImageFilepath, imageFilepath, masterImageFilepath)
                        os.system(cmd)
                        logging.debug(cmd)
                    except IOError:
                        print "cannot convert", imageFilepath

        if not keepAll:
            shutil.rmtree(imagePath)

    def _swapHistogramList(self, verticalPositions_nm, histogramList):
        # Swap XY images.
        histogramListSwapped = []

        lx = int(self._bins[0]/2.0)
        ly = int(self._bins[1]/2.0)

        for indexZ, dummy_verticalPosition_nm in enumerate(verticalPositions_nm):
            histogramListTemp = np.zeros_like(histogramList[indexZ])
            for indexX in xrange(self._bins[0]):
                for indexY in xrange(self._bins[1]):
                    if indexX < lx and indexY < ly:
                        swappedX = lx + indexX;
                        swappedY = ly + indexY;
                    elif indexX < lx:
                        swappedX = lx + indexX;
                        swappedY = indexY - ly;
                    elif indexY < ly:
                        swappedX = indexX - lx;
                        swappedY = ly + indexY;
                    else:
                        swappedX = indexX - lx;
                        swappedY = indexY - ly;

                    histogramListTemp[swappedX, swappedY] = histogramList[indexZ][indexX, indexY]

            histogramListSwapped.append(histogramListTemp)

        assert(len(histogramListSwapped) % 2 == 0)

        # Swap Z images.
        numberSlices = len(histogramListSwapped)
        if numberSlices == 1:
            return histogramListSwapped

        histogramListTemp = histogramListSwapped[:]

        size = int(numberSlices/2.0)
        offset = int((numberSlices)/2.0)
        for index1 in xrange(size):
            index2 = int(index1 + offset)
            #Swap slices s1 and s2.
            histogramListSwapped[index1] = histogramListTemp[index2]
            histogramListSwapped[index2] = histogramListTemp[index1]

        assert(len(histogramListSwapped) % 2 == 0)

        return histogramListSwapped

    def _writeAxisValues(self, folder="dataPsfs"):
        path = os.path.join(self.getSimulationPath(), folder)
        path = Files.createPath(path)

        # X
        filename = "AxisValuesX.csv"
        filepath = os.path.join(path, filename)

        writer = csv.writer(open(filepath, 'wb'))

        row = ["index", "x (nm)"]
        writer.writerow(row)

        xValues = sorted(self._setX)
        for index, x in enumerate(xValues):
            row = [index, x]
            writer.writerow(row)

        # Y
        filename = "AxisValuesY.csv"
        filepath = os.path.join(path, filename)

        writer = csv.writer(open(filepath, 'wb'))

        row = ["index", "y (nm)"]
        writer.writerow(row)

        values = sorted(self._setY)
        for index, value in enumerate(values):
            row = [index, value]
            writer.writerow(row)

    def _writeImageAxisValues(self, xSet, ySet, zSet, folder="dataPsfs"):
        path = os.path.join(self.getSimulationPath(), folder)
        path = Files.createPath(path)

        # X
        filename = "AxisValuesX.csv"
        filepath = os.path.join(path, filename)

        writer = csv.writer(open(filepath, 'wb'))

        row = ["index", "x (nm)"]
        writer.writerow(row)

        xValues = sorted(xSet)
        for index, x in enumerate(xValues):
            row = [index, x]
            writer.writerow(row)

        # Y
        filename = "AxisValuesY.csv"
        filepath = os.path.join(path, filename)

        writer = csv.writer(open(filepath, 'wb'))

        row = ["index", "y (nm)"]
        writer.writerow(row)

        values = sorted(ySet)
        for index, value in enumerate(values):
            row = [index, value]
            writer.writerow(row)

        # Z
        filename = "AxisValuesZ.csv"
        filepath = os.path.join(path, filename)

        writer = csv.writer(open(filepath, 'wb'))

        row = ["index", "z (nm)"]
        writer.writerow(row)

        values = sorted(zSet)
        for index, value in enumerate(values):
            row = [index, value]
            writer.writerow(row)

    def _writeAxiZValues(self, fz_nm, verticalPositions_nm, folder="dataPsfs"):
        path = os.path.join(self.getSimulationPath(), folder)
        path = Files.createPath(path)
        # Z
        filename = "AxisValuesZ_fz%inm.csv" % (fz_nm)
        filepath = os.path.join(path, filename)

        writer = csv.writer(open(filepath, 'wb'))

        row = ["index", "z (nm)"]
        writer.writerow(row)

        values = sorted(verticalPositions_nm)
        for index, value in enumerate(values):
            row = [index, value]
            writer.writerow(row)

    def _computePeakInfo(self, x, y, verbose=False, detailled=False):
        indexMiddle = int(len(x)/2.0)
        backgroundList = []
        backgroundList.extend(y[:20])
        backgroundList.extend(y[-20:])
        background = np.mean(backgroundList)
        if verbose:
            logging.info("background: %s", background)

        #maxValue = np.mean(y[indexMiddle-1:indexMiddle+1])
        maxValue = np.max(y)
        if verbose:
            logging.info("maxValue: %s", maxValue)

        signal = maxValue - background
        halfMaxValue = background + signal/2.0
        if verbose:
            logging.info("signal: %s", signal)
            logging.info("halfMaxValue: %s", halfMaxValue)

        index1 = indexMiddle
        for index1 in xrange(indexMiddle, 0, -1):
            yy = y[index1]
            if yy <= halfMaxValue:
                break
        if index1 == indexMiddle:
            x1 = x[0]
        else:
            x1 = x[index1]

        index2 = indexMiddle
        for index2 in xrange(indexMiddle, len(x), 1):
            yy = y[index2]
            if yy <= halfMaxValue:
                break
        if index2 == indexMiddle:
            x2 = x[-1]
        else:
            x2 = x[index2]
        if verbose:
            logging.info("x1: %s", x1)
            logging.info("x2: %s", x2)

        fwhm = abs(x2 - x1)
        snr = (signal)/math.sqrt(maxValue + background)
        if verbose:
            logging.info("fwhm: %s", fwhm)
            logging.info("snr: %s", snr)

        if detailled:
            return snr, fwhm, maxValue, halfMaxValue, background
        else:
            return snr, fwhm

    @property
    def resetCache(self):
        return self._resetCache
    @resetCache.setter
    def resetCache(self, resetCache):
        self._resetCache = resetCache

if __name__ == '__main__':    #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
