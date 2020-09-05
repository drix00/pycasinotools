#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.region_options

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

RegionOptions data from CASINO v2.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, write_int
from casinotools.file_format.tags import add_tag_old, find_tag
from casinotools.file_format.casino2.region import Region

# Globals and constants variables.
TAG_REGION_DATA = b"*REGIONDATA%%%%"


class RegionOptions:
    def __init__(self, number_xray_layers):
        self._numberXRayLayers = number_xray_layers

        self._numberRegions = None

        self._regions = []

    def read(self, file, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = TAG_REGION_DATA
        find_tag(file, tag_id)

        self._numberRegions = read_int(file)

        for dummy in range(self._numberRegions):
            region = Region(self._numberXRayLayers)
            region.read(file, version)
            self._regions.append(region)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_REGION_DATA
        add_tag_old(file, tag_id)

        write_int(file, self._numberRegions)

        assert len(self._regions) == self._numberRegions
        for index in range(self._numberRegions):
            region = self._regions[index]
            region.write(file)

    def get_region(self, index):
        return self._regions[index]

    def get_number_regions(self):
        return len(self._regions)

    def get_regions(self):
        return self._regions

    def set_element(self, element_symbol, index_region=0):
        self._regions[index_region].set_element(element_symbol, number_xray_layers=self._numberXRayLayers)

    def set_film_thickness(self, thickness_nm):
        assert len(self._regions) == 2

        parameters = self._regions[0].get_parameters()
        parameters[1] = thickness_nm
        self._regions[0].set_parameters(parameters)

        parameters = self._regions[1].get_parameters()
        parameters[2] = parameters[1]
        parameters[1] = 1.0e10
        parameters[0] = thickness_nm
        self._regions[1].set_parameters(parameters)

    def set_film_thickness_in_substrate(self, layer_top_position_z_nm, thickness_nm):
        assert len(self._regions) == 3

        parameters = self._regions[0].get_parameters()
        parameters[1] = layer_top_position_z_nm
        self._regions[0].set_parameters(parameters)

        parameters = self._regions[1].get_parameters()
        # parameters[2] = parameters[1]
        parameters[1] = layer_top_position_z_nm + thickness_nm
        parameters[0] = layer_top_position_z_nm
        self._regions[1].set_parameters(parameters)

        parameters = self._regions[2].get_parameters()
        parameters[0] = layer_top_position_z_nm + thickness_nm
        self._regions[2].set_parameters(parameters)

    def set_thin_film_thickness(self, thickness_nm):
        assert len(self._regions) == 1

        parameters = self._regions[0].get_parameters()
        parameters[1] = thickness_nm
        self._regions[0].set_parameters(parameters)
