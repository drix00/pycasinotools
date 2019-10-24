#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.test_Region

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.fileformat.casino2.Region`.
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
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
import pytest

# Local modules.
import casinotools.fileformat.casino2.Region as Region
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


class TestRegion(test_File.TestFile):
    """
    TestCase class for the module `casinotools.fileformat.casino2.Region`.
    """

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file, self.version_2_45)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            pytest.skip
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file, self.version_2_45)

    def _read_tests(self, file, version):
        file.seek(0)
        region = Region.Region(500)
        region.read(file, version)

        self.assertEqual(0, region.ID)
        self.assertEqual("BC", region.Name)
