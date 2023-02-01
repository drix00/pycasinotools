#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.file_reader_writer_tools
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

# Globals and constants variables.


def read_int(file):
    value_format = "i"
    value = _read(file, value_format, int)
    return value


def read_long(file):
    value_format = "l"
    value = _read(file, value_format, int)
    return value


def read_double(file):
    value_format = "d"
    value = _read(file, value_format, float)
    return value


def read_float(file):
    value_format = "f"
    value = _read(file, value_format, float)
    return value


def read_bool(file):
    value_format = "?"
    value = _read(file, value_format, bool)
    return value


def read_str(file):
    size = read_int(file)
    return _read_str_length(file, size)


def _read_str_length(file, size):
    value_format = "{:d}s".format(size)
    value = _read(file, value_format, bytes)
    value = value.decode('ascii', 'replace')
    value = value.replace('\x00', '')
    return value


def _read(file, value_format, value_type):
    size = struct.calcsize(value_format)
    buffer = file.read(size)
    items = struct.unpack_from(value_format, buffer)
    return value_type(items[0])


def read_float_list(file, number_elements):
    return _read_float_list_without_loop_fast(file, number_elements)


def _read_float_list_without_loop_fast(file, number_elements):
    value_format = "{:d}f".format(number_elements)
    size = struct.calcsize(value_format)
    buffer = file.read(size)
    items = struct.unpack_from(value_format, buffer)

    return list(items)


def read_double_list(file, number_elements=None):
    if number_elements is None:
        number_elements = read_int(file)

    return read_double_list_without_loop_fast(file, number_elements)


def read_double_list_with_loop(file, number_elements):
    array = []
    for dummy in range(number_elements):
        value = read_double(file)
        array.append(value)

    return array


def read_double_list_without_loop(file, number_elements):
    value_format = "{:d}d".format(number_elements)
    size = struct.calcsize(value_format)
    buffer = file.read(size)
    items = struct.unpack_from(value_format, buffer)
    array = [float(item) for item in items]

    return array


def read_double_list_without_loop_fast(file, number_elements):
    if number_elements > 0:
        value_format = "{:d}d".format(number_elements)
        size = struct.calcsize(value_format)
        buffer = file.read(size)
        items = struct.unpack_from(value_format, buffer)

        return list(items)
    else:
        return []


def read_int_list(file, number_elements):
    return _read_int_list_without_loop_fast(file, number_elements)


def _read_int_list_without_loop_fast(file, number_elements):
    value_format = "{:d}i".format(number_elements)
    size = struct.calcsize(value_format)
    buffer = file.read(size)
    items = struct.unpack_from(value_format, buffer)

    return list(items)


def get_size_of_double_list(number_elements):
    value_format = "{:d}d".format(number_elements)
    size = struct.calcsize(value_format)
    return size


def get_size_of_int_list(number_elements):
    value_format = "{:d}i".format(number_elements)
    size = struct.calcsize(value_format)
    return size


def read_multiple_values(file, value_format):
    size = struct.calcsize(value_format)
    buffer = file.read(size)
    items = struct.unpack_from(value_format, buffer)
    return items


def check_and_correct_value_size(value, size):
    if len(value) > size:
        value = value[:size]
    assert len(value) <= size
    return value


def write_int(file, value):
    value_format = "i"
    _write(file, value_format, value, int)


def write_long(file, value):
    value_format = "=l"
    _write(file, value_format, value, int)


def write_double(file, value):
    value_format = "d"
    _write(file, value_format, value, float)


def write_bool(file, value):
    value_format = "?"
    _write(file, value_format, value, bool)


def write_float(file, value):
    value_format = "f"
    _write(file, value_format, value, float)


def write_str(file, value):
    size = len(value)
    write_int(file, size)
    _write_str_length(file, value, size)


def _write_str_length(file, value, size):
    value = check_and_correct_value_size(value, size)
    value_format = "%is" % (size,)
    value = value.encode('ascii', 'replace')
    _write(file, value_format, value, bytes)


def _write(file, value_format, value, value_type):
    value = value_type(value)
    buffer = struct.pack(value_format, value)
    file.write(buffer)
    file.flush()


def write_double_list(file, value_list, number_elements=None):
    if number_elements is None:
        number_elements = len(value_list)
    assert len(value_list) == number_elements
    write_double_list_without_loop(file, value_list, number_elements)


def write_double_list_with_loop(file, value_list, number_elements):
    for index in range(number_elements):
        write_double(file, value_list[index])


def write_double_list_without_loop(file, value_list, number_elements):
    value_format = "{:d}d".format(number_elements)
    buffer = struct.pack(value_format, *value_list)
    file.write(buffer)


def write_int_list(file, value_list):
    number_elements = len(value_list)
    value_format = "{:d}i".format(number_elements)
    buffer = struct.pack(value_format, *value_list)
    file.write(buffer)


def write_float_list(file, value_list):
    number_elements = len(value_list)
    value_format = "{:d}f".format(number_elements)
    buffer = struct.pack(value_format, *value_list)
    file.write(buffer)


def write_line(file, line):
    if not line.endswith('\n'):
        line += '\n'
    file.write(line)


def extract_version_string(version):
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


def extract_boolean_string(boolean_value):
    boolean_value = bool(boolean_value)

    if boolean_value:
        return "true"
    else:
        return "false"
