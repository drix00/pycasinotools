#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
from io import BytesIO

# Third party modules.
import pytest

# Local modules.
import casinotools.fileformat.casino2.Composition as Composition
import tests.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

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
