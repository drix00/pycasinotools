#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.region
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
import decimal

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools
from casinotools.file_format.casino3.element import Element

# Globals and constants variables.
decimal.getcontext().prec = 28
EPSILON = 1.0e-4

NB_PAR_MAX = 4

TAG_REGIONS_DATA = b"*regionSDATA%%%"


class Region(FileReaderWriterTools):
    def __init__(self):
        self._file = None
        self._start_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._version = 0
        self._carrier_diffusion_length = 0.0
        self.id_ed = 0

        self._number_elements = 0
        self.rho = 0.0

        self.zmoy = 0.0

        self._work_function = 0.0
        self._average_plasmon_energy = 0.0
        self.id = 0
        self.substrate = 0
        self.user_density = 0
        self.user_composition = 0
        self._checked = 0

        self._energy_intensity = 0.0

        self.name = ""

        self._number_sample_objects = 0

        self._sample_object_ids = {}

        self._moller_init = 0.0
        self._triangle_color_x = 0.0
        self._triangle_color_y = 0.0
        self._triangle_color_z = 0.0

        self._elements = []
        self._chemical_name = ""

    def read(self, file):
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        self._version = self.read_int(file)

        tag_id = TAG_REGIONS_DATA
        self.find_tag(file, tag_id)

        if self._version > 30104072:
            self._carrier_diffusion_length = self.read_double(file)

        if self._version < 30105005:
            self.id_ed = self.read_int(file)

        self._number_elements = self.read_int(file)
        self.rho = self.read_double(file)

        if self._version < 30105001:
            self.zmoy = self.read_double(file)

        self._work_function = self.read_double(file)
        self._average_plasmon_energy = self.read_double(file)
        self.id = self.read_int(file)
        self.substrate = self.read_int(file)
        self.user_density = self.read_int(file)
        self.user_composition = self.read_int(file)
        self._checked = self.read_int(file)

        if self._version < 30105022:
            self._energy_intensity = self.read_double(file)

        self.name = self.read_str(file)

        self._number_sample_objects = self.read_int(file)

        self._sample_object_ids = {}
        for dummy in range(self._number_sample_objects):
            object_id = self.read_int(file)
            inside_or_outside = self.read_int(file)

            self._sample_object_ids[object_id] = inside_or_outside

        self._moller_init = self.read_double(file)
        self._triangle_color_x = self.read_double(file)
        self._triangle_color_y = self.read_double(file)
        self._triangle_color_z = self.read_double(file)

        self._elements = []
        for dummy in range(self._number_elements):
            element = Element()
            element.read(file)
            self._elements.append(element)

        self._chemical_name = self.read_str(file)

    def _modify(self, file):
        assert file.mode == 'r+b'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write", file.tell())

        tag_id = TAG_REGIONS_DATA
        if self.find_tag(file, tag_id):
            self.write_int(file, self._version)

            self.write_double(file, self._carrier_diffusion_length)

            self.write_int(file, self._number_elements)
            self.write_double(file, self.rho)

            self.write_double(file, self._work_function)
            self.write_double(file, self._average_plasmon_energy)
            self.write_int(file, self.id)
            self.write_int(file, self.substrate)
            self.write_int(file, self.user_density)
            self.write_int(file, self.user_composition)
            self.write_int(file, self._checked)

            self.write_str(file, self.name)

            self.write_int(file, self._number_sample_objects)

            for objectID in sorted(self._sample_object_ids.keys()):
                self.write_int(file, objectID)
                self.write_int(file, self._sample_object_ids[objectID])

            self.write_double(file, self._moller_init)
            self.write_double(file, self._triangle_color_x)
            self.write_double(file, self._triangle_color_y)
            self.write_double(file, self._triangle_color_z)

            for element in self._elements:
                element._modify(file)

            self.write_str(file, self._chemical_name)

    def write(self, file):
        raise NotImplementedError

    def modify_name(self, name):
        self.name = name
        if not self._file.closed:
            current_position = self._file.tell()
            self._file.close()
        else:
            current_position = 0

        self._file = open(self._file_pathname, 'r+b')

        self._file.seek(self._start_position)

        self._modify(self._file)

        self._file.close()
        self._file = open(self._file_pathname, 'rb')
        self._file.seek(current_position)

    def get_number_elements(self):
        assert len(self._elements) == self._number_elements
        return self._number_elements

    def remove_all_elements(self):
        self._number_elements = 0
        self._elements = []
        assert len(self._elements) == self._number_elements

    def add_element(self, symbol, weight_fraction=1.0, number_x_ray_layers=500):
        self._number_elements += 1
        element = Element()
        element.set_element(symbol, weight_fraction)
        self._elements.append(element)
        assert len(self._elements) == self._number_elements

    def get_element(self, index):
        return self._elements[index]

    def get_element_by_symbol(self, symbol):
        for element in self._elements:
            if element.get_symbol() == symbol:
                return element

    def update(self):
        self._number_elements = self._compute_number_elements()
        self.rho = self._compute_mean_mass_density_g_cm3()
        self.zmoy = self._compute_mean_atomic_number()
        self.name = self._generate_name()

        self._compute_atomic_fraction_elements()
        self._check_weight_fraction()
        self._check_atomic_fraction()

    def _compute_number_elements(self):
        return len(self._elements)

    def _compute_mean_mass_density_g_cm3(self):
        inverse_total = 0.0
        for element in self._elements:
            weight_fraction = element.get_weight_fraction()
            mass_density_g_cm3 = element.get_mass_density_g_cm3()

            inverse_total += weight_fraction / mass_density_g_cm3

        mean_mass_density = 1.0 / inverse_total
        return mean_mass_density

    def _compute_mean_atomic_number(self):
        total_z = 0.0
        total_elements = 0.0

        for element in self._elements:
            repetition = element.get_repetition()
            total_elements += repetition
            total_z += element.get_atomic_number() * repetition

        mean_atomic_number = total_z / total_elements
        return mean_atomic_number

    def _generate_name(self):
        name = ""
        for element in self._elements:
            name += element.get_symbol().strip()

        return name

    def _compute_atomic_fraction_elements(self):
        total = 0.0
        for element in self._elements:
            weight_fraction = element.get_weight_fraction()
            atomic_weight = element.get_atomic_weight_g_mol()

            total += weight_fraction / atomic_weight

        for element in self._elements:
            weight_fraction = element.get_weight_fraction()
            atomic_weight = element.get_atomic_weight_g_mol()

            atomic_fraction = (weight_fraction / atomic_weight) / total
            element.set_atomic_fraction(atomic_fraction)

    def _check_weight_fraction(self):
        weight_fractions = [element.get_weight_fraction() for element in self._elements]
        total = sum(weight_fractions)
        assert abs(total - 1.0) < EPSILON

        for element in self._elements:
            new_weight_fraction = decimal.Decimal(str(element.get_weight_fraction())) / decimal.Decimal(str(total))
            element.set_weight_fraction(float(new_weight_fraction))

        weight_fractions = [element.get_weight_fraction() for element in self._elements]
        total = sum(weight_fractions)
        assert abs(total - 1.0) < EPSILON * EPSILON

    def _check_atomic_fraction(self):
        atomic_fractions = [element.get_atomic_fraction() for element in self._elements]
        total = sum(atomic_fractions)
        assert abs(total - 1.0) < EPSILON

        for element in self._elements:
            new_atomic_fraction = decimal.Decimal(str(element.get_atomic_fraction())) / decimal.Decimal(str(total))
            element.set_atomic_fraction(float(new_atomic_fraction))

        atomic_fractions = [element.get_atomic_fraction() for element in self._elements]
        total = sum(atomic_fractions)
        assert abs(total - 1.0) < EPSILON * EPSILON

    def get_mean_mass_density_g_cm3(self):
        return self.rho

    def get_mean_atomic_number(self):
        return self.zmoy

    def get_name(self):
        return self.name

    def get_composition(self):
        return self._chemical_name

    def get_id(self):
        return self.id

    def export(self, export_file):
        # todo: implement the export method.
        logging.error("implement the export method.")
