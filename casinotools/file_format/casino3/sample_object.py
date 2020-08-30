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
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools
from casinotools.file_format.casino3.sample_shape.shape_type import get_string

# Globals and constants variables.


class SampleObject(FileReaderWriterTools):
    def __init__(self, shape_type):
        self._file = None
        self._start_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._version = None
        self._name = "Empty"
        self._region_name = "Undefined"

        self._translation = []
        self._rotation = []
        self._scale = [1.0, 1.0, 1.0]
        self._color = [0.0, 0.0, 1.0]

        self._shape_type = shape_type

    def read(self, file):
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        tag_id = b"%SMPLOBJ"
        if self.find_tag(file, tag_id):
            self._version = self.read_int(file)

            self._name = self.read_str(file)
            self._region_name = self.read_str(file)

            self._translation = self.read_double_list(file, 3)
            self._rotation = self.read_double_list(file, 3)
            self._scale = self.read_double_list(file, 3)
            self._color = self.read_double_list(file, 3)

    def get_name(self):
        return self._name

    def get_type(self):
        return self._shape_type

    def get_version(self):
        return self._version

    def get_translation_nm(self):
        return self._translation

    def get_scale_nm(self):
        return self._scale

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
        version_string = self._extract_version_string(version)
        line = "Sample object version: %s (%i)" % (version_string, version)
        self.write_line(export_file, line)

    def _export_type(self, export_file):
        type_str = get_string(self._shape_type)
        line = "Type: {}}".format(type_str)
        self.write_line(export_file, line)

    def _export_name(self, export_file):
        line = "name: {}}".format(self._name)
        self.write_line(export_file, line)

    def _export_region_name(self, export_file):
        line = "Region name: {}".format(self._region_name)
        self.write_line(export_file, line)

    def _export_translation(self, export_file):
        line = "Translation:"
        self.write_line(export_file, line)

        for label, value in zip(["X", 'Y', 'z'], self._translation):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

    def _export_rotation(self, export_file):
        line = "Rotation:"
        self.write_line(export_file, line)

        for label, value in zip(["X", 'Y', 'z'], self._rotation):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

    def _export_scale(self, export_file):
        line = "Scale:"
        self.write_line(export_file, line)

        for label, value in zip(["X", 'Y', 'z'], self._scale):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

    def _export_color(self, export_file):
        line = "Color:"
        self.write_line(export_file, line)

        for label, value in zip(["R", 'G', 'B'], self._color):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

    def modify_position_z(self, new_position_z_nm):
        if not self._file.closed:
            current_position = self._file.tell()
            self._file.close()
        else:
            current_position = 0

        self._file = open(self._file_pathname, 'r+b')

        self._file.seek(self._start_position)
        self._translation = (self._translation[0], self._translation[1], new_position_z_nm)

        self._modify(self._file)

        self._file.close()
        self._file = open(self._file_pathname, 'rb')
        self._file.seek(current_position)

    def _modify(self, file):
        assert file.mode == 'r+b'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write", file.tell())

        tag_id = "%SMPLOBJ"
        if self.find_tag(file, tag_id):
            self.write_int(file, self._version)

            self.write_str(file, self._name)
            self.write_str(file, self._region_name)

            self.write_double_list(file, self._translation, 3)
            self.write_double_list(file, self._rotation, 3)
            self.write_double_list(file, self._scale, 3)
            self.write_double_list(file, self._color, 3)
