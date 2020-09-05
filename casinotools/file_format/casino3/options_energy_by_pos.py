#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_energy_by_pos
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_double
from casinotools.file_format.tags import find_tag

# Globals and constants variables.
# Filename to store the defaults settings
OPTIONS_DEPOS_DEF_FILENAME = "EnergyByPosition_Settings_Defaults.dat"

# const definition for the energy display mode (XZ, XY or PROJECTION)
ENERGY_DISPLAY_XZ = 0
ENERGY_DISPLAY_XY = 1
ENERGY_DISPLAY_PROJECTION = 2

DEPOS_DIFFUSION_MINIMUM_ENERGY_DEFAULT = 1e-14


# Sum the current distribution in DEpos distribution.
#    int depos_summation

# Flag telling the application to apply diffusion to the EnergyMatrix
#    int diffuse

# Surface recombination value (used in diffuse calculation)
#    double carrier_surface_recombination

# Energy display mode : see const definition above
#    int x_zor_xy

# Plane to draw when Summation==0    in DEpos
#    int y_plane

# Plane to draw when Summation==0    in DEpos
#    int z_plane

# Percentage of energy to display
#    double depos_iso_level

# normalize or not the energy with the volume of the indexes
#    int normalize
class OptionsEnergyByPos:
    def __init__(self):
        self.diffuse = 0
        self.depos_summation = 1
        self.x_zor_xy = ENERGY_DISPLAY_XZ
        self.y_plane = 0
        self.z_plane = 0
        self.depos_iso_level = 0.1
        self.carrier_surface_recombination = -1
        self.normalize = 1

        self._version = 0

        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file,"*EN_POS_SET_BEG", 15)
#    writeVersion(file)
#
#    safe_write<int>(file, diffuse)
#    safe_write<int>(file, depos_summation)
#    safe_write<int>(file, x_zor_xy)
#    safe_write<int>(file, y_plane)
#    safe_write<int>(file, z_plane)
#    safe_write<double>(file, depos_iso_level)
#    safe_write<double>(file, carrier_surface_recombination)
#    safe_write<int>(file, normalize)
#    double minimumDiffusionEnergy //obsolete
#    safe_write<double>(file, minimumDiffusionEnergy)
#
#    Tags::AddTag(file, "*EN_POS_SET_END", 15)

    def read(self, file):
        tag_id = b"*EN_POS_SET_BEG"
        find_tag(file, tag_id)

        self._version = read_int(file)

        self.diffuse = read_int(file)

        self.depos_summation = read_int(file)
        self.x_zor_xy = read_int(file)
        self.y_plane = read_int(file)
        self.z_plane = read_int(file)
        self.depos_iso_level = read_double(file)

        self.carrier_surface_recombination = read_double(file)

        self.normalize = read_int(file)

        # obsolete minimumDiffusionEnergy =
        read_double(file)

        tag_id = b"*EN_POS_SET_END"
        find_tag(file, tag_id)

    def reset(self):
        self.diffuse = 0
        self.depos_summation = 1
        self.x_zor_xy = ENERGY_DISPLAY_XZ
        self.y_plane = 0
        self.z_plane = 0
        self.depos_iso_level = 0.1
        self.carrier_surface_recombination = -1
        self.normalize = 1
