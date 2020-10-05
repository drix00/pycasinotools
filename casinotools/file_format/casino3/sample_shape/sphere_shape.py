#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_shape.sphere_shape
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
from casinotools.file_format.casino3.sample_object import SampleObject
from casinotools.file_format.casino3.sample_shape.shape_type import SHAPE_SPHERE
from casinotools.file_format.file_reader_writer_tools import read_double, read_int

# Globals and constants variables.


class SphereShape(SampleObject):
    def __init__(self, shape_type):
        super(SphereShape, self).__init__(shape_type)
        self._type = SHAPE_SPHERE

        self._radius_nm = 5.0
        self._division_phi = 4
        self._division_theta = 4
        self._color = [0.0, 1.0, 0.0]

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        super(SphereShape, self).read(file)

        self._radius_nm = read_double(file)
        self._division_phi = read_int(file)
        self._division_theta = read_int(file)

    def set_radius_nm(self, radius_nm):
        self._radius_nm = radius_nm

    def set_division(self, division):
        self._division_phi = division
        self._division_theta = division
