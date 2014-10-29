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
import os.path

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.SampleReader as SampleReader

# Globals and constants variables.

class TestSampleReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../../testData/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.filepathCas = resource_filename(__name__, "../../../testData/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        reader = SampleReader.SampleReader()
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)

        if not os.path.isfile(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        reader = SampleReader.SampleReader()
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
