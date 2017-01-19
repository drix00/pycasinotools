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

import casinotools.fileformat.casino3.OptionsPhysic as OptionsPhysic
import casinotools.fileformat.casino3.OptionsDist as OptionsDist
import casinotools.fileformat.casino3.OptionsMicro as OptionsMicro
import casinotools.fileformat.casino3.OptionsAdvBackSet as OptionsAdvBackSet
import casinotools.fileformat.casino3.OptionsXray as OptionsXray
import casinotools.fileformat.casino3.OptionsEnergyByPos as OptionsEnergyByPos
import casinotools.fileformat.casino3.OptionsADF as OptionsADF
import casinotools.fileformat.casino3.OptionsAdvancedPsfsSettings as OptionsAdvancedPsfsSettings
import casinotools.fileformat.casino3.Version as Version

# Globals and constants variables.

class SimulationOptions(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._optionsPhysic = OptionsPhysic.OptionsPhysic()
        self._optionsDist = OptionsDist.OptionsDist()
        self._optionsMicro = OptionsMicro.OptionsMicro()
        self._optionsAdvBackSet = OptionsAdvBackSet.OptionsAdvBackSet()
        self._optionsXray = OptionsXray.OptionsXray()
        self._optionsEnergyByPos = OptionsEnergyByPos.OptionsEnergyByPos()
        self._optionsADF = OptionsADF.OptionsADF()
        self._optionsAdvancedPsfsSettings = OptionsAdvancedPsfsSettings.OptionsAdvancedPsfsSettings()

        self._file = None
        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        tagID = b"*SIMULATIONOPT%"
        if self.findTag(file, tagID):
            self._version = self.readInt(file)

            self._optionsADF.read(file)
            self._optionsAdvBackSet.read(file)

            if self._version >= Version.SIM_OPTIONS_VERSION_3_3_0_0 and self._version < Version.SIM_OPTIONS_VERSION_3_3_0_4:
                self._optionsAdvancedPsfsSettings.read(file)

            self._optionsDist.read(file)
            self._optionsEnergyByPos.read(file)
            self._optionsMicro.read(file)
            self._optionsPhysic.read(file)

            self._optionsXray.read(file)

            tagID = b"*SIM_OPT_END%"
            if not self.findTag(file, tagID):
                return "Wrong version."

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

    def write(self, file):
        raise NotImplementedError

    def export(self, exportFile):
        # todo: implement the export method.
        pass

    def getOptionsDistributions(self):
        return self._optionsDist

    def getOptionsAdvancedPsfsSettings(self):
        return self._optionsAdvancedPsfsSettings
