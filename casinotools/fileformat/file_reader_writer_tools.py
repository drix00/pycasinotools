#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
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
import struct

# Third party modules.

# Local modules.

# Project modules.
from casinotools.fileformat.tags import search_tag, TAG_LENGTH, add_tag_old, add_tag

# Globals and constants variables.


class FileReaderWriterTools(object):
    @staticmethod
    def find_tag(file, tag_id):
        return search_tag(file, tag_id, TAG_LENGTH)

    @staticmethod
    def add_tag_old(file, tag_id):
        return add_tag_old(file, tag_id, TAG_LENGTH)

    @staticmethod
    def add_tag(file, tag_id):
        return add_tag(file, tag_id, TAG_LENGTH)

    def read_int(self, file):
        value_format = "i"
        value = self._read(file, value_format, int)
        return value

    def read_long(self, file):
        # TODO: Check if using i in the value_format is not a bug.
        value_format = "i"
        value = self._read(file, value_format, int)
        return value

    def read_double(self, file):
        value_format = "d"
        value = self._read(file, value_format, float)
        return value

    def read_float(self, file):
        value_format = "f"
        value = self._read(file, value_format, float)
        return value

    def read_bool(self, file):
        value_format = "?"
        value = self._read(file, value_format, bool)
        return value

    def read_str(self, file):
        size = self.read_int(file)
        # self.read_int(file)
        return self.read_str_length(file, size)

    def read_str_length(self, file, size):
        value_format = "{:d}s".format(size)
        value = self._read(file, value_format, bytes)
        value = value.decode('ascii', 'replace')
        value = value.replace('\x00', '')
        return value

    def read_float_list(self, file, number_elements):
        return self._read_float_list_without_loop_fast(file, number_elements)

    @staticmethod
    def _read_float_list_without_loop_fast(file, number_elements):
        value_format = "{:d}f".format(number_elements)
        size = struct.calcsize(value_format)
        buffer = file.read(size)
        items = struct.unpack_from(value_format, buffer)

        return items

    def read_double_list(self, file, number_elements=None):
        if number_elements is None:
            # number_elements = self.read_long(file)
            number_elements = self.read_int(file)

        return self._read_double_list_without_loop_fast(file, number_elements)

    def _read_double_list_with_loop(self, file, number_elements):
        array = []
        for dummy in range(number_elements):
            value = self.read_double(file)
            array.append(value)

        return array

    @staticmethod
    def _read_double_list_without_loop(file, number_elements):
        value_format = "{:d}d".format(number_elements)
        size = struct.calcsize(value_format)
        buffer = file.read(size)
        items = struct.unpack_from(value_format, buffer)
        array = [float(item) for item in items]

        return array

    @staticmethod
    def _read_double_list_without_loop_fast(file, number_elements):
        if number_elements > 0:
            value_format = "{:d}d".format(number_elements)
            size = struct.calcsize(value_format)
            buffer = file.read(size)
            items = struct.unpack_from(value_format, buffer)

            return items
        else:
            return []

    def read_int_list(self, file, number_elements):
        return self._read_int_list_without_loop_fast(file, number_elements)

    @staticmethod
    def _read_int_list_without_loop_fast(file, number_elements):
        value_format = "{:d}i".format(number_elements)
        size = struct.calcsize(value_format)
        buffer = file.read(size)
        items = struct.unpack_from(value_format, buffer)

        return items

    @staticmethod
    def get_size_of_double_list(number_elements):
        value_format = "{:d}d".format(number_elements)
        size = struct.calcsize(value_format)
        return size

    @staticmethod
    def get_size_of_int_list(number_elements):
        value_format = "{:d}i".format(number_elements)
        size = struct.calcsize(value_format)
        return size

    @staticmethod
    def _read(file, value_format, value_type):
        size = struct.calcsize(value_format)
        buffer = file.read(size)
        items = struct.unpack_from(value_format, buffer)
        return value_type(items[0])

    @staticmethod
    def read_multiple_values(file, value_format):
        size = struct.calcsize(value_format)
        buffer = file.read(size)
        items = struct.unpack_from(value_format, buffer)
        return items

    def write_str_length(self, file, value, size):
        value = self._check_and_correct_value_size(value, size)
        value_format = "%is" % (size,)
        value = value.encode('ascii', 'replace')
        self._write(file, value_format, value, bytes)

    @staticmethod
    def _check_and_correct_value_size(value, size):
        if len(value) > size:
            value = value[:size]
        assert len(value) <= size
        return value

    def write_int(self, file, value):
        value_format = "i"
        self._write(file, value_format, value, int)

    def write_double(self, file, value):
        value_format = "d"
        self._write(file, value_format, value, float)

    def write_long(self, file, value):
        value_format = "=l"
        self._write(file, value_format, value, int)

    def write_bool(self, file, value):
        value_format = "?"
        self._write(file, value_format, value, bool)

    def write_float(self, file, value):
        value_format = "f"
        self._write(file, value_format, value, float)

    def write_str(self, file, value):
        size = len(value)
        self.write_int(file, size)
        self.write_str_length(file, value, size)

    def write_double_list(self, file, value_list, number_elements):
        assert len(value_list) == number_elements
        self._write_double_list_without_loop(file, value_list, number_elements)

    def _write_double_list_with_loop(self, file, value_list, number_elements):
        for index in range(number_elements):
            self.write_double(file, value_list[index])

    @staticmethod
    def _write_double_list_without_loop(file, value_list, number_elements):
        value_format = "{:d}d".format(number_elements)
        buffer = struct.pack(value_format, *value_list)
        file.write(buffer)

    @staticmethod
    def _write(file, value_format, value, value_type):
        value = value_type(value)
        buffer = struct.pack(value_format, value)
        file.write(buffer)
        file.flush()

    def export(self, export_file):
        raise NotImplementedError

    @staticmethod
    def write_line(file, line):
        if not line.endswith('\n'):
            line += '\n'
        file.write(line)

    @staticmethod
    def _extract_version_string(version):
        """
        30103040
        """
        text = str(version)

        major = int(text[0])
        minor = int(text[1:3])
        revision = int(text[3:5])
        build = int(text[5:])

        version_str = "%s.%s.%s.%s" % (major, minor, revision, build)
        return version_str

    @staticmethod
    def _extract_boolean_string(boolean_value):
        boolean_value = bool(boolean_value)

        if boolean_value:
            return "true"
        else:
            return "false"
