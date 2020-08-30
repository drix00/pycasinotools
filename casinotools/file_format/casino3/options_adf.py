#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_adf
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
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.
# Filename to store the defaults settings
OPTIONS_ADF_DEF_FILENAME = "ADF_Settings_Defaults.dat"


class OptionsADF(FileReaderWriterTools):
    def __init__(self):
        # max semi-angle of the detector
        self.MinAngle = 0.200
        self.MaxAngle = 0.5
        self.Enabled = 1
        self.keepData = 0
        self.MaxPoints = 0
        # quantum efficiency of the detector
        self.DQE = 1

        self._version = 0

        self.reset()

    def write(self, file):
        pass
#    Tags::AddTag(file, "*ADF_SET_BEG", 15)
#    writeVersion(file)
#
#    safe_write<double>(file, DQE)
#    safe_write<int>(file, Enabled)
#    safe_write<int>(file, keepData)
#    safe_write<double>(file, MaxAngle)
#    safe_write<double>(file, MinAngle)
#    safe_write<int>(file, MaxPoints)
#
#    Tags::AddTag(file, "*ADF_SET_END", 15)}

    def read(self, file):
        tag_id = b"*ADF_SET_BEG"
        self.find_tag(file, tag_id)

        self._version = self.read_int(file)

        self.DQE = self.read_double(file)

        self.Enabled = self.read_int(file)
        self.keepData = self.read_int(file)
        self.MaxAngle = self.read_double(file)
        self.MinAngle = self.read_double(file)
        self.MaxPoints = self.read_int(file)

        tag_id = b"*ADF_SET_END"
        self.find_tag(file, tag_id)

    def reset(self):
        # max semi-angle of the detector
        self.MinAngle = 0.200
        self.MaxAngle = 0.5
        self.Enabled = 1
        self.keepData = 0
        self.MaxPoints = 0
        # quantum efficiency of the detector
        self.DQE = 1
