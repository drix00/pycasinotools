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

# Third party modules.

# Local modules.

# Globals and constants variables.

class BatchFile(object):
    def __init__(self, overwrite=True):
        self._overwrite = overwrite
        self._path = None
        self._batchBasename = None
        self._batchExtension = ".bat"
        self._scriptFilenames = []
        self._programName = "console_casino3_script_x64.exe"
        self._optionsPathDefaultFilepath = None

        self._numberSimulationsTodo = 0
        self._numberSimulationsDone = 0
        self._numberSimulationsTotal = 0

    def setPath(self, path):
        self._path = path

    def setBasename(self, basename):
        self._batchBasename = basename

    def setScriptPath(self, path):
        self._scriptPath = path

    def setScriptFilenames(self, scriptFilenames, todoNumberSimulations, doneNumberSimulations):
        self._scriptFilenames = scriptFilenames
        self._numberSimulationsTodo += todoNumberSimulations
        self._numberSimulationsDone += doneNumberSimulations
        self._numberSimulationsTotal += todoNumberSimulations + doneNumberSimulations

    def addScriptFilenames(self, scriptFilenames, todoNumberSimulations, doneNumberSimulations):
        self._scriptFilenames.extend(scriptFilenames)
        self._numberSimulationsTodo += todoNumberSimulations
        self._numberSimulationsDone += doneNumberSimulations
        self._numberSimulationsTotal += todoNumberSimulations + doneNumberSimulations

    def setOptionsPathDefaultFilepath(self, filepath):
        self._optionsPathDefaultFilepath = filepath

    def createFile(self, isWarning=True):
        lines = self._generateLines()

        batchFilepath = self._generateBatchFilepath()

        if not os.path.isfile(batchFilepath) or self._overwrite:
            if len(self._scriptFilenames) > 0:
                file = open(batchFilepath, 'wb')
                file.writelines(lines)
                return batchFilepath
            else:
                if isWarning:
                    logging.warning("Empty batch file, batch file (%s) not created", self._batchBasename)
                if os.path.isfile(batchFilepath):
                    logging.warning("Remove old batch file: (%s)", batchFilepath)
                    os.remove(batchFilepath)
                return None

    def _generateLines(self):
        lines = []

        line = r"@echo off"
        lines.append(line + '\n')

        if self._optionsPathDefaultFilepath != None:
            line = "cp Settings/Options_Path_Defaults.txt Settings/Options_Path_Defaults.txt.old"
            lines.append(line + '\n')
            line = "cp %s Settings/Options_Path_Defaults.txt" % (self._optionsPathDefaultFilepath)
            lines.append(line + '\n')

        total = len(self._scriptFilenames)
        done = 0
        for scriptFilename in self._scriptFilenames:
            scriptFilepath = os.path.join(self._scriptPath, scriptFilename)
            line = "%s %s" % (self._programName, scriptFilepath)
            lines.append(line + '\n')
            done += 1
            size = len(str(total))
            #line = "echo 'done %s/%s: %s'" % (done, total, scriptFilename)
            line = "echo 'done {0:{1}d}/{2:d}: {3:s}'".format(done, size, total, scriptFilename)
            lines.append(line + '\n')

        if self._optionsPathDefaultFilepath != None:
            line = "cp Settings/Options_Path_Defaults.txt.old Settings/Options_Path_Defaults.txt"
            lines.append(line + '\n')

        return lines

    def _generateBatchFilepath(self):
        batchFilename = self._batchBasename + self._batchExtension
        batchFilepath = os.path.join(self._path, batchFilename)

        return batchFilepath

    def copyRuntimeSettings(self, filepath):
        lines = open(self._generateBatchFilepath(), 'rb').readlines()

        newLines = []
        line =r"cp Settings/Runtime_Settings_Defaults.dat Settings/Runtime_Settings_Defaults.dat.old"
        newLines.append(line+'\n')
        line =r"cp %s Settings/Runtime_Settings_Defaults.dat" % (filepath)
        newLines.append(line+'\n')

        newLines.extend(lines)

        line =r"cp Settings/Runtime_Settings_Defaults.dat.old Settings/Runtime_Settings_Defaults.dat"
        newLines.append(line+'\n')

        batchFile = open(self._generateBatchFilepath(), 'wb')
        batchFile.writelines(newLines)

    def logInfo(self):
        assert (self._numberSimulationsDone+self._numberSimulationsTodo) == self._numberSimulationsTotal

        logging.info("%s", self._batchBasename)

        if self._numberSimulationsTotal > 0:
            percentage = 100.0*self._numberSimulationsDone/float(self._numberSimulationsTotal)
        else:
            percentage = 0.0
        logging.info("Simulation done: %i/%i (%.1f%%)", self._numberSimulationsDone, self._numberSimulationsTotal, percentage)

        if self._numberSimulationsTotal > 0:
            percentage = 100.0*self._numberSimulationsTodo/float(self._numberSimulationsTotal)
        else:
            percentage = 0.0
        logging.info("Simulation todo: %i/%i (%.1f%%)", self._numberSimulationsTodo, self._numberSimulationsTotal, percentage)
