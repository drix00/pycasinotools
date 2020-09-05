#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.composition
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, write_int, write_double

# Globals and constants variables.


class Composition:
    def __init__(self):
        self.NuEl = 0
        self.FWt = 1.0
        self.FAt = 1.0
        self.SigmaT = 0.0
        self.SigmaTIne = 0.0
        self.Rep = 1

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        self.NuEl = read_int(file)
        self.FWt = read_double(file)
        self.FAt = read_double(file)
        self.SigmaT = read_double(file)
        self.SigmaTIne = read_double(file)
        self.Rep = read_int(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        write_int(file, self.NuEl)
        write_double(file, self.FWt)
        write_double(file, self.FAt)
        write_double(file, self.SigmaT)
        write_double(file, self.SigmaTIne)
        write_int(file, self.Rep)

    def set_index(self, index):
        self.NuEl = index

    def set_weight_fraction(self, weight_fraction):
        self.FWt = weight_fraction

    def set_atomic_fraction(self, fraction):
        self.FAt = fraction
