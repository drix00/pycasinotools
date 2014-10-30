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
# Filename to store the defaults settings
OPTIONS_XRAY_DEF_FILENAME = "XRay_Settings_Defaults.dat"

#//--------------------------------------
#// XRays
#//--------------------------------------
#
#//-----------------------------------------------------------------------------
#/// Take off angle of the X-ray detector
#//-----------------------------------------------------------------------------
#    double TOA
#//-----------------------------------------------------------------------------
#/// Polar angle of the X-Ray detecteur
#//-----------------------------------------------------------------------------
#    float PhieRX
#//-----------------------------------------------------------------------------
class OptionsXray(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file,"*XRAY_OPT_BEG", 15)
#    writeVersion(file)
#
#    safewrite<double>(file, TOA)
#    safewrite<float>(file, PhieRX)
#
#    Tags::AddTag(file, "*XRAY_OPT_END", 15)

    def read(self, file):
        tagID = b"*XRAY_OPT_BEG"
        self.findTag(file, tagID)

        self._version = self.readInt(file)

        self.TOA = self.readDouble(file)
        self.PhieRX = self.readFloat(file)

        tagID = b"*XRAY_OPT_END"
        self.findTag(file, tagID)

    def reset(self):
        self.TOA = 40.0
        self.PhieRX = 0.0
