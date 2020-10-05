#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`module_name` module.
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
import pytest
# Local modules.

# Project modules.
from casinotools.file_format.casino3.scan_points.scan_points_file import ScanPointsFile

# Globals and constants variables.


@pytest.fixture
def scan_points_file():
    scan_points_file = ScanPointsFile()
    scan_points_file.set_number_points(100)
    scan_points_file.set_width_nm(10)
    scan_points_file.set_height_nm(10)
    return scan_points_file


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_compute_separation_nm(scan_points_file):
    assert scan_points_file._separation_nm is None

    scan_points_file._compute_separation_nm()
    separation_ref_nm = 1.0
    assert scan_points_file._separation_nm == pytest.approx(separation_ref_nm)

    scan_points_file.set_number_points(10000)
    scan_points_file._compute_separation_nm()
    separation_ref_nm = 0.1
    assert scan_points_file._separation_nm == pytest.approx(separation_ref_nm)

    scan_points_file.set_number_points(10)
    scan_points_file._compute_separation_nm()
    separation_ref_nm = 3.1622776601683795
    assert scan_points_file._separation_nm == pytest.approx(separation_ref_nm)

    scan_points_file.set_number_points(100)
    scan_points_file.set_width_nm(50)
    scan_points_file.set_height_nm(50)
    scan_points_file._compute_separation_nm()
    separation_ref_nm = 5.0
    assert scan_points_file._separation_nm == pytest.approx(separation_ref_nm)

    scan_points_file.set_number_points(100)
    scan_points_file.set_width_nm(50)
    scan_points_file.set_height_nm(10)
    scan_points_file._compute_separation_nm()
    separation_ref_nm = 2.236067977499
    assert scan_points_file._separation_nm == pytest.approx(separation_ref_nm)


def test_generate_scan_points(scan_points_file):
    assert scan_points_file._scan_points == []

    scan_points_file._generate_scan_points()
    assert len(scan_points_file._scan_points) == 100

    first_point_ref_nm = (-4.5, -4.5)
    first_point_nm = scan_points_file._scan_points[0]
    assert first_point_nm[0] == pytest.approx(first_point_ref_nm[0])
    assert first_point_nm[1] == pytest.approx(first_point_ref_nm[1])

    last_point_ref_nm = (4.5, 4.5)
    last_point_nm = scan_points_file._scan_points[-1]
    assert last_point_nm[0] == pytest.approx(last_point_ref_nm[0])
    assert last_point_nm[1] == pytest.approx(last_point_ref_nm[1])


def test_generate_line_scan(scan_points_file):
    assert scan_points_file._scan_points == []

    scan_points_file.set_height_nm(100.0)
    scan_points_file.set_width_nm(0.0)

    scan_points_file._generate_scan_points()
    assert len(scan_points_file._scan_points) == 100

    first_point_ref_nm = (0.0, -49.5)
    first_point_nm = scan_points_file._scan_points[0]
    assert first_point_nm[0] == pytest.approx(first_point_ref_nm[0])
    assert first_point_nm[1] == pytest.approx(first_point_ref_nm[1])

    last_point_ref_nm = (0.0, 49.5)
    last_point_nm = scan_points_file._scan_points[-1]
    assert last_point_nm[0] == pytest.approx(last_point_ref_nm[0])
    assert last_point_nm[1] == pytest.approx(last_point_ref_nm[1])

    scan_points_file.set_height_nm(0.0)
    scan_points_file.set_width_nm(100.0)

    scan_points_file._generate_scan_points()
    assert len(scan_points_file._scan_points) == 100

    first_point_ref_nm = (-49.5, 0.0)
    first_point_nm = scan_points_file._scan_points[0]
    assert first_point_nm[0] == pytest.approx(first_point_ref_nm[0])
    assert first_point_nm[1] == pytest.approx(first_point_ref_nm[1])

    last_point_ref_nm = (49.5, 0.0)
    last_point_nm = scan_points_file._scan_points[-1]
    assert last_point_nm[0] == pytest.approx(last_point_ref_nm[0])
    assert last_point_nm[1] == pytest.approx(last_point_ref_nm[1])


def test_set_center_point(scan_points_file):
    assert scan_points_file._scan_points == []

    scan_points_file.set_height_nm(100.0)
    scan_points_file.set_width_nm(0.0)
    x_ref = -23.6
    y_ref = 50.0
    scan_points_file.set_center_point((x_ref, y_ref))

    scan_points_file._generate_scan_points()
    assert len(scan_points_file._scan_points) == 100

    first_point_ref_nm = (x_ref, -49.5 + y_ref)
    first_point_nm = scan_points_file._scan_points[0]
    assert first_point_nm[0] == pytest.approx(first_point_ref_nm[0])
    assert first_point_nm[1] == pytest.approx(first_point_ref_nm[1])

    last_point_ref_nm = (x_ref, 49.5 + y_ref)
    last_point_nm = scan_points_file._scan_points[-1]
    assert last_point_nm[0] == pytest.approx(last_point_ref_nm[0])
    assert last_point_nm[1] == pytest.approx(last_point_ref_nm[1])

    scan_points_file.set_height_nm(0.0)
    scan_points_file.set_width_nm(100.0)

    scan_points_file._generate_scan_points()
    assert len(scan_points_file._scan_points) == 100

    first_point_ref_nm = (-49.5 + x_ref, 0.0 + y_ref)
    first_point_nm = scan_points_file._scan_points[0]
    assert first_point_nm[0] == pytest.approx(first_point_ref_nm[0])
    assert first_point_nm[1] == pytest.approx(first_point_ref_nm[1])

    last_point_ref_nm = (49.5 + x_ref, 0.0 + y_ref)
    last_point_nm = scan_points_file._scan_points[-1]
    assert last_point_nm[0] == pytest.approx(last_point_ref_nm[0])
    assert last_point_nm[1] == pytest.approx(last_point_ref_nm[1])

    scan_points_file.set_width_nm(10)
    scan_points_file.set_height_nm(10)
    scan_points_file.set_center_point((x_ref, y_ref))

    scan_points_file._generate_scan_points()
    assert len(scan_points_file._scan_points) == 100

    first_point_ref_nm = (-4.5 + x_ref, -4.5 + y_ref)
    first_point_nm = scan_points_file._scan_points[0]
    assert first_point_nm[0] == pytest.approx(first_point_ref_nm[0])
    assert first_point_nm[1] == pytest.approx(first_point_ref_nm[1])

    last_point_ref_nm = (4.5 + x_ref, 4.5 + y_ref)
    last_point_nm = scan_points_file._scan_points[-1]
    assert last_point_nm[0] == pytest.approx(last_point_ref_nm[0])
    assert last_point_nm[1] == pytest.approx(last_point_ref_nm[1])


def test_generate_lines(scan_points_file):
    lines = scan_points_file._generate_lines()
    assert len(lines) == 100

    first_lines_ref_nm = "-4.500000, -4.500000\n"
    assert lines[0] == first_lines_ref_nm

    last_lines_ref_nm = "4.500000, 4.500000\n"
    assert lines[-1] == last_lines_ref_nm


def test_is_line_valid(scan_points_file):
    spf = scan_points_file
    line = ""
    assert spf._is_line_valid(line) is False

    line = "4.500000, 4.500000\n"
    assert spf._is_line_valid(line) is True
    line = "4.500000, 4.500000\r"
    assert spf._is_line_valid(line) is True
    line = "4.500000, 4.500000\r\n"
    assert spf._is_line_valid(line) is True
    line = "-4.500000, -4.500000"
    assert spf._is_line_valid(line) is False

    line = "-4.500000, -4.500000\n"
    assert spf._is_line_valid(line) is True

    line = "4.500000 4.500000\n"
    assert spf._is_line_valid(line) is False
    line = "-4.as000, -4.500000\n"
    assert spf._is_line_valid(line) is False
    line = "-4.500000, -4.asd000\n"
    assert spf._is_line_valid(line) is False
    line = "-e.500000, -4.500000\n"
    assert spf._is_line_valid(line) is False
    line = "-4.500000, -a.500000\n"
    assert spf._is_line_valid(line) is False

    line = "-4.500000, -4.500000\n"
    assert spf._is_line_valid(line) is True

    line = "-4.50000000000000000000000000000, -4.50000000000000000000000000000\n"
    assert spf._is_line_valid(line) is False


def test_different_number_electrons_in_y_and_z():
    number_points_list = [(300, 250), (300, 100), (300, 25)]
    for number_points_y, number_points_z in number_points_list:
        scan_points_file = ScanPointsFile()
        scan_points_file.set_width_nm(300, number_points_y)
        scan_points_file.set_height_nm(2500, number_points_z)
        scan_points_file.set_center_point((0.0, 500.0))

        assert scan_points_file.get_number_points() == number_points_y * number_points_z
