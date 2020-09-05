#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.test_file_reader_writer_tools
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.file_reader_writer_tools` module.
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
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import _check_and_correct_value_size, _extract_version_string, \
    _extract_boolean_string
from casinotools.file_format.file_reader_writer_tools import write_int, read_int, write_long, read_long, \
    write_double, read_double, write_float, read_float, write_bool, read_bool, write_str, read_str, \
    write_double_list, read_double_list, _write_double_list_with_loop, _write_double_list_without_loop, \
    _read_double_list_with_loop, _read_double_list_without_loop, _read_double_list_without_loop_fast, \
    write_float_list, read_float_list, write_int_list, read_int_list, get_size_of_double_list, get_size_of_int_list
from casinotools.file_format.casino3.file import File, V30103040, V30103070, V30104060, V30107002
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_check_and_correct_value_size():
    value_ref = "WinCasino Simulation File"
    size = 26
    value = _check_and_correct_value_size(value_ref, size)
    assert value == value_ref

    size = 6
    value = _check_and_correct_value_size(value_ref, size)
    assert value != value_ref
    assert value == value_ref[:size]


def test_extract_version_string(filepath_sim):
    if is_bad_file(filepath_sim):  # pragma: no cover
        pytest.skip()
    casino_file = File(filepath_sim)

    version = V30103040
    version_str_ref = "3.1.3.40"
    version_str = _extract_version_string(version)
    assert version_str == version_str_ref

    version = V30103070
    version_str_ref = "3.1.3.70"
    version_str = _extract_version_string(version)
    assert version_str == version_str_ref

    version = V30104060
    version_str_ref = "3.1.4.60"
    version_str = _extract_version_string(version)
    assert version_str == version_str_ref

    version = V30107002
    version_str_ref = "3.1.7.2"
    version_str = _extract_version_string(version)
    assert version_str == version_str_ref


@pytest.mark.parametrize("value, value_str_ref",
                         [(0, "false"),
                          (1, "true"),
                          (2, "true"),
                          ('0', "true"),
                          ('1', "true"),
                          ('2', "true"),
                          (0.0, "false"),
                          (1.0, "true"),
                          (2.0, "true"),
                          (False, "false"),
                          (True, "true"),
                          ])
def test_extract_boolean_string(value, value_str_ref):
    value_str = _extract_boolean_string(value)
    assert value_str == value_str_ref


def test_write_int(tmpdir):
    value_ref = 34
    size = struct.calcsize("i")
    file_path = tmpdir / "test_write_int.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_int(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_int(fp)
        assert value == value_ref


def test_write_long(tmpdir):
    value_ref = 34
    size = struct.calcsize("l")
    file_path = tmpdir / "test_write_long.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_long(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_long(fp)
        assert value == value_ref


def test_write_double(tmpdir):
    value_ref = 34.545689
    size = struct.calcsize("d")
    file_path = tmpdir / "test_write_double.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_double(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_double(fp)
        assert value == value_ref


def test_write_float(tmpdir):
    value_ref = 34.540000915527344
    size = struct.calcsize("f")
    file_path = tmpdir / "test_write_float.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_float(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_float(fp)
        assert value == value_ref


def test_write_bool(tmpdir):
    value_ref = True
    size = struct.calcsize("?")
    file_path = tmpdir / "test_write_bool.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_bool(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_bool(fp)
        assert value == value_ref


def test_write_str(tmpdir):
    value_ref = "fadsf sdafasdf sadf"
    size = struct.calcsize("i") + len(value_ref)
    file_path = tmpdir / "test_write_str.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_str(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_str(fp)
        assert value == value_ref


def test_write_double_list(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    size = struct.calcsize("d") * len(value_ref)
    file_path = tmpdir / "test_write_double_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_double_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_double_list(fp, len(value_ref))
        assert value == value_ref


def test_write_double_list_with_loop(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    number_elements = len(value_ref)
    size = struct.calcsize("d") * number_elements
    file_path = tmpdir / "test_write_double_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        _write_double_list_with_loop(fp, value_ref, number_elements)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_double_list(fp, number_elements)
        assert value == value_ref


def test_write_double_list_without_loop(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    number_elements = len(value_ref)
    size = struct.calcsize("d") * number_elements
    file_path = tmpdir / "test_write_double_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        _write_double_list_without_loop(fp, value_ref, number_elements)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_double_list(fp, number_elements)
        assert value == value_ref


def test_read_double_list_with_loop(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    size = struct.calcsize("d") * len(value_ref)
    file_path = tmpdir / "test_write_double_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_double_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = _read_double_list_with_loop(fp, len(value_ref))
        assert value == value_ref


def test_read_double_list_without_loop(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    size = struct.calcsize("d") * len(value_ref)
    file_path = tmpdir / "test_write_double_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_double_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = _read_double_list_without_loop(fp, len(value_ref))
        assert value == value_ref


def test_read_double_list_without_loop_fast(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    size = struct.calcsize("d") * len(value_ref)
    file_path = tmpdir / "test_write_double_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_double_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = _read_double_list_without_loop_fast(fp, len(value_ref))
        assert value == value_ref

        value = _read_double_list_without_loop_fast(fp, 0)
        assert value == []


def test_read_double_list_wo_number_elements(tmpdir):
    value_ref = [34.545689, 456534.231423, 234.5647654]
    number_elements = len(value_ref)
    size = struct.calcsize("d") * number_elements + struct.calcsize("i")
    file_path = tmpdir / "test_read_double_list_wo_number_elements.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_int(fp, number_elements)
        write_double_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_double_list(fp)
        assert value == value_ref


def test_write_float_list(tmpdir):
    value_ref = [34.54568862915039, 456534.21875, 234.56475830078125]
    size = struct.calcsize("f") * len(value_ref)
    file_path = tmpdir / "test_write_float_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_float_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_float_list(fp, len(value_ref))
        assert value == value_ref


def test_write_int_list(tmpdir):
    value_ref = [34, 456534, 234]
    size = struct.calcsize("i") * len(value_ref)
    file_path = tmpdir / "test_write_float_list.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        write_int_list(fp, value_ref)
        assert fp.tell() == start_pos + size

    with open(file_path, 'rb') as fp:
        value = read_int_list(fp, len(value_ref))
        assert value == value_ref


def test_get_size_of_double_list():
    assert get_size_of_double_list(3) == 8*3


def test_get_size_of_int_list():
    assert get_size_of_int_list(3) == 4*3
