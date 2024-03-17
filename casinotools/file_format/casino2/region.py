#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.region

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Region data from CASINO v2.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, read_long, read_str, \
    write_int, write_double, write_long, write_str
from casinotools.file_format.tags import add_tag_old, find_tag
from casinotools.file_format.casino2.element import Element

# Globals and constants variables.

# Third party modules.

# Local modules.

# Globals and constants variables.
decimal.getcontext().prec = 28
EPSILON = 1.0e-4

NB_PAR_MAX = 4

TAG_REGIONS_DATA = b"*REGIONSDATA%%%"


class Region:
    def __init__(self, number_xray_layers):
        self._number_xray_layers = number_xray_layers

        self.ID = None
        self.IDed = None
        self.NbEl = None
        self.Rho = None
        self.Zmoy = None

        self.Parametre = []

        self.Forme = None
        self.Substrate = None
        self.color = None
        self.cindex = None
        self.User_Density = None
        self.User_Composition = None

        self._elements = []

        self.NbEl = None
        self.Rho = None
        self.Zmoy = None
        self.Name = None

    def read(self, file, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = TAG_REGIONS_DATA
        find_tag(file, tag_id)

        self.ID = read_int(file)
        self.IDed = read_int(file)
        self.NbEl = read_int(file)
        self.Rho = read_double(file)
        self.Zmoy = read_double(file)

        self.Parametre = []
        for dummy in range(NB_PAR_MAX):
            value = read_double(file)
            self.Parametre.append(value)

        self.Forme = read_int(file)
        self.Substrate = read_int(file)
        self.color = read_long(file)
        self.cindex = read_int(file)
        self.User_Density = read_int(file)
        self.User_Composition = read_int(file)

        self.Name = read_str(file)

        self._elements = []
        for dummy in range(self.NbEl):
            element = Element()
            element.read(file, self._number_xray_layers, version)
            self._elements.append(element)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_REGIONS_DATA
        add_tag_old(file, tag_id)
        write_int(file, self.ID)
        write_int(file, self.IDed)
        write_int(file, self.NbEl)
        write_double(file, self.Rho)
        write_double(file, self.Zmoy)

        assert len(self.Parametre) == NB_PAR_MAX
        for index in range(NB_PAR_MAX):
            value = self.Parametre[index]
            write_double(file, value)

        write_int(file, self.Forme)
        write_int(file, self.Substrate)
        write_long(file, self.color)
        write_int(file, self.cindex)
        write_int(file, self.User_Density)
        write_int(file, self.User_Composition)

        write_str(file, self.Name)

        assert len(self._elements) == self.NbEl
        for index in range(self.NbEl):
            element = self._elements[index]
            element.write(file, self._number_xray_layers)

    def get_number_elements(self):
        assert len(self._elements) == self.NbEl
        return self.NbEl

    def remove_all_elements(self):
        self.NbEl = 0
        self._elements = []
        assert len(self._elements) == self.NbEl

    def add_element(self, symbol, weight_fraction=1.0, number_xray_layers=500):
        self.NbEl += 1
        element = Element(number_xray_layers)
        element.set_element(symbol, weight_fraction)
        self._elements.append(element)
        assert len(self._elements) == self.NbEl

    def get_element(self, index):
        return self._elements[index]

    def get_elements(self):
        return self._elements

    def set_element(self, element_symbol, weight_fraction=1.0, number_xray_layers=500, index_element=0):
        element = Element(number_xray_layers)
        element.set_element(element_symbol, weight_fraction)
        self._elements[index_element] = element
        assert len(self._elements) == self.NbEl
        self.update()

    def get_element_by_symbol(self, symbol):
        for element in self._elements:
            if element.get_symbol() == symbol:
                return element

    def update(self):
        self.NbEl = self._compute_number_elements()
        self.Rho = self._compute_mean_mass_density_g_cm3()
        self.Zmoy = self._compute_mean_atomic_number()
        self.Name = self._generate_name()

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
        total__elements = 0.0

        for element in self._elements:
            repetition = element.get_repetition()
            total__elements += repetition
            total_z += element.get_atomic_number() * repetition

        mean_atomic_number = total_z / total__elements
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
        return self.Rho

    def get_mean_atomic_number(self):
        return self.Zmoy

    def get_name(self):
        return self.Name

    def is_user_mass_density(self):
        return bool(self.User_Density)

    def get_parameters(self):
        return self.Parametre

    def set_parameters(self, parameters):
        self.Parametre = parameters
