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
import casinotools.file_format.file_reader_writer_tools as FileReaderWriterTools
import casinotools.file_format.casino3.version as Version
import casinotools.file_format.casino3.vector as Vector

# Globals and constants variables.

class OptionsAdvancedPsfsSettings(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, outputFile):
        pass

    def read(self, inputFile):
        assert inputFile.mode == 'rb'

        tagID = b"*PSF_SET_BEG"
        self.find_tag(inputFile, tagID)

        self._version = self.read_int(inputFile)
        assert self._version >= Version.SIM_OPTIONS_VERSION_3_3_0_0

        self._generatePsf = self.read_bool(inputFile)
        self._useScanPointForCenter = self.read_bool(inputFile)

        self._autoExportPsfData = self.read_bool(inputFile)
        self._exportTiff = self.read_bool(inputFile)
        self._exportCsv = self.read_bool(inputFile)
        self._exportStackedTiff = self.read_bool(inputFile)

        self._psfSize_nm.x = self.read_double(inputFile)
        self._psfSize_nm.y = self.read_double(inputFile)
        self._psfSize_nm.z = self.read_double(inputFile)

        self._psfNumberSteps.x = self.read_int(inputFile)
        self._psfNumberSteps.y = self.read_int(inputFile)
        self._psfNumberSteps.z = self.read_int(inputFile)

        self._psfCenter_nm.x = self.read_double(inputFile)
        self._psfCenter_nm.y = self.read_double(inputFile)
        self._psfCenter_nm.z = self.read_double(inputFile)

        tagID = b"*PSF_SET_END"
        self.find_tag(inputFile, tagID)

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
