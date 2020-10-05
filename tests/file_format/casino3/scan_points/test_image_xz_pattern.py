#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.scan_points.test_image_xz_pattern
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.scan_points.image_xz_pattern` module.
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
from casinotools.file_format.casino3.scan_points.image_xz_pattern import ImageXZPattern

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True

# Globals and constants variables.


def test_get_scan_points():
    image_xz = ImageXZPattern()

    image_xz.set_center_point_nm((5.0, -350.0))
    image_xz.set_step_x_nm(10.0)
    image_xz.set_range_x_nm(20.0)
    image_xz.set_step_z_nm(200.0)
    image_xz.set_range_z_nm(200.0)

    scan_points = image_xz.get_scan_points()

    scan_points_ref = [(-5.0, -450.0), (5.0, -450.0), (15.0, -450.0), (-5.0, -250.0), (5.0, -250.0), (15.0, -250.0)]

    assert len(scan_points) == len(scan_points_ref)

    for pointRef, point in zip(scan_points_ref, scan_points):
        x_ref, y_ref = pointRef
        x, y = point

        assert x == pytest.approx(x_ref)
        assert y == pytest.approx(y_ref)
