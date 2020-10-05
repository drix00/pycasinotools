#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_object
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_str, read_double_list, \
    write_int, write_str, write_double_list
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino3.sample_shape.shape_type import get_string

# Globals and constants variables.


class SampleObject:
    def __init__(self, shape_type):
        self._file = None
        self._start_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._version = None
        self._name = "Empty"
        self._region_name = "Undefined"

        self.translation = []
        self.rotation = []
        self.scale = [1.0, 1.0, 1.0]
        self.color = [0.0, 0.0, 1.0]

        self.shape_type = shape_type

    def read(self, file):
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        tag_id = b"%SMPLOBJ"
        if find_tag(file, tag_id):
            self._version = read_int(file)

            self._name = read_str(file)
            self._region_name = read_str(file)

            self.translation = read_double_list(file, 3)
            self.rotation = read_double_list(file, 3)
            self.scale = read_double_list(file, 3)
            self.color = read_double_list(file, 3)

    def get_name(self):
        return self._name

    def get_type(self):
        return self.shape_type

    def get_version(self):
        return self._version

    def get_translation_nm(self):
        return self.translation

    def get_scale_nm(self):
        return self.scale

    def export(self, export_file):
        self._export_version(export_file)
        self._export_type(export_file)
        self._export_name(export_file)
        self._export_region_name(export_file)
        self._export_translation(export_file)
        self._export_rotation(export_file)
        self._export_scale(export_file)
        self._export_color(export_file)

    def _export_version(self, export_file):
        version = self.get_version()
        version_string = _extract_version_string(version)
        line = "Sample object version: %s (%i)" % (version_string, version)
        write_line(export_file, line)

    def _export_type(self, export_file):
        type_str = get_string(self.shape_type)
        line = "Type: {}}".format(type_str)
        write_line(export_file, line)

    def _export_name(self, export_file):
        line = "name: {}}".format(self._name)
        write_line(export_file, line)

    def _export_region_name(self, export_file):
        line = "Region name: {}".format(self._region_name)
        write_line(export_file, line)

    def _export_translation(self, export_file):
        line = "Translation:"
        write_line(export_file, line)

        for label, value in zip(["X", 'Y', 'z'], self.translation):
            line = "\t%s: %g" % (label, value)
            write_line(export_file, line)

    def _export_rotation(self, export_file):
        line = "Rotation:"
        write_line(export_file, line)

        for label, value in zip(["X", 'Y', 'z'], self.rotation):
            line = "\t%s: %g" % (label, value)
            write_line(export_file, line)

    def _export_scale(self, export_file):
        line = "Scale:"
        write_line(export_file, line)

        for label, value in zip(["X", 'Y', 'z'], self.scale):
            line = "\t%s: %g" % (label, value)
            write_line(export_file, line)

    def _export_color(self, export_file):
        line = "Color:"
        write_line(export_file, line)

        for label, value in zip(["R", 'G', 'B'], self.color):
            line = "\t%s: %g" % (label, value)
            write_line(export_file, line)

    def modify_position_z(self, new_position_z_nm):
        if not self._file.closed:
            current_position = self._file.tell()
            self._file.close()
        else:
            current_position = 0

        self._file = open(self._file_pathname, 'r+b')

        self._file.seek(self._start_position)
        self.translation = (self.translation[0], self.translation[1], new_position_z_nm)

        self._modify(self._file)

        self._file.close()
        self._file = open(self._file_pathname, 'rb')
        self._file.seek(current_position)

    def _modify(self, file):
        assert file.mode == 'r+b'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write", file.tell())

        tag_id = "%SMPLOBJ"
        if find_tag(file, tag_id):
            write_int(file, self._version)

            write_str(file, self._name)
            write_str(file, self._region_name)

            write_double_list(file, self.translation, 3)
            write_double_list(file, self.rotation, 3)
            write_double_list(file, self.scale, 3)
            write_double_list(file, self.color, 3)
