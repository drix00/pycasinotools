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
import casinotools.fileformat.casino3.Vector as Vector

# Globals and constants variables.

# Filename to store the defaults settings
OPTIONS_DIST_DEF_FILENAME = "Distribution_Settings_Defaults.dat"

#-----------------------------------------------------------------------------
#/ possible values for the RangeFinder parameter (used to specify how the range
#/ of the distributions are found.
#-----------------------------------------------------------------------------
RANGE_SIMULATED = 0
RANGE_OKAYAMA = 1
RANGE_HOVINGTON = 2
RANGE_FIXED = 3
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ possible values for the Energy by Position (DEpos) Distribution Type
#/ combo box
#-----------------------------------------------------------------------------
DIST_DEPOS_TYPE_CARTESIAN = 0 #cartesian
DIST_DEPOS_TYPE_CYLINDRIC = 1 #cylindric
DIST_DEPOS_TYPE_SPHERIC = 2 #spheric
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ possible value for the position of the center
#-----------------------------------------------------------------------------
DIST_DEPOS_POSITION_ABSOLUTE = 0
DIST_DEPOS_POSITION_RELATIVE = 1
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ Associated with RangeFinder
#-----------------------------------------------------------------------------
RANGE_SAFETY_FACTOR = 1.5
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ value indicating that this value of the distribution is to be determined
#/ automatically.
#-----------------------------------------------------------------------------
autoFlag = -4e34
#-----------------------------------------------------------------------------

#//--------------------------------------
#// Flags for distributions
#//--------------------------------------
#
#//-----------------------------------------------------------------------------
#/// Flag to generate X-Ray
#//-----------------------------------------------------------------------------
#    int    FEmissionRX;
#    int FEmissionRXLog;
#    int NbreCoucheRX;
#//-----------------------------------------------------------------------------
#/// Distribution of the maximum dethp
#//-----------------------------------------------------------------------------
#    int FDZmax;
#    int FDZmaxLog;
#    int NbPointDZMax;
#    double DZmaxMax;
#    double DZmaxMin;
#//-----------------------------------------------------------------------------
#/// Distribution of Energy of the backscattered electron
#//-----------------------------------------------------------------------------
#    int FDenr;
#    int FDenrLog;
#    int NbPointDENR;
#    double DenrMax;
#    double DenrMin;
#//-----------------------------------------------------------------------------
#/// Distribution of Energy of the transmitted electron
#//-----------------------------------------------------------------------------
#    int FDent;
#    int FDentLog;
#    int NbPointDENT;
#    double DentMax;
#    double DentMin;
#//-----------------------------------------------------------------------------
#/// Distribution of the escape radius of the backscattered electorn
#//-----------------------------------------------------------------------------
#    int FDrsr;
#    int FDrsrLog;
#    int NbPointDRSR;
#    double DrsrMax;
#    double DrsrMin;
#//-----------------------------------------------------------------------------
#/// Distribution of the Backscattered electron angle relative to Z axis
#//-----------------------------------------------------------------------------
#    int FDbang;
#    int FDbangLog;
#    int NbPointDBANG;
#    double DbangMax;
#    double DbangMin;
#//-----------------------------------------------------------------------------
#
#
#//--------------------------------------
#// DEpos : Distribution of energy by position
#//--------------------------------------
#    int Flag_Energy_Density;
#    int DEpos_Type;
#
#    int NbPointDEpos_X;
#    int NbPointDEpos_Y;
#    int NbPointDEpos_Z;
#    int DEpos_LogX;
#    int DEpos_LogY;
#    int DEpos_LogZ;
#
#    vector<double> DEpos_Center;
#    vector<double> DEpos_Size;
#
#    int DEposSpheric_Rad_Div;
#    double DEposSpheric_Rad;
#    int DEposSpheric_Rad_Log;
#
#    int DEposCyl_Rad_Div;
#    double DEposCyl_Rad;
#    int DEposCyl_Rad_Log;
#    int DEposCyl_Z_Div;
#    double DEposCyl_Z;
#    int DEposCyl_Z_Log;
#
#    int DEpos_Position;
#//-----------------------------------------------------------------------------
#
#///--------------------------------------
#// Range
#///--------------------------------------
#
#//-----------------------------------------------------------------------------
#/// Max Range Parameter from the Distribution dialog.
#/// @note : see possible values above
#//-----------------------------------------------------------------------------
#    int RangeFinder;
#//-----------------------------------------------------------------------------
class OptionsDist(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file, "*DIST_OPT_BEG", 15);
#    writeVersion(file);
#
#    safewrite<double>(file, DenrMax);
#    safewrite<double>(file, DenrMin);
#    safewrite<double>(file, DentMax);
#    safewrite<double>(file, DentMin);
#    safewrite<double>(file, DrsrMax);
#    safewrite<double>(file, DrsrMin);
#    safewrite<double>(file, DZmaxMax);
#    safewrite<double>(file, DZmaxMin);
#    safewrite<double>(file, DbangMax);
#    safewrite<double>(file, DbangMin);
#
#    safewrite<int>(file, FDZmaxLog);
#    safewrite<int>(file, FDenrLog);
#    safewrite<int>(file, FDentLog);
#    safewrite<int>(file, FDrsrLog);
#    safewrite<int>(file, FDbangLog);
#    safewrite<int>(file, FEmissionRXLog);
#
#    safewrite<int>(file, FEmissionRX);
#    safewrite<int>(file, FDZmax);
#    safewrite<int>(file, FDenr);
#    safewrite<int>(file, FDent);
#    safewrite<int>(file, FDrsr);
#    safewrite<int>(file, Flag_Energy_Density);
#    safewrite<int>(file, FDbang);
#
#    safewrite<int>(file, NbPointDZMax);
#    safewrite<int>(file, NbPointDENR);
#    safewrite<int>(file, NbPointDENT);
#    safewrite<int>(file, NbPointDRSR);
#    safewrite<int>(file, NbPointDEpos_X);
#    safewrite<int>(file, NbPointDEpos_Y);
#    safewrite<int>(file, NbPointDEpos_Z);
#    safewrite<int>(file, NbPointDBANG);
#
#    safewrite<int>(file, RangeFinder);
#
#    safewrite<double>(file, DEpos_Center.x);
#    safewrite<double>(file, DEpos_Center.y);
#    safewrite<double>(file, DEpos_Center.z);
#    safewrite<double>(file, DEpos_Size.x);
#    safewrite<double>(file, DEpos_Size.y);
#    safewrite<double>(file, DEpos_Size.z);
#
#    //---------------------------
#    // added : version 3010405
#    safewrite<int>(file, DEpos_Type);
#
#    safewrite<int>(file, DEposSpheric_Rad_Div);
#    safewrite<double>(file, DEposSpheric_Rad);
#    safewrite<int>(file, DEposSpheric_Rad_Log);
#
#    safewrite<int>(file, DEposCyl_Rad_Div);
#    safewrite<double>(file, DEposCyl_Rad);
#    safewrite<int>(file, DEposCyl_Rad_Log);
#    safewrite<int>(file, DEposCyl_Z_Div);
#    safewrite<double>(file, DEposCyl_Z);
#    safewrite<int>(file, DEposCyl_Z_Log);
#
#    //new version 30104072
#    safewrite<int>(file, DEpos_Position);
#    //---------------------------
#
#    Tags::AddTag(file, "*DIST_OPT_END", 15);

    def read(self, file):
        tagID = b"*DIST_OPT_BEG"
        self.find_tag(file, tagID)

        self._version = self.read_int(file)

        self.DenrMax = self.read_double(file)
        self.DenrMin = self.read_double(file)
        self.DentMax = self.read_double(file)
        self.DentMin = self.read_double(file)
        self.DrsrMax = self.read_double(file)
        self.DrsrMin = self.read_double(file)
        self.DZmaxMax = self.read_double(file)
        self.DZmaxMin = self.read_double(file)
        self.DbangMax = self.read_double(file)
        self.DbangMin = self.read_double(file)

        self.FDZmaxLog = self.read_int(file)
        self.FDenrLog = self.read_int(file)
        self.FDentLog = self.read_int(file)
        self.FDrsrLog = self.read_int(file)
        self.FDbangLog = self.read_int(file)
        self.FEmissionRXLog = self.read_int(file)

        self.FEmissionRX = self.read_int(file)
        self.FDZmax = self.read_int(file)
        self.FDenr = self.read_int(file)
        self.FDent = self.read_int(file)
        self.FDrsr = self.read_int(file)
        self.Flag_Energy_Density = self.read_int(file)
        self.FDbang = self.read_int(file)

        self.NbPointDZMax = self.read_int(file)
        self.NbPointDENR = self.read_int(file)
        self.NbPointDENT = self.read_int(file)
        self.NbPointDRSR = self.read_int(file)
        self.NbPointDEpos_X = self.read_int(file)
        self.NbPointDEpos_Y = self.read_int(file)
        self.NbPointDEpos_Z = self.read_int(file)
        self.NbPointDBANG = self.read_int(file)

        self.RangeFinder = self.read_int(file)

        self.DEpos_Center.x = self.read_double(file)
        self.DEpos_Center.y = self.read_double(file)
        self.DEpos_Center.z = self.read_double(file)
        self.DEpos_Size.x = self.read_double(file)
        self.DEpos_Size.y = self.read_double(file)
        self.DEpos_Size.z = self.read_double(file)

        self.DEpos_Type = self.read_int(file)

        self.DEposSpheric_Rad_Div = self.read_int(file)
        self.DEposSpheric_Rad = self.read_double(file)
        self.DEposSpheric_Rad_Log = self.read_int(file)

        self.DEposCyl_Rad_Div = self.read_int(file)
        self.DEposCyl_Rad = self.read_double(file)
        self.DEposCyl_Rad_Log = self.read_int(file)
        self.DEposCyl_Z_Div = self.read_int(file)
        self.DEposCyl_Z = self.read_double(file)
        self.DEposCyl_Z_Log = self.read_int(file)

        self.DEpos_Position = self.read_int(file)

        tagID = b"*DIST_OPT_END"
        self.find_tag(file, tagID)

    def reset(self):
        self.FDZmax = 1;
        self.FDZmaxLog = 0;
        self.NbPointDZMax = 1000;
        self.DZmaxMax = autoFlag;
        self.DZmaxMin = autoFlag;

        self.FDenr = 1;
        self.FDenrLog = 0;
        self.NbPointDENR = 500;
        self.DenrMax = autoFlag;
        self.DenrMin = autoFlag;

        self.FDent = 1;
        self.FDentLog = 0;
        self.NbPointDENT = 500;
        self.DentMax = autoFlag;
        self.DentMin = autoFlag;

        self.FDrsr = 1;
        self.FDrsrLog = 0;
        self.NbPointDRSR = 500;
        self.DrsrMax = autoFlag;
        self.DrsrMin = autoFlag;

        self.FDbang = 1;
        self.FDbangLog = 0;
        self.NbPointDBANG = 91;
        self.DbangMax = autoFlag;
        self.DbangMin = autoFlag;

        self.FEmissionRX = 1;
        self.FEmissionRXLog = 0;
        self.NbreCoucheRX = 500;

        self.RangeFinder = RANGE_SIMULATED;

        self.Flag_Energy_Density = 1;
        self.DEpos_Type = 0;

        self.NbPointDEpos_X = 50;
        self.NbPointDEpos_Y = 50;
        self.NbPointDEpos_Z = 50;

        self.DEpos_Center = Vector.Vector(0.0, 0.0, 0.0);
        self.DEpos_Size = Vector.Vector(1000.0, 1000.0, 1000.0);

        self.DEposSpheric_Rad_Div = 50;
        self.DEposSpheric_Rad = 1000;
        self.DEposSpheric_Rad_Log = 0;

        self.DEposCyl_Rad_Div = 50;
        self.DEposCyl_Rad = 1000;
        self.DEposCyl_Rad_Log = 0;
        self.DEposCyl_Z_Div = 50;
        self.DEposCyl_Z = 1000;
        self.DEposCyl_Z_Log = 0;

        self.DEpos_Position = DIST_DEPOS_POSITION_ABSOLUTE;

    def getDepositedEnergyCenter_nm(self):
        return self.DEpos_Center

    def getDepositedEnergySize_nm(self):
        return self.DEpos_Size
