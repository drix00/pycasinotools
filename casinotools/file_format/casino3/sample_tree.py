#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_tree
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
from casinotools.file_format.file_reader_writer_tools import read_double, read_int, read_double_list, write_line
from casinotools.file_format.casino3.triangle import Triangle

# Globals and constants variables.


class SampleTree:
    def __init__(self):
        self._file = None
        self._start_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._max_size = 0.0
        self._max_level = 0
        self._maximum = []
        self._minimum = []

        self._number_triangles = 0
        self._triangles = []

    def read(self, file):
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        self._max_size = read_double(file)
        self._max_level = read_int(file)
        self._maximum = read_double_list(file, 3)
        self._minimum = read_double_list(file, 3)

        self._number_triangles = read_int(file)
        self._triangles = []
        for dummy in range(self._number_triangles):
            triangle = Triangle()
            triangle.read(file)
            self._triangles.append(triangle)

    def export(self, export_file):
        line = "Maximum size: {:f}".format(self._max_size)
        write_line(export_file, line)

        line = "Maximum level: {:d}".format(self._max_level)
        write_line(export_file, line)

        line = "Maximum:"
        write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'z'], self._maximum):
            line = "\t%s: %g" % (label, value)
            write_line(export_file, line)

        line = "Minimum:"
        write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'z'], self._minimum):
            line = "\t%s: %g" % (label, value)
            write_line(export_file, line)

        line = "Number triangles: {:d}".format(self._number_triangles)
        write_line(export_file, line)

        triangle_id = 0
        for triangle in self._triangles:
            triangle_id += 1

            line = "*"*15
            write_line(export_file, line)

            line = "Triangle: {:d}".format(triangle_id)
            write_line(export_file, line)

            triangle.export(export_file)
