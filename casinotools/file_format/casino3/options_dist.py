#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_dist
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
"""

###############################################################################
# Copyright 2020 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, read_double
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino3.vector import Vector

# Globals and constants variables.
# Filename to store the defaults settings
OPTIONS_DIST_DEF_FILENAME = "Distribution_Settings_Defaults.dat"

# possible values for the RangeFinder parameter (used to specify how the range
# of the distributions are found.
RANGE_SIMULATED = 0
RANGE_OKAYAMA = 1
RANGE_HOVINGTON = 2
RANGE_FIXED = 3

# possible values for the Energy by Position (DEpos) Distribution Type
# combo box
DIST_DEPOS_TYPE_CARTESIAN = 0  # cartesian
DIST_DEPOS_TYPE_CYLINDRIC = 1  # cylindrical
DIST_DEPOS_TYPE_SPHERIC = 2  # spherical

# possible value for the position of the center_nm
DIST_DEPOS_POSITION_ABSOLUTE = 0
DIST_DEPOS_POSITION_RELATIVE = 1

# Associated with RangeFinder
RANGE_SAFETY_FACTOR = 1.5

# value indicating that this value of the distribution is to be determined
# automatically.
autoFlag = -4e34

# Flags for distributions
# Flag to generate X-Ray
#    int    FEmissionRX
#    int FEmissionRXLog
#    int NbreCoucheRX

# Distribution of the maximum dethp
#    int FDZmax
#    int FDZmaxLog
#    int NbPointDZMax
#    double DZmaxMax
#    double DZmaxMin

# Distribution of Energy of the backscattered electron
#    int FDenr
#    int FDenrLog
#    int NbPointDENR
#    double DenrMax
#    double DenrMin

# Distribution of Energy of the transmitted electron
#    int FDent
#    int FDentLog
#    int NbPointDENT
#    double DentMax
#    double DentMin

# Distribution of the escape radius of the backscattered electorn
#    int FDrsr
#    int FDrsrLog
#    int NbPointDRSR
#    double DrsrMax
#    double DrsrMin

# Distribution of the Backscattered electron angle relative to z axis
#    int FDbang
#    int FDbangLog
#    int NbPointDBANG
#    double DbangMax
#    double DbangMin

# DEpos : Distribution of energy by position
#    int Flag_Energy_Density
#    int DEpos_Type

#    int NbPointDEpos_X
#    int NbPointDEpos_Y
#    int NbPointDEpos_Z
#    int DEpos_LogX
#    int DEpos_LogY
#    int DEpos_LogZ

#    vector<double> DEpos_Center
#    vector<double> DEpos_Size

#    int DEposSpheric_Rad_Div
#    double DEposSpheric_Rad
#    int DEposSpheric_Rad_Log

#    int DEposCyl_Rad_Div
#    double DEposCyl_Rad
#    int DEposCyl_Rad_Log
#    int DEposCyl_Z_Div
#    double DEposCyl_Z
#    int DEposCyl_Z_Log

#    int DEpos_Position

# Range
# Max Range Parameter from the Distribution dialog.
# @note : see possible values above
#    int RangeFinder


class OptionsDist:
    def __init__(self):
        self.FDZmax = 1
        self.FDZmaxLog = 0
        self.NbPointDZMax = 1000
        self.DZmaxMax = autoFlag
        self.DZmaxMin = autoFlag

        self.FDenr = 1
        self.FDenrLog = 0
        self.NbPointDENR = 500
        self.DenrMax = autoFlag
        self.DenrMin = autoFlag

        self.FDent = 1
        self.FDentLog = 0
        self.NbPointDENT = 500
        self.DentMax = autoFlag
        self.DentMin = autoFlag

        self.FDrsr = 1
        self.FDrsrLog = 0
        self.NbPointDRSR = 500
        self.DrsrMax = autoFlag
        self.DrsrMin = autoFlag

        self.FDbang = 1
        self.FDbangLog = 0
        self.NbPointDBANG = 91
        self.DbangMax = autoFlag
        self.DbangMin = autoFlag

        self.FEmissionRX = 1
        self.FEmissionRXLog = 0
        self.NbreCoucheRX = 500

        self.RangeFinder = RANGE_SIMULATED

        self.Flag_Energy_Density = 1
        self.DEpos_Type = 0

        self.NbPointDEpos_X = 50
        self.NbPointDEpos_Y = 50
        self.NbPointDEpos_Z = 50

        self.DEpos_Center = Vector(0.0, 0.0, 0.0)
        self.DEpos_Size = Vector(1000.0, 1000.0, 1000.0)

        self.DEposSpheric_Rad_Div = 50
        self.DEposSpheric_Rad = 1000
        self.DEposSpheric_Rad_Log = 0

        self.DEposCyl_Rad_Div = 50
        self.DEposCyl_Rad = 1000
        self.DEposCyl_Rad_Log = 0
        self.DEposCyl_Z_Div = 50
        self.DEposCyl_Z = 1000
        self.DEposCyl_Z_Log = 0

        self.DEpos_Position = DIST_DEPOS_POSITION_ABSOLUTE

        self.version = 0

        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file, "*DIST_OPT_BEG", 15)
#    writeVersion(file)
#
#    safe_write<double>(file, DenrMax)
#    safe_write<double>(file, DenrMin)
#    safe_write<double>(file, DentMax)
#    safe_write<double>(file, DentMin)
#    safe_write<double>(file, DrsrMax)
#    safe_write<double>(file, DrsrMin)
#    safe_write<double>(file, DZmaxMax)
#    safe_write<double>(file, DZmaxMin)
#    safe_write<double>(file, DbangMax)
#    safe_write<double>(file, DbangMin)
#
#    safe_write<int>(file, FDZmaxLog)
#    safe_write<int>(file, FDenrLog)
#    safe_write<int>(file, FDentLog)
#    safe_write<int>(file, FDrsrLog)
#    safe_write<int>(file, FDbangLog)
#    safe_write<int>(file, FEmissionRXLog)
#
#    safe_write<int>(file, FEmissionRX)
#    safe_write<int>(file, FDZmax)
#    safe_write<int>(file, FDenr)
#    safe_write<int>(file, FDent)
#    safe_write<int>(file, FDrsr)
#    safe_write<int>(file, Flag_Energy_Density)
#    safe_write<int>(file, FDbang)
#
#    safe_write<int>(file, NbPointDZMax)
#    safe_write<int>(file, NbPointDENR)
#    safe_write<int>(file, NbPointDENT)
#    safe_write<int>(file, NbPointDRSR)
#    safe_write<int>(file, NbPointDEpos_X)
#    safe_write<int>(file, NbPointDEpos_Y)
#    safe_write<int>(file, NbPointDEpos_Z)
#    safe_write<int>(file, NbPointDBANG)
#
#    safe_write<int>(file, RangeFinder)
#
#    safe_write<double>(file, DEpos_Center.x)
#    safe_write<double>(file, DEpos_Center.y)
#    safe_write<double>(file, DEpos_Center.z)
#    safe_write<double>(file, DEpos_Size.x)
#    safe_write<double>(file, DEpos_Size.y)
#    safe_write<double>(file, DEpos_Size.z)
#
#    //---------------------------
#    // added : version 3010405
#    safe_write<int>(file, DEpos_Type)
#
#    safe_write<int>(file, DEposSpheric_Rad_Div)
#    safe_write<double>(file, DEposSpheric_Rad)
#    safe_write<int>(file, DEposSpheric_Rad_Log)
#
#    safe_write<int>(file, DEposCyl_Rad_Div)
#    safe_write<double>(file, DEposCyl_Rad)
#    safe_write<int>(file, DEposCyl_Rad_Log)
#    safe_write<int>(file, DEposCyl_Z_Div)
#    safe_write<double>(file, DEposCyl_Z)
#    safe_write<int>(file, DEposCyl_Z_Log)
#
#    //new version 30104072
#    safe_write<int>(file, DEpos_Position)
#    //---------------------------
#
#    Tags::AddTag(file, "*DIST_OPT_END", 15)

    def read(self, file):
        tag_id = b"*DIST_OPT_BEG"
        find_tag(file, tag_id)

        self.version = read_int(file)

        self.DenrMax = read_double(file)
        self.DenrMin = read_double(file)
        self.DentMax = read_double(file)
        self.DentMin = read_double(file)
        self.DrsrMax = read_double(file)
        self.DrsrMin = read_double(file)
        self.DZmaxMax = read_double(file)
        self.DZmaxMin = read_double(file)
        self.DbangMax = read_double(file)
        self.DbangMin = read_double(file)

        self.FDZmaxLog = read_int(file)
        self.FDenrLog = read_int(file)
        self.FDentLog = read_int(file)
        self.FDrsrLog = read_int(file)
        self.FDbangLog = read_int(file)
        self.FEmissionRXLog = read_int(file)

        self.FEmissionRX = read_int(file)
        self.FDZmax = read_int(file)
        self.FDenr = read_int(file)
        self.FDent = read_int(file)
        self.FDrsr = read_int(file)
        self.Flag_Energy_Density = read_int(file)
        self.FDbang = read_int(file)

        self.NbPointDZMax = read_int(file)
        self.NbPointDENR = read_int(file)
        self.NbPointDENT = read_int(file)
        self.NbPointDRSR = read_int(file)
        self.NbPointDEpos_X = read_int(file)
        self.NbPointDEpos_Y = read_int(file)
        self.NbPointDEpos_Z = read_int(file)
        self.NbPointDBANG = read_int(file)

        self.RangeFinder = read_int(file)

        self.DEpos_Center.x = read_double(file)
        self.DEpos_Center.y = read_double(file)
        self.DEpos_Center.z = read_double(file)
        self.DEpos_Size.x = read_double(file)
        self.DEpos_Size.y = read_double(file)
        self.DEpos_Size.z = read_double(file)

        self.DEpos_Type = read_int(file)

        self.DEposSpheric_Rad_Div = read_int(file)
        self.DEposSpheric_Rad = read_double(file)
        self.DEposSpheric_Rad_Log = read_int(file)

        self.DEposCyl_Rad_Div = read_int(file)
        self.DEposCyl_Rad = read_double(file)
        self.DEposCyl_Rad_Log = read_int(file)
        self.DEposCyl_Z_Div = read_int(file)
        self.DEposCyl_Z = read_double(file)
        self.DEposCyl_Z_Log = read_int(file)

        self.DEpos_Position = read_int(file)

        tag_id = b"*DIST_OPT_END"
        find_tag(file, tag_id)

    def reset(self):
        self.FDZmax = 1
        self.FDZmaxLog = 0
        self.NbPointDZMax = 1000
        self.DZmaxMax = autoFlag
        self.DZmaxMin = autoFlag

        self.FDenr = 1
        self.FDenrLog = 0
        self.NbPointDENR = 500
        self.DenrMax = autoFlag
        self.DenrMin = autoFlag

        self.FDent = 1
        self.FDentLog = 0
        self.NbPointDENT = 500
        self.DentMax = autoFlag
        self.DentMin = autoFlag

        self.FDrsr = 1
        self.FDrsrLog = 0
        self.NbPointDRSR = 500
        self.DrsrMax = autoFlag
        self.DrsrMin = autoFlag

        self.FDbang = 1
        self.FDbangLog = 0
        self.NbPointDBANG = 91
        self.DbangMax = autoFlag
        self.DbangMin = autoFlag

        self.FEmissionRX = 1
        self.FEmissionRXLog = 0
        self.NbreCoucheRX = 500

        self.RangeFinder = RANGE_SIMULATED

        self.Flag_Energy_Density = 1
        self.DEpos_Type = 0

        self.NbPointDEpos_X = 50
        self.NbPointDEpos_Y = 50
        self.NbPointDEpos_Z = 50

        self.DEpos_Center = Vector(0.0, 0.0, 0.0)
        self.DEpos_Size = Vector(1000.0, 1000.0, 1000.0)

        self.DEposSpheric_Rad_Div = 50
        self.DEposSpheric_Rad = 1000
        self.DEposSpheric_Rad_Log = 0

        self.DEposCyl_Rad_Div = 50
        self.DEposCyl_Rad = 1000
        self.DEposCyl_Rad_Log = 0
        self.DEposCyl_Z_Div = 50
        self.DEposCyl_Z = 1000
        self.DEposCyl_Z_Log = 0

        self.DEpos_Position = DIST_DEPOS_POSITION_ABSOLUTE

    def get_deposited_energy_center_nm(self):
        return self.DEpos_Center

    def get_deposited_energy_size_nm(self):
        return self.DEpos_Size
