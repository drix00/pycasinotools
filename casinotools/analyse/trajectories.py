#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Helper to extract and use electron trajectories from CASINO.

.. todo:: Add same helper for CASINO 2.
.. todo:: Add same helper for CASINO 3.
.. todo:: Read data from .cas file.
.. todo:: Read data from exported .dat file.

"""

###############################################################################
# Copyright 2023 Hendrix Demers
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

# Local modules.

# Project modules.
from casinotools.file_format.casino2.file import File as Casino2File
from casinotools.file_format.casino2.version import is_version_casino2
from casinotools.file_format.casino3.file import File as Casino3File
from casinotools.file_format.casino3.file import SIMULATION_CONFIGURATIONS, SIMULATION_RESULTS
from casinotools.file_format.casino3.version import is_version_casino3

# Globals and constants variables.


def is_casino_2_sim_file(file_path):
    """
    status = n
    """
    file = Casino2File()
    version = file.extract_version(file_path)
    if is_version_casino2(version):
        file.read_from_filepath(file_path)
        option_simulation_data = file.get_option_simulation_data()
        if option_simulation_data.status == 'n':
            return True

    return False


def is_casino_2_cas_file(file_path):
    """
    status = f
    """
    file = Casino2File()
    version = file.extract_version(file_path)
    if is_version_casino2(version):
        file.read_from_filepath(file_path)
        option_simulation_data = file.get_option_simulation_data()
        if option_simulation_data.status == 'f':
            return True

    return False


def is_casino_2_data_file(file_path):
    with open(file_path) as data_file:
        try:
            line1 = data_file.readline().strip()
            line2 = data_file.readline().strip()

            if line1 == '-----------------------------------------------------------------' and line2.startswith(
                'Trajectory'):
                return True
        except UnicodeDecodeError:
            return False

    return False


def is_casino_3_sim_file(file_path):
    """
    status = n
    """
    file = Casino3File(file_path)
    if is_version_casino3(file.version):
        if file.type == SIMULATION_CONFIGURATIONS:
            return True

    return False


def is_casino_3_cas_file(file_path):
    """
    status = f
    """
    file = Casino3File(file_path)
    if is_version_casino3(file.version):
        if file.type == SIMULATION_RESULTS:
            return True

    return False


def is_casino_3_data_file(file_path):
    with open(file_path) as data_file:
        try:
            line1 = data_file.readline().strip()
            line2 = data_file.readline().strip()

            if line1 == '"================================================================="' and line2.startswith('"WinCasino 3.'):
                return True
        except UnicodeDecodeError:
            return False

    return False
