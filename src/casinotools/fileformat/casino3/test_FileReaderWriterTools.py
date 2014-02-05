#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2467 $"
__svnDate__ = "$Date: 2011-09-08 16:41:24 -0400 (Thu, 08 Sep 2011) $"
__svnId__ = "$Id: test_FileReaderWriterTools.py 2467 2011-09-08 20:41:24Z hdemers $"

# Standard library modules.
import unittest

# Third party modules.

# Local modules.
import casinoTools.FileFormat.casino3.FileReaderWriterTools as FileReaderWriterTools
import casinoTools.FileFormat.casino3.File as File
import DrixUtilities.Files as Files
from DrixUtilities.Testings import ignore

# Globals and constants variables.

class TestFileReaderWriterTools(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = Files.getCurrentModulePath(__file__, "../../testData/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.filepathSim_3202 = Files.getCurrentModulePath(__file__, "../../testData/casino3.x/SiSubstrateThreeLines_Points_3202.sim")
        self.filepathCas = Files.getCurrentModulePath(__file__, "../../testData/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_checkAndCorrectValueSize(self):
        valueRef = "WinCasino Simulation File"
        size = 26
        value = FileReaderWriterTools.FileReaderWriterTools()._checkAndCorrectValueSize(valueRef, size)
        self.assertEquals(valueRef, value)

        size = 6
        value = FileReaderWriterTools.FileReaderWriterTools()._checkAndCorrectValueSize(valueRef, size)
        self.assertNotEquals(valueRef, value)
        self.assertEquals(valueRef[:size], value)

        #self.fail("Test if the testcase is working.")

    @ignore()
    def test_extractVersionString(self):
        casinoFile = File.File(self.filepathSim)

        version = File.V30103040
        versionStrRef = "3.1.3.40"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        version = File.V30103070
        versionStrRef = "3.1.3.70"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        version = File.V30104060
        versionStrRef = "3.1.4.60"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        version = File.V30107002
        versionStrRef = "3.1.7.2"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':    #pragma: no cover
    #logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
