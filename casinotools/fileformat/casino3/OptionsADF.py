#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.
#-----------------------------------------------------------------------------
#/ Filename to store the defaults settings
#-----------------------------------------
OPTIONS_ADF_DEF_FILENAME = "ADF_Settings_Defaults.dat"

class OptionsADF(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, file):
        pass
#    Tags::AddTag(file, "*ADF_SET_BEG", 15)
#    writeVersion(file)
#
#    safewrite<double>(file, DQE)
#    safewrite<int>(file, Enabled)
#    safewrite<int>(file, keepData)
#    safewrite<double>(file, MaxAngle)
#    safewrite<double>(file, MinAngle)
#    safewrite<int>(file, MaxPoints)
#
#    Tags::AddTag(file, "*ADF_SET_END", 15)}

    def read(self, file):
        tagID = b"*ADF_SET_BEG"
        self.findTag(file, tagID)

        self._version = self.readInt(file)

        self.DQE = self.readDouble(file)

        self.Enabled = self.readInt(file)
        self.keepData = self.readInt(file)
        self.MaxAngle = self.readDouble(file)
        self.MinAngle = self.readDouble(file)
        self.MaxPoints = self.readInt(file)

        tagID = b"*ADF_SET_END"
        self.findTag(file, tagID)

    def reset(self):
        # max semi-angle of the detector
        self.MinAngle = 0.200
        self.MaxAngle = 0.5
        self.Enabled = 1
        self.keepData = 0
        self.MaxPoints = 0
        #quantum efficiency of the detector
        self.DQE = 1
