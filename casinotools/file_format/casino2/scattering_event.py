#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.scattering_event
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
import struct

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.


class ScatteringEvent(FileReaderWriterTools):
    def __init__(self):
        self.X = 0.0
        self.Y = 0.0
        self.z = 0.0
        self.E = 0.0
        self.Intersect = 0
        self.id = 0

    @staticmethod
    def get_skip_offset():
        value_format = "4f2i"
        return struct.calcsize(value_format)

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self.X = self.read_float(file)
        self.Y = self.read_float(file)
        self.z = self.read_float(file)
        self.E = self.read_float(file)
        self.Intersect = self.read_int(file)
        self.id = self.read_int(file)
