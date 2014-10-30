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

##-----------------------------------------------------------------------------
##/ Minimum angle for energy filter
##-----------------------------------------------------------------------------
#    double BEMin_Angle
##-----------------------------------------------------------------------------
##/ Maximum angle for Energy filter
##-----------------------------------------------------------------------------
#    double BEMax_Angle
##-----------------------------------------------------------------------------
##/ Maximum value of energy filter
##-----------------------------------------------------------------------------
#    double EFilterMax
##-----------------------------------------------------------------------------
##/ Minimum value of energy filter
##-----------------------------------------------------------------------------
#    double EFilterMin
##-----------------------------------------------------------------------------
##/ Middle values of energy filter
##-----------------------------------------------------------------------------
#    double EFilterVal[101]
##-----------------------------------------------------------------------------
##/ flag for doing filtration by energy(added to filter by position)
##-----------------------------------------------------------------------------
#    int FEFilter
##-----------------------------------------------------------------------------
#
##-------------------------------------------
## Setting of Backscattered electron detector
## Permit the setting of the sensibility of the backscattered electron detector
##-------------------------------------------
#
##-----------------------------------------------------------------------------
##/ Determine if using the advanced backscattered electron sensor settings :
##/ -true : Use them
##/ -false : Do not use them.
##-----------------------------------------------------------------------------
#    bool UseEnBack
##-----------------------------------------------------------------------------
##/ Backscattered electron sensor matrix setting
##-----------------------------------------------------------------------------
# TODO: implement the MatrixDetect variable and read data from file.
#    Matrix2d<double> MatrixDetect
##-----------------------------------------------------------------------------
##/ Working distance of the backscattered electron sensor.
##-----------------------------------------------------------------------------
#    double WorkDist
##-----------------------------------------------------------------------------
##/ Scale in X of one division of the sensor, in nm.
##-----------------------------------------------------------------------------
#    double DetectScaleX
##-----------------------------------------------------------------------------
##/ Scale in Y of one division of the sensor, in nm
##-----------------------------------------------------------------------------
#    double DetectScaleY
##-----------------------------------------------------------------------------
##/ Determine if the backscattered sensor matrix (MatrixDetect) is valid
##-----------------------------------------------------------------------------
#    bool ValidMatrix
##-----------------------------------------------------------------------------
##/ Name of the matrix file (and the path).
##-----------------------------------------------------------------------------
#    std::string pathToMatrix
##-----------------------------------------------------------------------------
class OptionsAdvBackSet(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file,"*MATRX_SET_BEG", 15)
#    OptionsGroup::writeVersion(file)
#
#    safewrite<bool>(file, UseEnBack)
#    safewrite<double>(file, WorkDist)
#    safewrite<double>(file, DetectScaleX)
#    safewrite<double>(file, DetectScaleY)
#    safewrite<bool>(file, ValidMatrix)
#
#    if(ValidMatrix == true)
#
#        for(int i = 0 i < 101 i++)
#
#            for(int j = 0 j < 101 j++)
#
#                safewrite<double>(file, MatrixDetect.get(i, j))
#
#
#
#
#    safewrite<double>(file, BEMin_Angle)
#    safewrite<double>(file, BEMax_Angle)
#    safewrite<double>(file, EFilterMax)
#    safewrite<double>(file, EFilterMin)
#
#    for(int i = 0 i < 101 i++)
#
#        safewrite<double>(file, EFilterVal[i])
#
#    safewrite<int>(file, FEFilter)
#
#    Tags::AddTag(file,"*MATRX_SET_END", 15)

    def read(self, file):
        tagID = b"*MATRX_SET_BEG"
        self.findTag(file, tagID)

        self._version = self.readInt(file)

        self.UseEnBack = self.readBool(file)
        self.WorkDist = self.readDouble(file)
        self.DetectScaleX = self.readDouble(file)
        self.DetectScaleY = self.readDouble(file)
        self.ValidMatrix = self.readBool(file)

        if self.ValidMatrix:
            raise NotImplementedError
#        for(int i = 0 i < 101 i++)
#            for(int j = 0 j < 101 j++)
#                double value
#                saferead<double>(file, value = self.readDouble(file)
#                MatrixDetect.set(i, j, value)

        self.BEMin_Angle = self.readDouble(file)
        self.BEMax_Angle = self.readDouble(file)
        self.EFilterMax = self.readDouble(file)
        self.EFilterMin = self.readDouble(file)

        for i in range(101):
            self.EFilterVal[i] = self.readDouble(file)

        self.FEFilter = self.readInt(file)

        tagID = b"*MATRX_SET_END"
        self.findTag(file, tagID)

    def reset(self):
        self.BEMin_Angle = 0.0
        self.BEMax_Angle = 0.0
        self.EFilterMax = 0.0
        self.EFilterMin = 0.0

        self.EFilterVal = []
        for dummy in range(101):
                self.EFilterVal.append(1.0)
        self.FEFilter = 0
        self.UseEnBack = False
        self.MatrixDetect = None
        self.WorkDist = 10.0
        self.DetectScaleX = 1.0
        self.DetectScaleY = 1.0
        self.ValidMatrix = False
