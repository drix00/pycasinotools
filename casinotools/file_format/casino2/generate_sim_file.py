#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.generate_sim_file
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.casino2.file import File

# Globals and constants variables.


class GenerateSimFile:
    def __init__(self, template_filepath):
        self._templateFilepath = template_filepath
        self._optionSimulationData = self._extract_option_simulation_data(self._templateFilepath)

    @staticmethod
    def _extract_option_simulation_data(filepath):
        file = File()
        file.read_from_filepath(filepath)

        return file.get_option_simulation_data()

    def get_option_simulation_data(self):
        return self._optionSimulationData

    def set_number_electrons(self, number_electrons):
        self._optionSimulationData.get_simulation_options().set_number_electrons(number_electrons)

    def set_incident_energy_keV(self, energy_keV):
        self._optionSimulationData.get_simulation_options().set_incident_energy_keV(energy_keV)

    def set_toa_deg(self, toa_deg):
        self._optionSimulationData.get_simulation_options().set_toa_deg(toa_deg)

    def set_beam_angle_deg(self, beam_angle_deg):
        self._optionSimulationData.get_simulation_options().set_beam_angle_deg(beam_angle_deg)

    def add_elements(self, symbols, weight_fractions=None):
        self._remove_all_elements()

        if weight_fractions is None:
            weight_fractions = []

        if len(weight_fractions) == len(symbols) - 1:
            last_weight_fraction = 1.0 - sum(weight_fractions)
            weight_fractions.append(last_weight_fraction)

        assert len(weight_fractions) == len(symbols)

        for symbol, weightFraction in zip(symbols, weight_fractions):
            self._add_element(symbol, weightFraction)

        self._optionSimulationData.get_region_options().get_region(0).update()

    def _remove_all_elements(self):
        self._optionSimulationData.get_region_options().get_region(0).remove_all_elements()

    def _add_element(self, symbol, weight_fraction=1.0):
        number_x_ray_layers = self._optionSimulationData.get_simulation_options().get_number_x_ray_layers()
        self._optionSimulationData.get_region_options().get_region(0).add_element(symbol, weight_fraction,
                                                                                  number_x_ray_layers)

    def save(self, filepath):
        file = File()
        file.set_option_simulation_data(self._optionSimulationData)
        file.write(filepath)

    def set_direction_cosines(self, direction_cosines_model):
        self._optionSimulationData.get_simulation_options().set_direction_cosines(direction_cosines_model)

    def set_electron_elastic_cross_section(self, cross_section_model):
        options = self._optionSimulationData.get_simulation_options()
        options.set_total_electron_elastic_cross_section(cross_section_model)
        options.set_partial_electron_elastic_cross_section(cross_section_model)

    def set_ionization_cross_section(self, cross_section_model):
        self._optionSimulationData.get_simulation_options().set_ionization_cross_section_type(cross_section_model)

    def set_ionization_potential(self, model):
        self._optionSimulationData.get_simulation_options().set_ionization_potential_type(model)
