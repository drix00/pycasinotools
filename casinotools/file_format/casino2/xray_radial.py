#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.xray_radial
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

# Globals and constants variables.
DISTANCE_nm = "Distance (nm)"
INTENSITY = "Intensity"
INTENSITY_ABSORBED = "Intensity Absorbed"


class XrayRadial(object):
    def __init__(self):
        self._line = None
        self._element_symbol = None
        self._labels = []
        self._data = {}

    def add_data(self, label, value):
        self._data.setdefault(label, []).append(value)

    def set_line(self, line):
        self._line = line

    def set_element_symbol(self, symbol):
        self._element_symbol = symbol

    def set_labels(self, labels):
        self._labels = labels

    def get_line(self):
        return self._line

    def get_element_symbol(self):
        return self._element_symbol

    def get_data_labels(self):
        return self._labels

    def get_distances_nm(self):
        return self._data[DISTANCE_nm]

    def get_intensities(self):
        return self._data[INTENSITY]

    def get_intensities_absorbed(self):
        return self._data[INTENSITY_ABSORBED]
