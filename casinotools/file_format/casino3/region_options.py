#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.region_options
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools
from casinotools.file_format.casino3.region import Region

# Globals and constants variables.
TAG_REGION_DATA = b"*REGIONDATA%%%%"


class RegionOptions(FileReaderWriterTools):
    def __init__(self):
        self._numberRegions = 0
        self._regions = []

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = TAG_REGION_DATA
        self.find_tag(file, tag_id)

        self._numberRegions = self.read_int(file)

        for dummy in range(self._numberRegions):
            region = Region()
            region.read(file)
            self._regions.append(region)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_REGION_DATA
        self.add_tag(file, tag_id)

        self.write_int(file, self._numberRegions)

        assert len(self._regions) == self._numberRegions
        for index in range(self._numberRegions):
            region = self._regions[index]
            region.write(file)

    def get_region(self, index):
        return self._regions[index]
