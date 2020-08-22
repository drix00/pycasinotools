#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
import pytest

# Local modules.
import casinotools.file_format.casino3.sample_reader as SampleReader
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSampleReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.filepathCas = resource_filename(__name__, "../../../test_data/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()
        file = open(self.filepathSim, 'rb')
        reader = SampleReader.SampleReader()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)

        if is_bad_file(self.filepathCas):
            pytest.skip()
        file = open(self.filepathCas, 'rb')
        reader = SampleReader.SampleReader()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)

        #self.fail("Test if the testcase is working.")
