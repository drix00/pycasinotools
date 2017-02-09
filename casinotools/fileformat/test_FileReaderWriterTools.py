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
import shutil

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.File as File
from casinotools.utilities.path import create_path, get_current_module_path
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestFileReaderWriterTools(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathSim = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.filepathSim_3202 = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points_3202.sim")
        self.filepathCas = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")

        path = get_current_module_path(__file__, "../../test_data/temp")
        self.temporaryDir = create_path(path)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.temporaryDir, ignore_errors=True)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_checkAndCorrectValueSize(self):
        valueRef = "WinCasino Simulation File"
        size = 26
        value = FileReaderWriterTools.FileReaderWriterTools()._checkAndCorrectValueSize(valueRef, size)
        self.assertEqual(valueRef, value)

        size = 6
        value = FileReaderWriterTools.FileReaderWriterTools()._checkAndCorrectValueSize(valueRef, size)
        self.assertNotEquals(valueRef, value)
        self.assertEqual(valueRef[:size], value)

        #self.fail("Test if the testcase is working.")

    def test_extractVersionString(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        casinoFile = File.File(self.filepathSim)

        version = File.V30103040
        versionStrRef = "3.1.3.40"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEqual(versionStrRef, versionStr)

        version = File.V30103070
        versionStrRef = "3.1.3.70"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEqual(versionStrRef, versionStr)

        version = File.V30104060
        versionStrRef = "3.1.4.60"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEqual(versionStrRef, versionStr)

        version = File.V30107002
        versionStrRef = "3.1.7.2"
        versionStr = casinoFile._extractVersionString(version)
        self.assertEqual(versionStrRef, versionStr)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
