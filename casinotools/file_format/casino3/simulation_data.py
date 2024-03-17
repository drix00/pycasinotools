#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.simulation_data
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
from casinotools.file_format.casino3.sample import Sample
from casinotools.file_format.casino3.simulation_options import SimulationOptions
from casinotools.file_format.casino3.scan_point_positions import ScanPointPositions
from casinotools.file_format.casino3.simulation_results import SimulationResults

# Globals and constants variables.
# TODO: Old Reader modules, refactor to use the data module directly.


class SimulationData(object):
    def __init__(self):
        self._sample = Sample()
        self._options = SimulationOptions()
        self._scan_point_positions = ScanPointPositions()
        self._results = SimulationResults()

    def set_sample(self, sample):
        self._sample = sample

    def set_options(self, options):
        self._options = options

    def set_scan_point_positions(self, scan_point_positions):
        self._scan_point_positions = scan_point_positions

    def set_results(self, results):
        self._results = results

    def read_sample(self, file):
        self._sample.read(file)

    def read_options(self, file):
        self._options.read(file)

    def read_scan_point_positions(self, file):
        self._scan_point_positions.read(file)

    def read_results(self, file):
        self._results.read(file, self._options)

    def write_sample(self, file):
        logging.info("write_sample")
        self._sample.write(file)

    def write_options(self, file):
        logging.info("write_options")
        self._options.write(file)

    def write_scan_point_positions(self, file):
        logging.info("write_scan_point_positions")
        self._scan_point_positions.write(file)

    def write_results(self, file):
        logging.info("write_results")
        self._results.write(file)

    def get_scan_point_positions(self):
        return self._scan_point_positions.get_positions()

    def get_result_list(self):
        return self._results

    def get_first_scan_point_results(self):
        return self._results.get_first_scan_point_results()

    def get_options(self):
        return self._options

    def get_sample(self):
        return self._sample

    def export(self, export_file):
        self._sample.export(export_file)
        self._options.export(export_file)
        self._scan_point_positions.export(export_file)
