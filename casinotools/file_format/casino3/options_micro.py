#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_micro
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
"""

########################################
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
########################################

# Standard library modules.

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.
# Filename to store the defaults settings
OPTIONS_MICRO_DEF_FILENAME = "Microscope_Settings_Defaults.dat"

# const for the beam_distribution option :
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

# Microscope settings
# Angle du faisceau d'electrons du microscope. Definition du microscope
#    double beam_angle

# Nombre d'electrons par point de simulation du microscope. Definition du microscope
#    int trajectories_number

# Puissance du faisceau en KeV a la derniere simulation.
# Permet de refaire les scan points de la simulation avec plusieurs energies differentes
#    double KEV_End

# Puissance du faisceau en KeV a la premiere simulation.
# Permet de refaire les scan points de la simulation avec plusieurs energies differentes
#    double KEV_Start

# Increment de puissance entre 2 simulations.
# Permet de refaire les scan points de la simulation avec plusieurs energies differentes
#    double KEV_Step

# Flag indicating if we use multiple scan points.
# 0 = No, positive = Yes.
#    int multiple_scan_energy

# Determine if we keep the simulation datas necessary to view the distributions.
#    int keep_simulation_data

# Microscope settings - Beam Settings
# Beam radius.
#    double beam_radius

# Beam Aperture Angle in Rad.
#    double beam_aperture_width

# z_plane_position position of the focal point when mode is XY scanning
# y_plane_position position of the Y plane when mode is XZ scanning
# x_plane_position position of the X plane when mode is YZ scanning

#    double z_plane_position
#    double y_plane_position
#    double x_plane_position

# scanning mode : can be MODE_XY_SCAN, MODE_XZ_SCAN, MODE_YZ_SCAN
#    int scanning_mode

# Beam Distribution Variance Used in the Gaussian Distribution
#    double beam_dist_variance

# Beam Distribution Type
# See related const BEAM_DIST_ above
#    int beam_distribution

# Avanced beam options flag
#    int beam_adv_set

# Cone Beam Algorithm used in cone beam calculation
#    int beam_cone_algo

# Electron beam diameter
#    int BeamDiam

# Noise settings for electrons trajectories numbers
#    int noise_type
#    int noise_enabled
#    double noise_percentage

# Flag determining if we simulate secondary electrons.
# Activated by the user in the settings dialogs.
#    int generate_secondary

# Flag determining if we generate X-Rays -- Not Used Right Now --.
# Activated by the user in the settings dialogs. Should be used when
# X-Rays will be reimplemented correctly.
#    int generate_x_rays

# keep in memory the distance between scan point for the microscope settings dialog
#    float scan_point_distribution


class OptionsMicro(FileReaderWriterTools):
    def __init__(self):
        self.beam_angle = 0.0
        self.trajectories_number = 1000
        self.KEV_End = 0.0
        self.KEV_Start = 1.0
        self.KEV_Step = 1.0
        self.multiple_scan_energy = 0

        self.beam_radius = 5.0
        self.beam_adv_set = 0
        self.beam_dist_variance = BEAM_VARIANCE_DEFAULT

        self.z_plane_position = Z_PLANE_POSITION_DEFAULT
        self.y_plane_position = Y_PLANE_POSITION_DEFAULT
        self.x_plane_position = X_PLANE_POSITION_DEFAULT
        self.scanning_mode = SCANNING_MODE_DEFAULT

        self.beam_aperture_width = BEAM_APERTURE_WIDTH_DEFAULT
        self.beam_distribution = BEAM_DISTRIBUTION_DEFAULT
        self.beam_cone_algo = BEAM_CONEALGO_DEFAULT

        self.generate_secondary = 0
        self.generate_x_rays = 0
        self.keep_simulation_data = 0
        self.scan_point_distribution = 1

        # Noise Settings
        self.noise_type = NOISE_TYPE_DEFAULT
        self.noise_enabled = False
        self.noise_percentage = NOISE_PERCENTAGE_DEFAULT

        self._version = 0

        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file, "*MICRO_SET_BEG", 15)
#        writeVersion(file)
#
#    //--New version 3.1.4.6
#    safe_write<int>(file, scanning_mode)
#    safe_write<double>(file, x_plane_position)
#    safe_write<double>(file, y_plane_position)
#    //--
#
#    safe_write<int>(file, noise_type)
#    safe_write<int>(file, noise_enabled)
#    safe_write<double>(file, noise_percentage)
#
#    safe_write<double>(file, beam_angle)
#    safe_write<double>(file, beam_radius)
#    safe_write<double>(file, beam_aperture_width)
#    safe_write<double>(file, z_plane_position)
#    safe_write<double>(file, beam_dist_variance)
#    safe_write<int>(file, beam_distribution)
#    safe_write<int>(file, beam_adv_set)
#
#    safe_write<int>(file, trajectories_number)
#    safe_write<double>(file, KEV_End)
#    safe_write<double>(file, KEV_Start)
#    safe_write<double>(file, KEV_Step)
#    safe_write<int>(file, multiple_scan_energy)
#    safe_write<int>(file, generate_secondary)
#    safe_write<int>(file, generate_x_rays)
#    safe_write<float>(file, scan_point_distribution)
#    safe_write<int>(file, keep_simulation_data)
#
#    Tags::AddTag(file, "*MICRO_SET_END", 15)

    def read(self, file):
        tag_id = b"*MICRO_SET_BEG"
        self.find_tag(file, tag_id)

        self._version = self.read_int(file)

        self.scanning_mode = self.read_int(file)
        self.x_plane_position = self.read_double(file)
        self.y_plane_position = self.read_double(file)

        self.noise_type = self.read_int(file)
        self.noise_enabled = self.read_int(file)
        self.noise_percentage = self.read_double(file)

        self.beam_angle = self.read_double(file)
        self.beam_radius = self.read_double(file)
        self.beam_aperture_width = self.read_double(file)
        self.z_plane_position = self.read_double(file)
        self.beam_dist_variance = self.read_double(file)
        self.beam_distribution = self.read_int(file)
        self.beam_adv_set = self.read_int(file)

        self.trajectories_number = self.read_int(file)
        self.KEV_End = self.read_double(file)
        self.KEV_Start = self.read_double(file)
        self.KEV_Step = self.read_double(file)
        self.multiple_scan_energy = self.read_int(file)
        self.generate_secondary = self.read_int(file)
        self.generate_x_rays = self.read_int(file)
        self.scan_point_distribution = self.read_float(file)
        self.keep_simulation_data = self.read_int(file)

        tag_id = b"*MICRO_SET_END"
        self.find_tag(file, tag_id)

    def reset(self):
        self.beam_angle = 0.0
        self.trajectories_number = 1000
        self.KEV_End = 0.0
        self.KEV_Start = 1.0
        self.KEV_Step = 1.0
        self.multiple_scan_energy = 0

        self.beam_radius = 5.0
        self.beam_adv_set = 0
        self.beam_dist_variance = BEAM_VARIANCE_DEFAULT

        self.z_plane_position = Z_PLANE_POSITION_DEFAULT
        self.y_plane_position = Y_PLANE_POSITION_DEFAULT
        self.x_plane_position = X_PLANE_POSITION_DEFAULT
        self.scanning_mode = SCANNING_MODE_DEFAULT

        self.beam_aperture_width = BEAM_APERTURE_WIDTH_DEFAULT
        self.beam_distribution = BEAM_DISTRIBUTION_DEFAULT
        self.beam_cone_algo = BEAM_CONEALGO_DEFAULT

        self.generate_secondary = 0
        self.generate_x_rays = 0
        self.keep_simulation_data = 0
        self.scan_point_distribution = 1

        # Noise Settings
        self.noise_type = NOISE_TYPE_DEFAULT
        self.noise_enabled = False
        self.noise_percentage = NOISE_PERCENTAGE_DEFAULT
