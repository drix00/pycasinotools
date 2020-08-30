#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.region_intensity_info
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


class RegionIntensityInfo(FileReaderWriterTools):
    def __init__(self):
        self._version = 0
        self._energy_intensity = 0.0
        self._region_id = 0
        self._normalized_energy_intensity = 0.0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self._version = self.read_int(file)
        self._energy_intensity = self.read_double(file)
        self._region_id = self.read_int(file)
        self._normalized_energy_intensity = self.read_double(file)

    def get_energy_intensity(self):
        return self._energy_intensity

    def get_normalized_energy_intensity(self):
        return self._normalized_energy_intensity
