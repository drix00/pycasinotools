#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_xray_radial_reader
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.xray_radial_reader` module.
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
import os.path

# Third party modules.
from pkg_resources import resource_filename  # @UnresolvedImport
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino2.xray_radial_reader import XrayRadialReader, K, L, M, HEADER_ELEMENT
from casinotools.file_format.casino2.xray_radial_reader import HEADER_ELEMENT_LINE, HEADER_ALL
from casinotools.file_format.casino2.xray_radial import DISTANCE_nm, INTENSITY, INTENSITY_ABSORBED
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True

# Third party modules.

# Local modules.

# Globals and constants variables.


@pytest.fixture
def base_path():
    base_path = resource_filename(__name__, "../../../test_data/casino2.x/exported_data")
    return base_path


@pytest.fixture
def filepath_Cu_K(base_path):
    file_path = os.path.join(base_path, "XrayRadial_Cu_K.txt")
    return file_path


@pytest.fixture
def filepath_Cu_L(base_path):
    file_path = os.path.join(base_path, "XrayRadial_Cu_L.txt")
    return file_path


@pytest.fixture
def filepath_Au_M(base_path):
    file_path = os.path.join(base_path, "XrayRadial_Au_M.txt")
    return file_path


@pytest.fixture
def filepath_Cu(base_path):
    file_path = os.path.join(base_path, "XrayRadial_Cu.txt")
    return file_path


def test_read_text_file(filepath_Cu_K):
    if is_bad_file(filepath_Cu_K):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Cu_K)

    xray_radial = xray_radial_reader.getData('Cu', K)
    assert xray_radial.get_line() == K
    assert xray_radial.get_element_symbol() == "Cu"

    data_labels_ref = [DISTANCE_nm, INTENSITY, INTENSITY_ABSORBED]
    assert xray_radial.get_data_labels() == data_labels_ref

    distances_nm = xray_radial.get_distances_nm()
    assert len(distances_nm) == 500
    assert distances_nm[0] == pytest.approx(0.0)
    assert distances_nm[-1] == pytest.approx(953.396625)

    intensities = xray_radial.get_intensities()
    assert len(intensities) == 500
    assert intensities[0] == pytest.approx(111.260633)
    assert intensities[-1] == pytest.approx(0.000128)

    intensities_absorbed = xray_radial.get_intensities_absorbed()
    assert len(intensities_absorbed) == 500
    assert intensities_absorbed[0] == pytest.approx(111.007526)
    assert intensities_absorbed[-1] == pytest.approx(0.000127)


def test_getLine(filepath_Cu_K, filepath_Cu_L, filepath_Au_M):
    if is_bad_file(filepath_Cu_K):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Cu_K)
    xray_radial = xray_radial_reader.getData('Cu', K)
    assert xray_radial.get_line() == K

    if is_bad_file(filepath_Cu_L):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Cu_L)
    xray_radial = xray_radial_reader.getData('Cu', L)
    assert xray_radial.get_line() == L

    if is_bad_file(filepath_Au_M):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Au_M)
    xray_radial = xray_radial_reader.getData('Au', M)
    assert xray_radial.get_line() == M


def test_get_element_symbol(filepath_Cu_K, filepath_Cu_L, filepath_Au_M):
    if is_bad_file(filepath_Cu_K):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Cu_K)
    xray_radial = xray_radial_reader.getData('Cu', K)
    assert xray_radial.get_element_symbol() == "Cu"

    if is_bad_file(filepath_Cu_L):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Cu_L)
    xray_radial = xray_radial_reader.getData('Cu', L)
    assert xray_radial.get_element_symbol() == "Cu"

    if is_bad_file(filepath_Au_M):
        pytest.skip()
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Au_M)
    xray_radial = xray_radial_reader.getData('Au', M)
    assert xray_radial.get_element_symbol() == "Au"


def no_test_read_element(filepath_Cu):
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader.readTextFile(filepath_Cu)

    assert xray_radial_reader._version == HEADER_ELEMENT

    xray_radial = xray_radial_reader.getData('Cu', K)
    assert xray_radial.get_element_symbol() == "Cu"
    assert xray_radial.get_line() == K

    xray_radial = xray_radial_reader.getData('Cu', L)
    assert xray_radial.get_element_symbol() == "Cu"
    assert xray_radial.get_line() == L


def test_set_text_file_version():
    line = "Radial XRay Distribution Layer MV of Element Au"
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader._setTextFileVersion(line)
    assert xray_radial_reader._version == HEADER_ELEMENT_LINE

    line = "Radial Distribution of Cu"
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader._setTextFileVersion(line)
    assert xray_radial_reader._version == HEADER_ELEMENT

    line = "XRay Radial of Cu"
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader._setTextFileVersion(line)
    assert xray_radial_reader._version == HEADER_ALL


def test_extract_data_label_line_data_element():
    line = "Distance(nm)\tIntensity: K\tIntensity: K ABS\tIntensity: LIII\tIntensity: LIII ABS"
    xray_radial_reader = XrayRadialReader()
    xray_radial_reader._extractDataLabelLineDataElement(line)
    labels = xray_radial_reader._labels
    assert labels[0] == DISTANCE_nm
