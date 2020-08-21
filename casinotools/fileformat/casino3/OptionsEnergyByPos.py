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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools

# Globals and constants variables.
# Filename to store the defaults settings
OPTIONS_DEPOS_DEF_FILENAME = "EnergyByPosition_Settings_Defaults.dat"

# const definition for the energy display mode (XZ, XY or PROJECTION)
ENERGY_DISPLAY_XZ = 0
ENERGY_DISPLAY_XY = 1
ENERGY_DISPLAY_PROJECTION = 2

DEPOS_DIFFUSION_MINIMUM_ENERGY_DEFAULT = 1e-14

#//-----------------------------------------------------------------------------
#/// Sum the current distribution in DEpos distribution.
#//-----------------------------------------------------------------------------
#    int Depos_Summation
#//-----------------------------------------------------------------------------
#/// Flag telling the application to apply diffusion to the EnergyMatrix
#//-----------------------------------------------------------------------------
#    int Diffuse
#//-----------------------------------------------------------------------------
#/// Surface recombination value (used in diffuse calculation)
#//-----------------------------------------------------------------------------
#    double CarrierSurfaceRecombination
#//-----------------------------------------------------------------------------
#/// Energy display mode : see const definition above
#//-----------------------------------------------------------------------------
#    int XZorXY
#//-----------------------------------------------------------------------------
#/// Plane to draw when Summation==0    in DEpos
#//-----------------------------------------------------------------------------
#    int Yplane
#//-----------------------------------------------------------------------------
#/// Plane to draw when Summation==0    in DEpos
#//-----------------------------------------------------------------------------
#    int Zplane
#//-----------------------------------------------------------------------------
#/// Percentage of energy to display
#//-----------------------------------------------------------------------------
#    double DEpos_IsoLevel
#//-----------------------------------------------------------------------------
#/// normalize or not the energy with the volume of the indexes
#//-----------------------------------------------------------------------------
#    int normalize
class OptionsEnergyByPos(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file,"*EN_POS_SET_BEG", 15)
#    writeVersion(file)
#
#    safewrite<int>(file, Diffuse)
#    safewrite<int>(file, Depos_Summation)
#    safewrite<int>(file, XZorXY)
#    safewrite<int>(file, Yplane)
#    safewrite<int>(file, Zplane)
#    safewrite<double>(file, DEpos_IsoLevel)
#    safewrite<double>(file, CarrierSurfaceRecombination)
#    safewrite<int>(file, normalize)
#    double minimumDiffusionEnergy //obsolete
#    safewrite<double>(file, minimumDiffusionEnergy)
#
#    Tags::AddTag(file, "*EN_POS_SET_END", 15)

    def read(self, file):
        tagID = b"*EN_POS_SET_BEG"
        self.find_tag(file, tagID)

        self._version = self.read_int(file)

        self.Diffuse = self.read_int(file)

        self.Depos_Summation = self.read_int(file)
        self.XZorXY = self.read_int(file)
        self.Yplane = self.read_int(file)
        self.Zplane = self.read_int(file)
        self.DEpos_IsoLevel = self.read_double(file)

        self.CarrierSurfaceRecombination = self.read_double(file)

        self.normalize = self.read_int(file)

        #obsolete minimumDiffusionEnergy =
        self.read_double(file)

        tagID = b"*EN_POS_SET_END"
        self.find_tag(file, tagID)

    def reset(self):
        self.Diffuse = 0
        self.Depos_Summation = 1
        self.XZorXY = ENERGY_DISPLAY_XZ
        self.Yplane = 0
        self.Zplane = 0
        self.DEpos_IsoLevel = 0.1
        self.CarrierSurfaceRecombination = -1
        self.normalize = 1
