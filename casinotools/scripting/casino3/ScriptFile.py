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
import logging
import stat

# Third party modules.

# Local modules.
from casinotools.scripting.casino3.Parameters import Parameters
from casinotools.scripting.casino3.StringParameters import StringParameters
from casinotools.scripting.casino3.StringArrayParameters import StringArrayParameters
from casinotools.scripting.casino3.NoParameters import NoParameters
from casinotools.scripting.casino3.RangedParameters import RangedParameters
from casinotools.scripting.casino3.RangedSampleParameters import RangedSampleParameters

import SimulationParameters as sp

# Globals and constants variables.

class ScriptFile(object):
    def __init__(self, basename, overwrite=True):
        self._overwrite = overwrite
        self._path = None
        self._basename = basename
        self._scriptFilename = None
        self._experiment = None

        self._repetitionNumber = None

        self._createParameters()
        self._createExperimentFunctions()

    def _createParameters(self):
        parameters = {}
        linesOrder = []

        command = StringParameters("LOAD")
        commandName = 'COMMAND_LOAD'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = NoParameters("ERASE_ALL_SCANPOINTS")
        commandName = 'COMMAND_ERASE_ALL_SCANPOINTS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = StringParameters("IMPORT_SCANPOINTS")
        commandName = 'COMMAND_IMPORT_SCANPOINTS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = StringArrayParameters("ADD_SCANPOINT")
        commandName = 'COMMAND_ADD_SCANPOINT'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET ENERGY", unit='keV')
        commandName = 'COMMAND_ENERGY'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Trajectories_Number", unit='e')
        commandName = 'COMMAND_NUMBER_TRAJECTORIES'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Beam_Radius", unit='nm', prefix='br')
        commandName = 'COMMAND_BEAM_RADIUS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Beam_Semi_Angle", unit='rad', prefix='bsa')
        commandName = 'COMMAND_BEAM_SEMI_ANGLE'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET FGenerateSecondary", prefix='se')
        commandName = 'COMMAND_GENERATE_SECONDARY'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Residual_Energy_Loss", unit='keV', prefix='rel')
        commandName = 'COMMAND_RESIDUAL_ENERGY_LOSS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET max_secondary_order", prefix='seo')
        commandName = 'COMMAND_MAX_SECONDARY_ORDER'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Min_Energy_Nosec", unit='keV', prefix='mwose')
        commandName = 'COMMAND_MIN_ENERGY_WO_SE'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Min_Energy_With_Sec", unit='keV', prefix='mwse')
        commandName = 'COMMAND_MIN_ENERGY_W_SE'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET Min_Gen_Secondary_Energy", unit='keV', prefix='mse')
        commandName = 'COMMAND_MIN_SE_ENERGY'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET FRan", prefix='R')
        commandName = 'COMMAND_RANDOM_NUMBER'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET FDeds", prefix='dEds')
        commandName = 'COMMAND_ENERGY_LOSS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET FTotalCross", prefix='TCS')
        commandName = 'COMMAND_TOTAL_CS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = Parameters("SET FPartialCross", prefix='PCS')
        commandName = 'COMMAND_PARTIAL_CS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        #COMMAND_SECTION_EFFICACES_IONISATION = Parameters("SET FSecIon")
        #COMMAND_MEAN_POTENTIAL = Parameters("SET FPotMoy")

        command = RangedSampleParameters("RANGE_SAMPLE TRANSLATION.z", unit='nm', prefix='z')
        commandName = 'COMMAND_SAMPLE_TRANSLATION_Z'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = RangedSampleParameters("RANGE_SAMPLE RADIUS", unit='nm', prefix='r')
        commandName = 'COMMAND_SAMPLE_RADIUS'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = RangedSampleParameters("RANGE_SAMPLE SCALE", unit='nm', prefix='s')
        commandName = 'COMMAND_SAMPLE_SCALE_Z'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = RangedSampleParameters("RANGE_SAMPLE DIVTHETA", unit='div')
        commandName = 'COMMAND_SAMPLE_DIV_THETA'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = RangedParameters("RANGE MICROSCOPE.Z_PLANE_POSITION", unit='nm', prefix='fz')
        commandName = 'COMMAND_MICROSCOPE_Z_PLANE_POSITION'
        parameters[commandName] = command
        linesOrder.append(commandName)

        command = StringParameters("SIM")
        commandName = 'COMMAND_SIM'
        parameters[commandName] = command
        linesOrder.append(commandName)

        self.__dict__.update(parameters)
        self._linesOrder = linesOrder

    def _createExperimentFunctions(self):
        self._experimentFunctions = {}
        self._experimentFunctions[sp.ENERGIES] = self.COMMAND_ENERGY
        self._experimentFunctions[sp.ERASE_ALL_SCANPOINTS] = self.COMMAND_ERASE_ALL_SCANPOINTS
        self._experimentFunctions[sp.SCAN_POINT_FILES] = self.COMMAND_IMPORT_SCANPOINTS
        self._experimentFunctions[sp.SCAN_POINT] = self.COMMAND_ADD_SCANPOINT
        self._experimentFunctions[sp.NUMBER_ELECTRONS] = self.COMMAND_NUMBER_TRAJECTORIES
        self._experimentFunctions[sp.FOCAL_PLANE_Z_LIST] = self.COMMAND_MICROSCOPE_Z_PLANE_POSITION
        self._experimentFunctions[sp.BEAM_RADIUS_nm] = self.COMMAND_BEAM_RADIUS
        self._experimentFunctions[sp.SEMI_ANGLES_rad] = self.COMMAND_BEAM_SEMI_ANGLE
        self._experimentFunctions[sp.SPHERE_RADIUS_nm] = self.COMMAND_SAMPLE_RADIUS
        self._experimentFunctions[sp.SPHERE_POSITION_Z_nm] = self.COMMAND_SAMPLE_TRANSLATION_Z
        self._experimentFunctions[sp.PLANE_POSITION_Z_nm] = self.COMMAND_SAMPLE_TRANSLATION_Z
        self._experimentFunctions[sp.TOTAL_CROSS_SECTION] = self.COMMAND_TOTAL_CS
        self._experimentFunctions[sp.PARTIAL_CROSS_SECTION] = self.COMMAND_PARTIAL_CS
        self._experimentFunctions[sp.SECONDARY_ELECTRON] = self.COMMAND_GENERATE_SECONDARY

    def setExperiment(self, experiment):
        self._experiment = experiment
        self._createFilename()

        for keyword in experiment:
            if type(keyword) == tuple:
                keywordF = keyword[0]
                shapeName = keyword[1]
                if keywordF in self._experimentFunctions:
                    value = experiment[keyword]
                    self._experimentFunctions[keywordF].setValue(value, shapeName)
                else:
                    logging.debug("No function for keyword: %s", keyword)
            elif keyword == sp.REPETITION:
                self._repetitionNumber = experiment[keyword]
            else:
                if keyword in self._experimentFunctions:
                    value = experiment[keyword]
                    self._experimentFunctions[keyword].setValue(value)
                else:
                    logging.debug("No function for keyword: %s", keyword)

    def _createFilename(self):
        if self._experiment == None:
            self._scriptFilename = self._generateSriptFilename()
        else:
            self._scriptFilename = "Script_" + self._experiment.getName(self._basename) + '.txt'

    def setPath(self, path):
        self._path = path

    def setBasename(self, basename):
        self._basename = basename

    def setSimulationPath(self, path):
        simulationFilename = self._experiment.getFilename()
        filepath = os.path.join(path, simulationFilename)
        self.COMMAND_LOAD.setValue(filepath)

    def setSimulationFilepath(self, filepath):
        self.COMMAND_LOAD.setValue(filepath)

    def setEnergy_keV(self, energy_keV):
        self.COMMAND_ENERGY.setValue(energy_keV)

    def setTrajectoryNumbers(self, numbers):
        self.COMMAND_NUMBER_TRAJECTORIES.setValue(numbers)

    def setResultsPath(self, path):
        filepath = os.path.join(path, self._experiment.getName(self._basename))
#        if self._repetitionNumber != None:
#            filepath += "_%s" % (self._repetitionNumber)
        filepath += '.cas'
        self.COMMAND_SIM.setValue(filepath)

    def setResultsFilepath(self, filepath):
        self.COMMAND_SIM.setValue(filepath)

    def getResultsFilepath(self):
        return self.COMMAND_SIM.getValue()

    def setSampleRadius(self, value, sampleObject):
        self.COMMAND_SAMPLE_RADIUS.setValue(value, sampleObject)

    def setSampleTranslationZ(self, value, sampleObject):
        self.COMMAND_SAMPLE_TRANSLATION_Z.setValue(value, sampleObject)

    def setSampleScaleZ(self, value, sampleObject):
        self.COMMAND_SAMPLE_SCALE_Z.setValue(value, sampleObject)

    def setSampleDivision(self, value, sampleObject):
        self.COMMAND_SAMPLE_DIV_THETA.setValue(value, sampleObject)

    def createFile(self):
        resultFilepath = self.getResultsFilepath()
        simulationFilepath = self._getSimulationFilepath()
        if self._overwrite and not self.isOlderThan(resultFilepath, simulationFilepath):
            return
        else:
            lines = self._generateLines()
            scriptFilepath = self._generateScriptFilepath()
            path, filename = os.path.split(scriptFilepath)

            if os.path.isdir(path):
                oldPath = os.getcwd()
                try:
                    os.chdir(path)
                    if not os.path.isfile(filename) or self._overwrite:
                        scriptFile = open(filename, 'wb')
                        scriptFile.writelines(lines)
                finally:
                    os.chdir(oldPath)

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

    def _generateLines(self):
        lines = []
        for commandKey in self._linesOrder:
            command = self.__dict__[commandKey]
            if command.isValueSet():
                lines.append(command.generateLine()+'\n')

        return lines

    def _generateSriptFilename(self):
        scriptFilename = self._basename
        if self._repetitionNumber != None:
            scriptFilename += "_%s" % (self._repetitionNumber)
        scriptFilename += '.txt'

        return scriptFilename

    def _generateScriptFilepath(self):
        if self._scriptFilename == None:
            self._createFilename()

        scriptFilepath = os.path.join(self._path, self._scriptFilename)
        return scriptFilepath

    def getScriptFilename(self):
        return self._scriptFilename

#    def getAllResultFilepaths(self):
#        simulationName = self._getSimulationName()
#        basename = self._resultsFilepath.replace(r"$(sim_name)", simulationName)
#
#        filepaths = []
#        if "$(ranged_value1)" in basename:
#            try:
#                min, max, step = self._ranges[0]._rangeValues
#                for value in np.arange(min, max+step, step):
#                    filepath = basename.replace("$(ranged_value1)", str(value))
#                    filepaths.append(filepath)
#            except:
#                pass
#
#        return filepaths

    def _getSimulationName(self):
        simulationFilepath = self.COMMAND_LOAD.getValue()
        basename, dummyExtension = os.path.splitext(os.path.basename(simulationFilepath))
        return basename

    def _getSimulationFilepath(self):
        return self.COMMAND_LOAD.getValue()
