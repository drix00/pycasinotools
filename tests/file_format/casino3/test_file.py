#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.file` module.
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
from casinotools.file_format.casino3.file import File, SIMULATION_CONFIGURATIONS, SIMULATION_RESULTS
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True

# Local modules.

# Globals and constants variables.


def test_init(filepath_sim):
    if is_bad_file(filepath_sim):
        pytest.skip()

    casino_file = File(filepath_sim)

    assert casino_file.get_filepath() == filepath_sim


def test_get_file_type(filepath_sim):
    if is_bad_file(filepath_sim):
        pytest.skip()
    casino_file = File(filepath_sim)

    file_type = casino_file.get_file_type()
    assert file_type == SIMULATION_CONFIGURATIONS

#        casino_file = File.File(self.filepathCas)
#        shape_type = casino_file.get_file_type()
#        assert File.SIMULATION_RESULTS, shape_type)


def test__read_extension(filepath_sim, filepath_cas):
    if is_bad_file(filepath_sim):
        pytest.skip()
    casino_file = File(filepath_sim)
    file = casino_file._open(filepath_sim)
    extension = casino_file._read_extension(file)
    assert extension == SIMULATION_CONFIGURATIONS

    file = open(filepath_cas, 'rb')
    extension = casino_file._read_extension(file)
    assert extension == SIMULATION_RESULTS


def test__read_version(filepath_sim):
    if is_bad_file(filepath_sim):
        pytest.skip()
    casino_file = File(filepath_sim)
    file = casino_file._open(filepath_sim)
    version = casino_file._read_version(file)
    assert version == 30107002


def test_open(filepath_sim):
    if is_bad_file(filepath_sim):
        pytest.skip()
    casino_file = File(filepath_sim)
    casino_file.open()

    assert casino_file._version == 30107002
    assert casino_file._numberSimulations == 1


def test_read_cas_file(filepath_cas):
    if is_bad_file(filepath_cas):
        pytest.skip()
    casino_file = File(filepath_cas)
    casino_file.open()

    assert casino_file._version == 30107002
    assert casino_file._numberSimulations == 1
