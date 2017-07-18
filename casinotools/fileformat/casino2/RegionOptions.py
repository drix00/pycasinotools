#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.RegionOptions

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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.Region as Region

# Globals and constants variables.
TAG_REGION_DATA = b"*REGIONDATA%%%%"


class RegionOptions(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, number_xray_layers):
        self._numberXRayLayers = number_xray_layers

        self._numberRegions = None

        self._regions = []

    def read(self, file, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = TAG_REGION_DATA
        self.findTag(file, tagID)

        self._numberRegions = self.readInt(file)

        for dummy in range(self._numberRegions):
            region = Region.Region(self._numberXRayLayers)
            region.read(file, version)
            self._regions.append(region)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_REGION_DATA
        self.addTagOld(file, tag_id)

        self.writeInt(file, self._numberRegions)

        assert len(self._regions) == self._numberRegions
        for index in range(self._numberRegions):
            region = self._regions[index]
            region.write(file)

    def getRegion(self, index):
        return self._regions[index]

    def getNumberRegions(self):
        return len(self._regions)

    def getRegions(self):
        return self._regions

    def setElement(self, element_symbol, index_region=0):
        self._regions[index_region].setElement(element_symbol, number_xray_layers=self._numberXRayLayers)

    def setFilmThickness(self, thickness_nm):
        assert len(self._regions) == 2

        parameters = self._regions[0].getParameters()
        parameters[1] = thickness_nm
        self._regions[0].setParameters(parameters)

        parameters = self._regions[1].getParameters()
        parameters[2] = parameters[1]
        parameters[1] = 1.0e10
        parameters[0] = thickness_nm
        self._regions[1].setParameters(parameters)

    def setFilmThicknessInSubstrate(self, layer_top_position_z_nm, thickness_nm):
        assert len(self._regions) == 3

        parameters = self._regions[0].getParameters()
        parameters[1] = layer_top_position_z_nm
        self._regions[0].setParameters(parameters)

        parameters = self._regions[1].getParameters()
        # parameters[2] = parameters[1]
        parameters[1] = layer_top_position_z_nm + thickness_nm
        parameters[0] = layer_top_position_z_nm
        self._regions[1].setParameters(parameters)

        parameters = self._regions[2].getParameters()
        parameters[0] = layer_top_position_z_nm + thickness_nm
        self._regions[2].setParameters(parameters)

    def setThinFilmThickness(self, thickness_nm):
        assert len(self._regions) == 1

        parameters = self._regions[0].getParameters()
        parameters[1] = thickness_nm
        self._regions[0].setParameters(parameters)
