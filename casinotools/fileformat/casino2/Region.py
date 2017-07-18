#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.Region

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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.Element as Element

# Globals and constants variables.
decimal.getcontext().prec = 28
EPSILON = 1.0e-4

NB_PAR_MAX = 4

TAG_REGIONS_DATA = b"*REGIONSDATA%%%"


class Region(FileReaderWriterTools.FileReaderWriterTools):
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
        self.findTag(file, tag_id)

        self.ID = self.readInt(file)
        self.IDed = self.readInt(file)
        self.NbEl = self.readInt(file)
        self.Rho = self.readDouble(file)
        self.Zmoy = self.readDouble(file)

        self.Parametre = []
        for dummy in range(NB_PAR_MAX):
            value = self.readDouble(file)
            self.Parametre.append(value)

        self.Forme = self.readInt(file)
        self.Substrate = self.readInt(file)
        self.color = self.readLong(file)
        self.cindex = self.readInt(file)
        self.User_Density = self.readInt(file)
        self.User_Composition = self.readInt(file)

        self.Name = self.readStr(file)

        self._elements = []
        for dummy in range(self.NbEl):
            element = Element.Element()
            element.read(file, self._number_xray_layers, version)
            self._elements.append(element)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_REGIONS_DATA
        self.addTagOld(file, tag_id)
        self.writeInt(file, self.ID)
        self.writeInt(file, self.IDed)
        self.writeInt(file, self.NbEl)
        self.writeDouble(file, self.Rho)
        self.writeDouble(file, self.Zmoy)

        assert len(self.Parametre) == NB_PAR_MAX
        for index in range(NB_PAR_MAX):
            value = self.Parametre[index]
            self.writeDouble(file, value)

        self.writeInt(file, self.Forme)
        self.writeInt(file, self.Substrate)
        self.writeLong(file, self.color)
        self.writeInt(file, self.cindex)
        self.writeInt(file, self.User_Density)
        self.writeInt(file, self.User_Composition)

        self.writeStr(file, self.Name)

        assert len(self._elements) == self.NbEl
        for index in range(self.NbEl):
            element = self._elements[index]
            element.write(file, self._number_xray_layers)

    def getNumberElements(self):
        assert len(self._elements) == self.NbEl
        return self.NbEl

    def removeAllElements(self):
        self.NbEl = 0
        self._elements = []
        assert len(self._elements) == self.NbEl

    def addElement(self, symbol, weight_fraction=1.0, number_xray_layers=500):
        self.NbEl += 1
        element = Element.Element(number_xray_layers)
        element.setElement(symbol, weight_fraction)
        self._elements.append(element)
        assert len(self._elements) == self.NbEl

    def getElement(self, index):
        return self._elements[index]

    def getElements(self):
        return self._elements

    def setElement(self, element_symbol, weight_fraction=1.0, number_xray_layers=500, index_element=0):
        element = Element.Element(number_xray_layers)
        element.setElement(element_symbol, weight_fraction)
        self._elements[index_element] = element
        assert len(self._elements) == self.NbEl
        self.update()

    def getElementBySymbol(self, symbol):
        for element in self._elements:
            if element.getSymbol() == symbol:
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
            weight_fraction = element.getWeightFraction()
            mass_density_g_cm3 = element.getMassDensity_g_cm3()

            inverse_total += weight_fraction / mass_density_g_cm3

        mean_mass_density = 1.0 / inverse_total
        return mean_mass_density

    def _compute_mean_atomic_number(self):
        total_z = 0.0
        total__elements = 0.0

        for element in self._elements:
            repetition = element.getRepetition()
            total__elements += repetition
            total_z += element.getAtomicNumber() * repetition

        mean_atomic_number = total_z / total__elements
        return mean_atomic_number

    def _generate_name(self):
        name = ""
        for element in self._elements:
            name += element.getSymbol().strip()

        return name

    def _compute_atomic_fraction_elements(self):
        total = 0.0
        for element in self._elements:
            weight_fraction = element.getWeightFraction()
            atomic_weight = element.getAtomicWeight_g_mol()

            total += weight_fraction / atomic_weight

        for element in self._elements:
            weight_fraction = element.getWeightFraction()
            atomic_weight = element.getAtomicWeight_g_mol()

            atomic_fraction = (weight_fraction / atomic_weight) / total
            element.setAtomicFraction(atomic_fraction)

    def _check_weight_fraction(self):
        weight_fractions = [element.getWeightFraction() for element in self._elements]
        total = sum(weight_fractions)
        assert abs(total - 1.0) < EPSILON

        for element in self._elements:
            new_weight_fraction = decimal.Decimal(str(element.getWeightFraction())) / decimal.Decimal(str(total))
            element.setWeightFraction(float(new_weight_fraction))

        weight_fractions = [element.getWeightFraction() for element in self._elements]
        total = sum(weight_fractions)
        assert abs(total - 1.0) < EPSILON * EPSILON

    def _check_atomic_fraction(self):
        atomic_fractions = [element.getAtomicFraction() for element in self._elements]
        total = sum(atomic_fractions)
        assert abs(total - 1.0) < EPSILON

        for element in self._elements:
            new_atomic_fraction = decimal.Decimal(str(element.getAtomicFraction())) / decimal.Decimal(str(total))
            element.setAtomicFraction(float(new_atomic_fraction))

        atomic_fractions = [element.getAtomicFraction() for element in self._elements]
        total = sum(atomic_fractions)
        assert abs(total - 1.0) < EPSILON * EPSILON

    def getMeanMassDensity_g_cm3(self):
        return self.Rho

    def getMeanAtomicNumber(self):
        return self.Zmoy

    def getName(self):
        return self.Name

    def isUserMassDensity(self):
        return bool(self.User_Density)

    def getParameters(self):
        return self.Parametre

    def setParameters(self, parameters):
        self.Parametre = parameters

