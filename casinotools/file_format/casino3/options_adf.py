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
import casinotools.file_format.file_reader_writer_tools as FileReaderWriterTools

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
        self.find_tag(file, tagID)

        self._version = self.read_int(file)

        self.DQE = self.read_double(file)

        self.Enabled = self.read_int(file)
        self.keepData = self.read_int(file)
        self.MaxAngle = self.read_double(file)
        self.MinAngle = self.read_double(file)
        self.MaxPoints = self.read_int(file)

        tagID = b"*ADF_SET_END"
        self.find_tag(file, tagID)

    def reset(self):
        # max semi-angle of the detector
        self.MinAngle = 0.200
        self.MaxAngle = 0.5
        self.Enabled = 1
        self.keepData = 0
        self.MaxPoints = 0
        #quantum efficiency of the detector
        self.DQE = 1
