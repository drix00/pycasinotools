#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_adv_back_set
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
"""

###############################################################################
# Copyright 2020 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_bool, read_double
from casinotools.file_format.tags import find_tag


# Globals and constants variables.
# Minimum angle for energy filter
#    double BEMin_Angle

# Maximum angle for Energy filter
#    double BEMax_Angle

# Maximum value of energy filter
#    double EFilterMax

# Minimum value of energy filter
#    double EFilterMin

# Middle values of energy filter
#    double EFilterVal[101]

# flag for doing filtration by energy(added to filter by position)
#    int FEFilter

# Setting of Backscattered electron detector
# Permit the setting of the sensibility of the backscattered electron detector

# Determine if using the advanced backscattered electron sensor settings :
# -true : Use them
# -false : Do not use them.
#    bool UseEnBack

# Backscattered electron sensor matrix setting
# TODO: implement the MatrixDetect variable and read data from file.
#    Matrix2d<double> MatrixDetect

# Working distance of the backscattered electron sensor.
#    double WorkDist

# Scale in X of one division of the sensor, in nm.
#    double DetectScaleX

# Scale in Y of one division of the sensor, in nm
#    double DetectScaleY

# Determine if the backscattered sensor matrix (MatrixDetect) is valid
#    bool ValidMatrix

# name of the matrix file (and the path).
#    std::string pathToMatrix


class OptionsAdvBackSet:
    def __init__(self):
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

        self.version = 0

        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file,"*MATRX_SET_BEG", 15)
#    OptionsGroup::writeVersion(file)
#
#    safe_write<bool>(file, UseEnBack)
#    safe_write<double>(file, WorkDist)
#    safe_write<double>(file, DetectScaleX)
#    safe_write<double>(file, DetectScaleY)
#    safe_write<bool>(file, ValidMatrix)
#
#    if(ValidMatrix == true)
#
#        for(int i = 0 i < 101 i++)
#
#            for(int j = 0 j < 101 j++)
#
#                safe_write<double>(file, MatrixDetect.get(i, j))
#
#
#
#
#    safe_write<double>(file, BEMin_Angle)
#    safe_write<double>(file, BEMax_Angle)
#    safe_write<double>(file, EFilterMax)
#    safe_write<double>(file, EFilterMin)
#
#    for(int i = 0 i < 101 i++)
#
#        safe_write<double>(file, EFilterVal[i])
#
#    safe_write<int>(file, FEFilter)
#
#    Tags::AddTag(file,"*MATRX_SET_END", 15)

    def read(self, file):
        tag_id = b"*MATRX_SET_BEG"
        find_tag(file, tag_id)

        self.version = read_int(file)

        self.UseEnBack = read_bool(file)
        self.WorkDist = read_double(file)
        self.DetectScaleX = read_double(file)
        self.DetectScaleY = read_double(file)
        self.ValidMatrix = read_bool(file)

        if self.ValidMatrix:
            raise NotImplementedError
#        for(int i = 0 i < 101 i++)
#            for(int j = 0 j < 101 j++)
#                double value
#                saferead<double>(file, value = read_double(file)
#                MatrixDetect.set(i, j, value)

        self.BEMin_Angle = read_double(file)
        self.BEMax_Angle = read_double(file)
        self.EFilterMax = read_double(file)
        self.EFilterMin = read_double(file)

        for i in range(101):
            self.EFilterVal[i] = read_double(file)

        self.FEFilter = read_int(file)

        tag_id = b"*MATRX_SET_END"
        find_tag(file, tag_id)

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
