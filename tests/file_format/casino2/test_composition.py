#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_composition
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.composition` module.
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
from io import BytesIO

# Third party modules.
import pytest

# Local modules.

# Project modules.
import casinotools.file_format.casino2.composition as Composition
import tests.file_format.casino2.test_file as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


class TestComposition(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()

        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()

        f = open(self.filepathSim, 'rb')
        buf = BytesIO(f.read())
        buf.mode = 'rb'
        f.close()
        self._read_tests(buf)

    def _read_tests(self, file):
        file.seek(1889)
        composition = Composition.Composition()
        composition.read(file)

        self.assertEqual(0, composition.NuEl)
        self.assertAlmostEqual(7.981000000000E-01, composition.FWt)
        self.assertAlmostEqual(8.145442797934E-01, composition.FAt)
        self.assertAlmostEqual(0.0, composition.SigmaT)
        self.assertAlmostEqual(0.0, composition.SigmaTIne)
        self.assertEqual(1, composition.Rep)
