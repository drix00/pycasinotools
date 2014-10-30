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
OPTIONS_MICRO_DEF_FILENAME = "Microscope_Settings_Defaults.dat"

# const for the Beam_Distribution option :
# BEAM_DIST_GAUSSIAN : Gaussian Distribution using variance Beam_Variance
# BEAM_DIST_UNIFORM : Uniform Distribution
BEAM_DIST_GAUSSIAN = 0
BEAM_DIST_UNIFORM = 1

# const for the Noise Type for the number of electrons trajectories
NOISE_TYPE_SHOT = 1
NOISE_TYPE_PERCENTAGE = 2
NOISE_TYPE_DEFAULT = NOISE_TYPE_PERCENTAGE
NOISE_PERCENTAGE_DEFAULT = 0

# const for the scanning mode (XY, XZ or YZ)
MODE_XY_SCAN = 0
MODE_XZ_SCAN = 1
MODE_YZ_SCAN = 2
SCANNING_MODE_DEFAULT = MODE_XY_SCAN

# const for the Cone Beam settings
# CONE_FOCUS_AFTER : the smallest point will be after the focus point, who will
# have the width of Beam Diameter
# CONE_FOCUS_BEFORE : the smallest point will be before the focus point, who will
# have the width of Beam Diameter
# CONE_FOCUS_AFTER2 : Another Focus Algorythm we test for the moment
# CONE_FOCUS_NONE : Algo that the smallest point will be the width of the beam
# diameter, altough the angles will be a little randomised
CONE_FOCUS_AFTER = 0
CONE_FOCUS_BEFORE = 1
CONE_FOCUS_AFTER2 = 2
CONE_FOCUS_NONE = 3

# Default values for Advanced Beam options
BEAM_APERTURE_WIDTH_DEFAULT = 0
BEAM_VARIANCE_DEFAULT = 1.65
BEAM_DISTRIBUTION_DEFAULT = BEAM_DIST_GAUSSIAN
Z_PLANE_POSITION_DEFAULT = 0
Y_PLANE_POSITION_DEFAULT = 0
X_PLANE_POSITION_DEFAULT = 0
BEAM_CONEALGO_DEFAULT = CONE_FOCUS_NONE

#//--------------------------------------
#// Microscope settings
#//--------------------------------------
#
#//-----------------------------------------------------------------------------
## Angle du faisceau d'electrons du microscope. Definition du microscope
#//-----------------------------------------------------------------------------
#    double Beam_angle
#//-----------------------------------------------------------------------------
##Nombre d'electrons par point de simulation du microscope. Definition du microscope
#//-----------------------------------------------------------------------------
#    int Trajectories_Number
#//-----------------------------------------------------------------------------
## Puissance du faisceau en KeV a la derniere simulation.
## Permet de refaire les scan points de la simulation avec plusieurs energies differentes
#//-----------------------------------------------------------------------------
#    double KEV_End
#//-----------------------------------------------------------------------------
## Puissance du faisceau en KeV a la premiere simulation.
## Permet de refaire les scan points de la simulation avec plusieurs energies differentes
#//-----------------------------------------------------------------------------
#    double KEV_Start
#//-----------------------------------------------------------------------------
## Increment de puissance entre 2 simulations.
## Permet de refaire les scan points de la simulation avec plusieurs energies differentes
#//-----------------------------------------------------------------------------
#    double KEV_Step
#//-----------------------------------------------------------------------------
## Flag indicating if we use multiple scan points.
## 0 = No, positive = Yes.
#//-----------------------------------------------------------------------------
#    int Multiple_Scan_Energy
#//-----------------------------------------------------------------------------
#
#//-----------------------------------------------------------------------------
## Determine if we keep the simulation datas necessary to view the distributions.
#//-----------------------------------------------------------------------------
#    int keep_simulation_data
#//-----------------------------------------------------------------------------
#
#//--------------------------------------
#// Microscope settings - Beam Settings
#//--------------------------------------
#
#//-----------------------------------------------------------------------------
## Beam radius.
#//-----------------------------------------------------------------------------
#    double Beam_Radius
#//-----------------------------------------------------------------------------
## Beam Aperture Angle in Rad.
#//-----------------------------------------------------------------------------
#    double Beam_ApertureWidth
#//-----------------------------------------------------------------------------
## Z_plane_position position of the focal point when mode is XY scanning
## Y_plane_position position of the Y plane when mode is XZ scanning
## X_plane_position position of the X plane when mode is YZ scanning
#//-----------------------------------------------------------------------------
#    double Z_plane_position
#    double Y_plane_position
#    double X_plane_position
#//-----------------------------------------------------------------------------
## scanning mode : can be MODE_XY_SCAN, MODE_XZ_SCAN, MODE_YZ_SCAN
#//-----------------------------------------------------------------------------
#    int scanning_mode
#//-----------------------------------------------------------------------------
## Beam Distribution Variance Used in the Gaussian Distribution
#//-----------------------------------------------------------------------------
#    double Beam_Dist_Variance
#//-----------------------------------------------------------------------------
## Beam Distribution Type
## See related const BEAM_DIST_ above
#//-----------------------------------------------------------------------------
#    int Beam_Distribution
#//-----------------------------------------------------------------------------
## Avanced beam options flag
#//-----------------------------------------------------------------------------
#    int Beam_AdvSet
#//-----------------------------------------------------------------------------
## Cone Beam Algorythm used in cone beam calculation
#//-----------------------------------------------------------------------------
#    int Beam_ConeAlgo
#//-----------------------------------------------------------------------------
#// Electron beam diameter
#//-----------------------------------------------------------------------------
#//    int BeamDiam
#//-----------------------------------------------------------------------------
#
#//-----------------------------------------------------------------------------
## Noise settings for electrons trajectories numbers
#//-----------------------------------------------------------------------------
#    int NoiseType
#    int NoiseEnabled
#    double NoisePercentage
#//-----------------------------------------------------------------------------
## Flag determining if we simulate secondary electrons.
## Activated by the user in the settings dialogs.
#//-----------------------------------------------------------------------------
#    int FGenerateSecondary
#//-----------------------------------------------------------------------------
## Flag determinig if we generate X-Rays -- Not Used Right Now --.
## Activated by the user in the settings dialogs. Should be used when
## X-Rays will be reinplemented correctly.
#//-----------------------------------------------------------------------------
#    int FGenerateXRays
#//-----------------------------------------------------------------------------
## keep in memory the distance between scan point for the microscope settings dialog
#    float scanPtDist
#//-----------------------------------------------------------------------------

class OptionsMicro(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file, "*MICRO_SET_BEG", 15)
#        writeVersion(file)
#
#    //--New version 3.1.4.6
#    safewrite<int>(file, scanning_mode)
#    safewrite<double>(file, X_plane_position)
#    safewrite<double>(file, Y_plane_position)
#    //--
#
#    safewrite<int>(file, NoiseType)
#    safewrite<int>(file, NoiseEnabled)
#    safewrite<double>(file, NoisePercentage)
#
#    safewrite<double>(file, Beam_angle)
#    safewrite<double>(file, Beam_Radius)
#    safewrite<double>(file, Beam_ApertureWidth)
#    safewrite<double>(file, Z_plane_position)
#    safewrite<double>(file, Beam_Dist_Variance)
#    safewrite<int>(file, Beam_Distribution)
#    safewrite<int>(file, Beam_AdvSet)
#
#    safewrite<int>(file, Trajectories_Number)
#    safewrite<double>(file, KEV_End)
#    safewrite<double>(file, KEV_Start)
#    safewrite<double>(file, KEV_Step)
#    safewrite<int>(file, Multiple_Scan_Energy)
#    safewrite<int>(file, FGenerateSecondary)
#    safewrite<int>(file, FGenerateXRays)
#    safewrite<float>(file, scanPtDist)
#    safewrite<int>(file, keep_simulation_data)
#
#    Tags::AddTag(file, "*MICRO_SET_END", 15)

    def read(self, file):
        tagID = b"*MICRO_SET_BEG"
        self.findTag(file, tagID)

        self._version = self.readInt(file)

        self.scanning_mode = self.readInt(file)
        self.X_plane_position = self.readDouble(file)
        self.Y_plane_position = self.readDouble(file)

        self.NoiseType = self.readInt(file)
        self.NoiseEnabled = self.readInt(file)
        self.NoisePercentage = self.readDouble(file)

        self.Beam_angle = self.readDouble(file)
        self.Beam_Radius = self.readDouble(file)
        self.Beam_ApertureWidth = self.readDouble(file)
        self.Z_plane_position = self.readDouble(file)
        self.Beam_Dist_Variance = self.readDouble(file)
        self.Beam_Distribution = self.readInt(file)
        self.Beam_AdvSet = self.readInt(file)

        self.Trajectories_Number = self.readInt(file)
        self.KEV_End = self.readDouble(file)
        self.KEV_Start = self.readDouble(file)
        self.KEV_Step = self.readDouble(file)
        self.Multiple_Scan_Energy = self.readInt(file)
        self.FGenerateSecondary = self.readInt(file)
        self.FGenerateXRays = self.readInt(file)
        self.scanPtDist = self.readFloat(file)
        self.keep_simulation_data = self.readInt(file)

        tagID = b"*MICRO_SET_END"
        self.findTag(file, tagID)

    def reset(self):
        self.Beam_angle = 0.0
        self.Trajectories_Number = 1000
        self.KEV_End = 0.0
        self.KEV_Start = 1.0
        self.KEV_Step = 1.0
        self.Multiple_Scan_Energy = 0

        self.Beam_Radius = 5.0
        self.Beam_AdvSet = 0
        self.Beam_Dist_Variance = BEAM_VARIANCE_DEFAULT

        self.Z_plane_position = Z_PLANE_POSITION_DEFAULT
        self.Y_plane_position = Y_PLANE_POSITION_DEFAULT
        self.X_plane_position = X_PLANE_POSITION_DEFAULT
        self.scanning_mode = SCANNING_MODE_DEFAULT

        self.Beam_ApertureWidth = BEAM_APERTURE_WIDTH_DEFAULT
        self.Beam_Distribution = BEAM_DISTRIBUTION_DEFAULT
        self.Beam_ConeAlgo = BEAM_CONEALGO_DEFAULT

        self.FGenerateSecondary = 0
        self.FGenerateXRays = 0
        self.keep_simulation_data = 0
        self.scanPtDist = 1

        # Noise Settings
        self.NoiseType = NOISE_TYPE_DEFAULT
        self.NoiseEnabled = False
        self.NoisePercentage = NOISE_PERCENTAGE_DEFAULT
