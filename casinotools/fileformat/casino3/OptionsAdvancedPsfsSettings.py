#!/usr/bin/env python
"""
.. py:currentmodule:: FileFormat.casino3.OptionsAdvancedPsfsSettings
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

OptionsAdvancedPsfsSettings module for CASINO v3.3
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Project modules
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.Version as Version
import casinotools.fileformat.casino3.Vector as Vector

# Globals and constants variables.

class OptionsAdvancedPsfsSettings(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, outputFile):
        pass

    def read(self, inputFile):
        assert inputFile.mode == 'rb'

        tagID = b"*PSF_SET_BEG"
        self.findTag(inputFile, tagID)

        self._version = self.readInt(inputFile)
        assert self._version >= Version.SIM_OPTIONS_VERSION_3_3_0_0

        self._generatePsf = self.readBool(inputFile)
        self._useScanPointForCenter = self.readBool(inputFile)

        self._autoExportPsfData = self.readBool(inputFile)
        self._exportTiff = self.readBool(inputFile)
        self._exportCsv = self.readBool(inputFile)
        self._exportStackedTiff = self.readBool(inputFile)

        self._psfSize_nm.x = self.readDouble(inputFile)
        self._psfSize_nm.y = self.readDouble(inputFile)
        self._psfSize_nm.z = self.readDouble(inputFile)

        self._psfNumberSteps.x = self.readInt(inputFile)
        self._psfNumberSteps.y = self.readInt(inputFile)
        self._psfNumberSteps.z = self.readInt(inputFile)

        self._psfCenter_nm.x = self.readDouble(inputFile)
        self._psfCenter_nm.y = self.readDouble(inputFile)
        self._psfCenter_nm.z = self.readDouble(inputFile)

        tagID = b"*PSF_SET_END"
        self.findTag(inputFile, tagID)

    def reset(self):
        self._generatePsf = True;
        self._useScanPointForCenter = True;

        self._autoExportPsfData = True;
        self._exportTiff = True;
        self._exportCsv = True;
        self._exportStackedTiff = True;

        self._psfSize_nm = Vector.Vector(128.0 * 1.0, 128.0 * 1.0, 128.0 * 5.0);
        self._psfNumberSteps = Vector.Vector(128, 128, 128);
        self._psfCenter_nm = Vector.Vector(0.0, 0.0, 500.0);

    def isGeneratingPSFs(self):
        return self._generatePsf

    def getUseScanPointForCenter(self):
        return self._useScanPointForCenter

    def getPsfCenter_nm(self):
        return self._psfCenter_nm

    def getNumberStepsX(self):
        return self._psfNumberSteps.x

    def getNumberStepsY(self):
        return self._psfNumberSteps.y

    def getNumberStepsZ(self):
        return self._psfNumberSteps.z
