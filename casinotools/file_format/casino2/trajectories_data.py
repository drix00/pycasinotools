#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.trajectories_data
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
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_long
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino2.trajectory import Trajectory

# Globals and constants variables.

# Third party modules.

# Local modules.

# Globals and constants variables.


class TrajectoriesData:
    def __init__(self, is_skip_reading_data=False):
        self._is_skip_reading_data = is_skip_reading_data

        self.number_trajectories = 0
        self._trajectories = []

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = b"*TRAJDATA%%%%%%"
        find_tag(file, tag_id)

        self.number_trajectories = read_long(file)

        self._trajectories = []
        for dummy in range(self.number_trajectories):
            trajectory = Trajectory(self._is_skip_reading_data)
            trajectory.read(file)
            self._trajectories.append(trajectory)

    def get_trajectories(self):
        return self._trajectories
