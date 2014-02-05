#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2378 $"
__svnDate__ = "$Date: 2011-06-20 15:45:48 -0400 (Mon, 20 Jun 2011) $"
__svnId__ = "$Id: test_SampleReader.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import casinoTools.FileFormat.casino3.SampleReader as SampleReader
import DrixUtilities.Files as Files
from DrixUtilities.Testings import ignore

# Globals and constants variables.

class TestSampleReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = Files.getCurrentModulePath(__file__, "../../testData/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.filepathCas = Files.getCurrentModulePath(__file__, "../../testData/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    @ignore()
    def test_read(self):
        reader = SampleReader.SampleReader()
        file = open(self.filepathSim, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)

        reader = SampleReader.SampleReader()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
