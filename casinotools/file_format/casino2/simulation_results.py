#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.simulation_results
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
import logging
import struct
import os

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, read_double_list, read_long, \
    read_double
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino2.element_intensity import ElementIntensity
from casinotools.file_format.casino2.graph_data import GraphData


# Globals and constants variables.


class SimulationResults:
    def __init__(self, is_skip_reading_data=False):
        self._is_skip_reading_data = is_skip_reading_data
        self.DENR = None
        self.DZMaxRetro = None

    def read(self, file, options, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = b"*DISTDATA%%%%%%"
        find_tag(file, tag_id)

        self._read_bse_intensity(file, options, version)

        tag_id = b"*REGULARDIST%%%"
        find_tag(file, tag_id)

        self._read_maximum_depth(file, options, version)

        self._read_backscattered_energy(file, options, version)

        self._read_backscattered_energy_t(file, options, version)

        self._read_surface_radius_bse(file, options, version)

        self._read_dncr(file, options)

        if version >= 22:
            self._read_deposited_energy(file, options)

        if version >= 25:
            self._read_backscattered_angle(file, options, version)

        if version >= 26:
            self._read_bse_angle_energie(file, options, version)

    def _read_bse_intensity(self, file, options, version):
        # Intensity distributions
        tag_id = b"*INTENSITYDIST%"
        find_tag(file, tag_id)
        self.BE_Intensity_Size = read_int(file)
        self.BE_Intensity = read_double_list(file, self.BE_Intensity_Size)
        if version >= 25 and options.UseEnBack:
            self.BE_Intensity_En = read_double_list(file, self.BE_Intensity_Size)
        self.eT = read_long(file)
        self.element_intensity_list = []
        for dummy in range(self.eT):
            element = ElementIntensity()
            element.read(file)
            self.element_intensity_list.append(element)

    def _read_maximum_depth(self, file, options, version):
        tag_id = b"*DZMAX%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDZmax:
            if version >= 2040601:
                flag = read_int(file)
                if flag == 1:
                    self.DZMax = GraphData(file=file)
                    self.DZMaxRetro = GraphData(file=file)
            else:
                number_points = read_long(file)
                self.NbPointDZMax = number_points
                if number_points > 0:
                    self.DZMax = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "z Max", "Depth (nm)",
                                           "Hits (Normalized)")
                    self.DZMaxRetro = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "z Max", "Depth (nm)",
                                                "Hits (Normalized)")
                    for dummy in range(number_points):
                        value = read_double(file)
                        self.DZMax.add(value)

                    for dummy in range(number_points):
                        value = read_double(file)
                        self.DZMaxRetro.add(value)

                else:
                    number_points *= -1

    def is_backscattered_maximum_depth_distribution(self):
        return self.DZMaxRetro is not None

    def get_backscattered_maximum_depth_distribution(self):
        return self.DZMaxRetro

    def get_backscattered_maximum_depth_range(self, fraction_limit=0.999):
        range_nm = _compute_depth_range(self.get_backscattered_maximum_depth_distribution(), fraction_limit)
        return range_nm

    def _read_backscattered_energy(self, file, options, version):
        tag_id = b"*DENR%%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDenr:
            values = None
            if version >= 2040601:
                flag = read_int(file)
                if flag == 1:
                    values = GraphData(file=file)
            else:
                number_points = read_long(file)
                self.NbPointDENR = number_points
                if number_points > 0:
                    values = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "Backscattered Energy", "Energy (KeV)",
                                       "Hits (Normalized)")
                    for dummy in range(number_points):
                        value = read_double(file)
                        values.add(value)

                else:
                    number_points *= -1
            self.DENR = values

    def is_backscattered_energy_distribution(self):
        return self.DENR is not None

    def get_backscattered_energy_distribution(self):
        return self.DENR

    def _read_backscattered_energy_t(self, file, options, version):
        tag_id = b"*DENT%%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDent:
            values = None
            if version >= 2040601:
                flag = read_int(file)
                if flag == 1:
                    values = GraphData(file=file)
            else:
                number_points = read_long(file)
                self.NbPointDENT = number_points
                if number_points > 0:
                    values = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "Backscattered Energy", "Energy (KeV)",
                                       "Hits (Normalized)")
                    for dummy in range(number_points):
                        value = read_double(file)
                        values.add(value)

                else:
                    number_points *= -1
            self.DENT = values

    def is_transmitted_energy_distribution(self):
        return self.DENT is not None

    def get_transmitted_energy_distribution(self):
        return self.DENT

    def _read_surface_radius_bse(self, file, options, version):
        tag_id = b"*DRSR%%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDrsr:
            if version >= 2040601:
                flag = read_int(file)
                if flag == 1:
                    self.DrasRetro = GraphData(file=file)
                    self.DrasRetroEnr = GraphData(file=file)
            else:
                number_points = read_long(file)
                self.NbPointDRSR = number_points
                if number_points > 0:
                    self.DrasRetro = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "Surface Radius of BE",
                                               "Radius (nm)", "Hits (Normalized) / nm")
                    self.DrasRetroEnr = GraphData(number_points, 0.0, options.RkoMax, 0, 0,
                                                  "Energy of Surface Radius of BE", "Radius (nm)", "KeV / nm")
                    for dummy in range(number_points):
                        value = read_double(file)
                        self.DrasRetro.add(value)

                    for dummy in range(number_points):
                        value = read_double(file)
                        self.DrasRetroEnr.add(value)

                else:
                    number_points *= -1

    def is_surface_radius_bse_distribution(self):
        return self.DrasRetro is not None

    def get_surface_radius_bse_distribution(self):
        return self.DrasRetro

    def _read_dncr(self, file, options):
        tag_id = b"*DNCR%%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDncr:
            number_points = read_long(file)
            values = []
            if number_points > 0:
                for dummy in range(number_points):
                    value = read_double(file)
                    values.append(value)

            else:
                number_points *= -1
            self.NbPointDNCR = number_points
            self.DNCR = values

    def _read_deposited_energy(self, file, options):
        tag_id = b"*DEPOS%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDEpos:
            self.NbPointDEpos_X = read_long(file)
            self.NbPointDEpos_Y = read_long(file)
            self.NbPointDEpos_Z = read_long(file)
            self.DEpos_maxE = read_double(file)
            if self.NbPointDEpos_X > 0:
                values = []
                number_points = self.NbPointDEpos_X * self.NbPointDEpos_Y * self.NbPointDEpos_Z

                if not self._is_skip_reading_data:
                    values = read_double_list(file, number_points)
                #                    for dummy in range(number_points):
                #                        value = read_double(file)
                #                        values.append(value)
                else:
                    offset = struct.calcsize("d") * number_points
                    file.seek(offset, os.SEEK_CUR)

                self.DEpos = values
            else:
                self.NbPointDEpos_X *= -1
                self.NbPointDEpos_Y *= -1
                self.NbPointDEpos_Z *= -1

    def get_number_points_energy_absorbed(self):
        return self.NbPointDEpos_X * self.NbPointDEpos_Y * self.NbPointDEpos_Z

    def get_number_points_energy_absorbed_x(self):
        return self.NbPointDEpos_X

    def get_number_points_energy_absorbed_y(self):
        return self.NbPointDEpos_Y

    def get_number_points_energy_absorbed_z(self):
        return self.NbPointDEpos_Z

    def get_maximum_energy_absorbed_keV(self):
        return self.DEpos_maxE

    def get_energy_absorbed_keV(self):
        return self.DEpos

    def _read_backscattered_angle(self, file, options, version):
        tag_id = b"*DBANG%%%%%%%%%"
        find_tag(file, tag_id)
        if options.FDbang:
            if version >= 2040601:
                flag = read_int(file)
                if flag == 1:
                    self.Dbang = GraphData(file=file)
                    if options.UseEnBack:
                        flag = read_int(file)
                        if flag == 1:
                            self.DEnBang = GraphData(file=file)
            else:
                number_points = read_long(file)
                if number_points > 0:
                    self.Dbang = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "Backscattered Angle",
                                           "Angle (degree)", "Hits (Normalized)")
                    for dummy in range(number_points):
                        value = read_double(file)
                        self.Dbang.add(value)

                    if options.UseEnBack:
                        self.DEnBang = GraphData(number_points, 0.0, options.RkoMax, 0, 0,
                                                 "Detected Backscattered Angle", "Angle (degree)", "Hits (Normalized)")
                        for dummy in range(number_points):
                            value = read_double(file)
                            self.DEnBang.add(value)

                else:
                    number_points *= -1
                self.NbPointDBANG = number_points

    def is_backscattered_angle_distribution(self):
        return self.Dbang is not None

    def get_backscattered_angle_distribution(self):
        return self.Dbang

    def _read_bse_angle_energie(self, file, options, version):
        tag_id = b"*DANGLEENERGY%%"
        find_tag(file, tag_id)
        if options.FDAngleVSEnergie:
            if version >= 2040601:
                flag = read_int(file)
                if flag == 1:
                    self.DAngleVSEnergie = GraphData(file=file)
                    if options.UseEnBack:
                        flag = read_int(file)
                        if flag == 1:
                            self.DEnAngleVSEnergie = GraphData(file=file)
            else:
                number_points = read_long(file)
                if number_points > 0:
                    self.DAngleVSEnergie = GraphData(number_points, 0.0, options.RkoMax, 0, 0, "Backscattered Angle",
                                                     "Angle (degree)", "Hits (Normalized)")
                    for dummy in range(number_points):
                        value = read_double(file)
                        self.DAngleVSEnergie.add(value)

                    if options.UseEnBack:
                        self.DEnAngleVSEnergie = GraphData(number_points, 0.0, options.RkoMax, 0, 0,
                                                           "Detected Backscattered Angle", "Angle (degree)",
                                                           "Hits (Normalized)")
                        for dummy in range(number_points):
                            value = read_double(file)
                            self.DEnAngleVSEnergie.add(value)

                else:
                    number_points *= -1
                self.NbPointDAngleVSEnergie = number_points


def _compute_depth_range(distribution, fraction_limit):
    positions = distribution.get_positions()
    values = distribution.get_values()

    total = sum(values)

    partial_total = 0.0
    fraction = 0.0
    for position, value in zip(positions, values):
        partial_total += value
        fraction = partial_total / total
        if fraction >= fraction_limit:
            return position

    depth = positions[-1]
    message = "Depth range not found, fraction smaller (%.f) than fraction limit (%.f), " \
              "return last depth (%.f)" % (fraction, fraction_limit, depth)
    logging.warning(message)
    return depth
