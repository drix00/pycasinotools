#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.simulation_options
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
from casinotools.file_format.file_reader_writer_tools import read_int
from casinotools.file_format.tags import find_tag

from casinotools.file_format.casino3.options_physic import OptionsPhysic
from casinotools.file_format.casino3.options_dist import OptionsDist
from casinotools.file_format.casino3.options_micro import OptionsMicro
from casinotools.file_format.casino3.options_adv_back_set import OptionsAdvBackSet
from casinotools.file_format.casino3.options_xray import OptionsXray
from casinotools.file_format.casino3.options_energy_by_pos import OptionsEnergyByPos
from casinotools.file_format.casino3.options_adf import OptionsADF
from casinotools.file_format.casino3.options_advanced_psfs_settings import OptionsAdvancedPsfsSettings
from casinotools.file_format.casino3.version import SIM_OPTIONS_VERSION_3_3_0_0, SIM_OPTIONS_VERSION_3_3_0_4

# Globals and constants variables.


class SimulationOptions:
    def __init__(self):
        self._options_physic = OptionsPhysic()
        self.options_dist = OptionsDist()
        self.options_microscope = OptionsMicro()
        self._options_adv_back_set = OptionsAdvBackSet()
        self._options_xray = OptionsXray()
        self._options_energy_by_pos = OptionsEnergyByPos()
        self._options_adf = OptionsADF()
        self._options_advanced_psfs_settings = OptionsAdvancedPsfsSettings()

        self._file = None
        self._start_position = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._version = 0

    def read(self, file):
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        tag_id = b"*SIMULATIONOPT%"
        if find_tag(file, tag_id):
            self._version = read_int(file)

            self._options_adf.read(file)
            self._options_adv_back_set.read(file)

            if SIM_OPTIONS_VERSION_3_3_0_0 <= self._version < SIM_OPTIONS_VERSION_3_3_0_4:
                self._options_advanced_psfs_settings.read(file)

            self.options_dist.read(file)
            self._options_energy_by_pos.read(file)
            self.options_microscope.read(file)
            self._options_physic.read(file)

            self._options_xray.read(file)

            tag_id = b"*SIM_OPT_END%"
            if not find_tag(file, tag_id):
                return "Wrong version."

        self._end_position = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._end_position)

    def write(self, file):
        raise NotImplementedError

    def export(self, export_file):
        # todo: implement the export method.
        pass

    def get_options_distributions(self):
        return self.options_dist

    def get_options_advanced_psfs_settings(self):
        return self._options_advanced_psfs_settings
