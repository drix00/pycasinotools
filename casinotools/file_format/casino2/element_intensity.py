#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.element_intensity
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


class ElementIntensity(FileReaderWriterTools):
    def __init__(self):
        self.name = ""
        self.Size = 0

        self.IntensityK = []
        self.IntensityL = []
        self.IntensityM = []

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self.name = self.read_str_length(file, 3)

        self.Size = self.read_long(file)

        if self.Size != 0:
            self.IntensityK = self.read_double_list(file, self.Size)
            self.IntensityL = self.read_double_list(file, self.Size)
            self.IntensityM = self.read_double_list(file, self.Size)
