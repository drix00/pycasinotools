#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.fileformat.test_file_reader_writer_tools
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:``casinotools.fileformat.file_reader_writer_tools` module.
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
import unittest
import shutil

# Third party modules.
from pkg_resources import resource_filename
import pytest

# Local modules.

# Project modules.
from casinotools.fileformat.file_reader_writer_tools import FileReaderWriterTools
import casinotools.fileformat.casino3.File as File
from casinotools.utilities.path import create_path, get_current_module_path
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


@pytest.fixture()
def filepath_sim():
    file_path = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
    return file_path


@pytest.fixture()
def filepath_sim_3202():
    file_path = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points_3202.sim")
    return file_path


@pytest.fixture()
def filepath_cas():
    file_path = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")
    return file_path


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


class TestFileReaderWriterTools(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.filepathSim_3202 = resource_filename(__name__,
                                                  "../../test_data/casino3.x/SiSubstrateThreeLines_Points_3202.sim")
        self.filepathCas = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")

        path = get_current_module_path(__file__, "../../test_data/temp")
        self.temporaryDir = create_path(path)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.temporaryDir, ignore_errors=True)


def test_check_and_correct_value_size():
    value_ref = "WinCasino Simulation File"
    size = 26
    value = FileReaderWriterTools()._check_and_correct_value_size(value_ref, size)
    assert value == value_ref

    size = 6
    value = FileReaderWriterTools()._check_and_correct_value_size(value_ref, size)
    assert value != value_ref
    assert value == value_ref[:size]


def test_extract_version_string(filepath_sim):
    if is_bad_file(filepath_sim):
        pytest.skip()
    casino_file = File.File(filepath_sim)

    version = File.V30103040
    version_str_ref = "3.1.3.40"
    version_str = casino_file._extract_version_string(version)
    assert version_str == version_str_ref

    version = File.V30103070
    version_str_ref = "3.1.3.70"
    version_str = casino_file._extract_version_string(version)
    assert version_str == version_str_ref

    version = File.V30104060
    version_str_ref = "3.1.4.60"
    version_str = casino_file._extract_version_string(version)
    assert version_str == version_str_ref

    version = File.V30107002
    version_str_ref = "3.1.7.2"
    version_str = casino_file._extract_version_string(version)
    assert version_str == version_str_ref
