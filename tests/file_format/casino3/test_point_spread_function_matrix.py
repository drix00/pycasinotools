#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_point_spread_function_matrix
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.point_spread_function_matrix` module.
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
from pkg_resources import resource_filename  # @UnresolvedImport
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino3.point_spread_function_matrix import PointSpreadFunctionMatrix
from casinotools.file_format.casino3.file import File
from casinotools.file_format.casino3.version import SIM_OPTIONS_VERSION_3_3_0_0
from casinotools.utilities.path import is_bad_file
from casinotools.file_format.file_reader_writer_tools import extract_version_string

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_sim_no_psfs():
    filepath = resource_filename(__name__, "../../../test_data/casino3.x/PSFs/SiN_woPSFs_bG_T200nm.sim")
    if is_bad_file(filepath):  # pragma: no cover
        pytest.skip(filepath)

    casino_file = File(filepath)

    version_ref = SIM_OPTIONS_VERSION_3_3_0_0
    version_str_ref = "3.3.0.0"

    version = casino_file.get_version()
    assert version == version_ref

    version_str = extract_version_string(version)
    assert version_str == version_str_ref

    options_advanced_psfs_settings = casino_file.get_options().get_options_advanced_psfs_settings()

    assert options_advanced_psfs_settings.is_generating_psfs() is False


def test_sim_psfs():
    filenames = ["SiN_wPSFs_bG_T200nm.sim", "SiN_wPSFs_wConserveData_bG_T200nm.sim"]
    for filename in filenames:
        filepath = resource_filename(__name__, "../../../test_data/casino3.x/PSFs/" + filename)
        if is_bad_file(filepath):  # pragma: no cover
            pytest.skip(filepath)

        casino_file = File(filepath)

        version_ref = SIM_OPTIONS_VERSION_3_3_0_0
        version_str_ref = "3.3.0.0"

        version = casino_file.get_version()
        assert version == version_ref

        version_str = extract_version_string(version)
        assert version_str == version_str_ref

        options_advanced_psfs_settings = casino_file.get_options().get_options_advanced_psfs_settings()

        assert options_advanced_psfs_settings.is_generating_psfs() is True


def test_cas_no_psfs():
    filepath = resource_filename(__name__, "../../../test_data/casino3.x/PSFs/SiN_woPSFs_bG_T200nm.cas")
    if is_bad_file(filepath):  # pragma: no cover
        pytest.skip(filepath)

    casino_file = File(filepath)

    version_ref = SIM_OPTIONS_VERSION_3_3_0_0
    version_str_ref = "3.3.0.0"

    version = casino_file.get_version()
    assert version == version_ref

    version_str = extract_version_string(version)
    assert version_str == version_str_ref

    options_advanced_psfs_settings = casino_file.get_options().get_options_advanced_psfs_settings()
    assert options_advanced_psfs_settings.is_generating_psfs() is False

    scan_point_results = casino_file.get_scan_point_results()
    assert scan_point_results[0].is_psfs() is False
    assert scan_point_results[0].get_point_spread_function_matrix() is None


def test_cas_psfs():
    filename = "SiN_wPSFs_bG_T200nm.cas"
    filepath = resource_filename(__name__, "../../../test_data/casino3.x/PSFs/" + filename)
    if is_bad_file(filepath):  # pragma: no cover
        pytest.skip(filepath)

    casino_file = File(filepath)

    version_ref = SIM_OPTIONS_VERSION_3_3_0_0
    version_str_ref = "3.3.0.0"

    version = casino_file.get_version()
    assert version == version_ref

    version_str = extract_version_string(version)
    assert version_str == version_str_ref

    options_advanced_psfs_settings = casino_file.get_options().get_options_advanced_psfs_settings()

    assert options_advanced_psfs_settings.is_generating_psfs() is True

    scan_point_results = casino_file.get_scan_point_results()
    assert scan_point_results[0].is_psfs() is False
    assert scan_point_results[0].get_point_spread_function_matrix() is None

    filename = "SiN_wPSFs_wConserveData_bG_T200nm.cas"
    filepath = resource_filename(__name__, "../../../test_data/casino3.x/PSFs/" + filename)

    casino_file = File(filepath)

    version_ref = SIM_OPTIONS_VERSION_3_3_0_0
    version_str_ref = "3.3.0.0"

    version = casino_file.get_version()
    assert version == version_ref

    version_str = extract_version_string(version)
    assert version_str == version_str_ref

    options_advanced_psfs_settings = casino_file.get_options().get_options_advanced_psfs_settings()

    assert options_advanced_psfs_settings.is_generating_psfs() is True

    scan_point_results = casino_file.get_scan_point_results()
    assert scan_point_results[0].is_psfs() is True
    assert isinstance(scan_point_results[0].get_point_spread_function_matrix(), PointSpreadFunctionMatrix)
