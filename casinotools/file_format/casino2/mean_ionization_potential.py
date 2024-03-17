#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.mean_ionization_potential
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
from math import pow

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
MODEL_JOY = 0
MODEL_BERGER = 1
MODEL_PH = 2


class MeanIonizationPotential:
    def __init__(self, model=MODEL_JOY):
        if model == MODEL_JOY:
            self._compute = _compute_joy
        elif model == MODEL_BERGER:
            self._compute = _compute_berger
        elif model == MODEL_PH:
            self._compute = _compute_ph

    def compute_j(self, atomic_number):
        return self._compute(atomic_number)


def _compute_joy(atomic_number):
    z = float(atomic_number)
    if atomic_number < 13:
        j = 11.5 * z * 1e-3
    else:
        j = 0.00976 * z + 0.0588 / pow(z, 0.19)

    return j


def _compute_berger(atomic_number):
    z = float(atomic_number)
    j = 0.00976 * z + 0.0588 / pow(z, 0.19)
    return j


def _compute_ph(atomic_number):
    z = float(atomic_number)
    if atomic_number <= 20:
        j = 14.858 + 15.4 * z - 2.9276 * pow(z, 2) + 0.5348 * pow(z, 3) - 0.03563 * pow(z, 4) + \
            7.7733e-4 * pow(z, 5)
    else:
        j = -2034.18 + 35.576 * z - 0.1142 * pow(z, 2) + 63824.348 / z - 658308.68 / (z * z)

    return j * 1e-3
