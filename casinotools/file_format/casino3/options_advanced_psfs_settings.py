#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_advanced_psfs_settings
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_bool, read_double
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino3.version import SIM_OPTIONS_VERSION_3_3_0_0
from casinotools.file_format.casino3.vector import Vector

# Globals and constants variables.


class OptionsAdvancedPsfsSettings:
    def __init__(self):
        self._generatePsf = True
        self._useScanPointForCenter = True

        self._autoExportPsfData = True
        self._exportTiff = True
        self._exportCsv = True
        self._exportStackedTiff = True

        self._psfSize_nm = Vector(128.0 * 1.0, 128.0 * 1.0, 128.0 * 5.0)
        self._psfNumberSteps = Vector(128, 128, 128)
        self._psfCenter_nm = Vector(0.0, 0.0, 500.0)

        self.version = 0

        self.reset()

    def write(self, output_file):
        pass

    def read(self, input_file):
        assert input_file.mode == 'rb'

        tag_id = b"*PSF_SET_BEG"
        find_tag(input_file, tag_id)

        self.version = read_int(input_file)
        assert self.version >= SIM_OPTIONS_VERSION_3_3_0_0

        self._generatePsf = read_bool(input_file)
        self._useScanPointForCenter = read_bool(input_file)

        self._autoExportPsfData = read_bool(input_file)
        self._exportTiff = read_bool(input_file)
        self._exportCsv = read_bool(input_file)
        self._exportStackedTiff = read_bool(input_file)

        self._psfSize_nm.x = read_double(input_file)
        self._psfSize_nm.y = read_double(input_file)
        self._psfSize_nm.z = read_double(input_file)

        self._psfNumberSteps.x = read_int(input_file)
        self._psfNumberSteps.y = read_int(input_file)
        self._psfNumberSteps.z = read_int(input_file)

        self._psfCenter_nm.x = read_double(input_file)
        self._psfCenter_nm.y = read_double(input_file)
        self._psfCenter_nm.z = read_double(input_file)

        tag_id = b"*PSF_SET_END"
        find_tag(input_file, tag_id)

    def reset(self):
        self._generatePsf = True
        self._useScanPointForCenter = True

        self._autoExportPsfData = True
        self._exportTiff = True
        self._exportCsv = True
        self._exportStackedTiff = True

        self._psfSize_nm = Vector(128.0 * 1.0, 128.0 * 1.0, 128.0 * 5.0)
        self._psfNumberSteps = Vector(128, 128, 128)
        self._psfCenter_nm = Vector(0.0, 0.0, 500.0)

    def is_generating_psfs(self):
        return self._generatePsf

    def get_use_scan_point_for_center(self):
        return self._useScanPointForCenter

    def get_psf_center_nm(self):
        return self._psfCenter_nm

    def get_number_steps_x(self):
        return self._psfNumberSteps.x

    def get_number_steps_y(self):
        return self._psfNumberSteps.y

    def get_number_steps_z(self):
        return self._psfNumberSteps.z
