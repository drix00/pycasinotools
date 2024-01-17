#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_intensity_image
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.intensity_image` module.
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
from casinotools.file_format.casino3.intensity_image import IntensityImage, INTENSITY_TRANSMITTED_DETECTED

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


@pytest.fixture()
def file_path_cas_binned():
    results_path = resource_filename(__name__, "../../../test_data/casino3.x/create_image")
    file_path = os.path.join(results_path, "Au_C_thin_1nm_Inside_100ke_binned.cas")
    return file_path


@pytest.fixture()
def image_binned(file_path_cas_binned):
    image = IntensityImage(file_path_cas_binned)
    return image


@pytest.fixture()
def file_path_cas_all():
    results_path = resource_filename(__name__, "../../../test_data/casino3.x/create_image")
    file_path = os.path.join(results_path, "Au_C_thin_1nm_Inside_100ke_all.cas")
    return file_path


def test_init(image_binned, file_path_cas_binned):
    image = image_binned
    assert image._filepath == file_path_cas_binned
    assert image._intensity_type == INTENSITY_TRANSMITTED_DETECTED


def test_extract_data(image_binned):
    image = image_binned
    image._extract_data()

    assert image._number_scan_points == 100

    assert len(image._positions) == 100
    assert len(image._intensities) == 100


def test_analyze_positions_xy(image_binned):
    positions = [(-5, -5, 0), (0, -5, 0), (5, -5, 0), (-5, 0, 0), (0, 0, 0), (5, 0, 0), (-5, 5, 0), (0, 5, 0),
                 (5, 5, 0)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "XY"


def test_analyze_positions_xz(image_binned):
    positions = [(-5, 0, -5), (0, 0, -5), (5, 0, -5), (-5, 0, 0), (0, 0, 0), (5, 0, 0), (-5, 0, 5), (0, 0, 5),
                 (5, 0, 5)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "XZ"


def test_analyze_positions_yz(image_binned):
    positions = [(0, -5, -5), (0, 0, -5), (0, 5, -5), (0, -5, 0), (0, 0, 0), (0, 5, 0), (0, -5, 5), (0, 0, 5),
                 (0, 5, 5)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "YZ"


def test_analyze_positions_x(image_binned):
    positions = [(-5, 0, 0), (0, 0, 0), (5, 0, 0), (-5, 0, 0), (0, 0, 0), (5, 0, 0), (-5, 0, 0), (0, 0, 0), (5, 0, 0)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "X"


def test_analyze_positions_y(image_binned):
    positions = [(0, -5, 0), (0, 0, 0), (0, 5, 0), (0, -5, 0), (0, 0, 0), (0, 5, 0), (0, -5, 0), (0, 0, 0), (0, 5, 0)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "Y"


def test_analyze_positions_z(image_binned):
    positions = [(0, 0, -5), (0, 0, -5), (0, 0, -5), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 5), (0, 0, 5), (0, 0, 5)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "z"


def test_analyze_positions_p(image_binned):
    positions = [(0, 0, 0)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "P"


def test_analyze_positions_3d(image_binned):
    positions = [(-5, -5, -5), (0, -5, -5), (5, -5, -5), (-5, 0, -5), (0, 0, -5), (5, 0, -5), (-5, 5, -5), (0, 5, -5),
                 (5, 5, -5), (-5, -5, 0), (0, -5, 0), (5, -5, 0), (-5, 0, 0), (0, 0, 0), (5, 0, 0), (-5, 5, 0),
                 (0, 5, 0), (5, 5, 0), (-5, -5, 5), (0, -5, 5), (5, -5, 5), (-5, 0, 5), (0, 0, 5), (5, 0, 5),
                 (-5, 5, 5), (0, 5, 5), (5, 5, 5)]

    image = image_binned
    image._positions = positions
    image._analyze_positions()

    assert image._imageType == "3D"


def test_create_image(image_binned):
    image = image_binned
    image.create_image()
