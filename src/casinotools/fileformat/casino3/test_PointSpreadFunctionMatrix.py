#!/usr/bin/env python
"""
.. py:currentmodule:: FileFormat.casino3.test_PointSpreadFunctionMatrix
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the PointSpreadFunctionMatrix module.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.attrib import attr

# Local modules.

# Project modules
import PointSpreadFunctionMatrix
import casinotools.fileformat.casino3.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.File as File
import casinotools.fileformat.casino3.Version as Version

# Globals and constants variables.

class TestPointSpreadFunctionMatrix(unittest.TestCase):
    """
    TestCase class for the module `moduleName`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    @attr('ignore')
    def test_SimNoPsfs(self):
        """
        Tests for method `SimNoPsfs`.
        """

        filepath = resource_filename(__name__, "../../testData/casino3.x/PSFs/SiN_woPSFs_bG_T200nm.sim")

        casinoFile = File.File(filepath)

        versionRef = Version.SIM_OPTIONS_VERSION_3_3_0_0
        versionStrRef = "3.3.0.0"

        version = casinoFile.getVersion()
        self.assertEquals(versionRef, version)

        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        optionsAdvancedPsfsSettings = casinoFile.getOptions().getOptionsAdvancedPsfsSettings()

        self.assertEqual(False, optionsAdvancedPsfsSettings.isGeneratingPSFs())

        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_SimPsfs(self):
        """
        Tests for method `SimNoPsfs`.
        """
        filenames = ["SiN_wPSFs_bG_T200nm.sim", "SiN_wPSFs_wConserveData_bG_T200nm.sim"]
        for filename in filenames:
            filepath = resource_filename(__name__, "../../testData/casino3.x/PSFs/" + filename)

            casinoFile = File.File(filepath)

            versionRef = Version.SIM_OPTIONS_VERSION_3_3_0_0
            versionStrRef = "3.3.0.0"

            version = casinoFile.getVersion()
            self.assertEquals(versionRef, version)

            versionStr = casinoFile._extractVersionString(version)
            self.assertEquals(versionStrRef, versionStr)

            optionsAdvancedPsfsSettings = casinoFile.getOptions().getOptionsAdvancedPsfsSettings()

            self.assertEqual(True, optionsAdvancedPsfsSettings.isGeneratingPSFs())

        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_CasNoPsfs(self):
        """
        Tests for method `SimNoPsfs`.
        """

        filepath = resource_filename(__name__, "../../testData/casino3.x/PSFs/SiN_woPSFs_bG_T200nm.cas")

        casinoFile = File.File(filepath)

        versionRef = Version.SIM_OPTIONS_VERSION_3_3_0_0
        versionStrRef = "3.3.0.0"

        version = casinoFile.getVersion()
        self.assertEquals(versionRef, version)

        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        optionsAdvancedPsfsSettings = casinoFile.getOptions().getOptionsAdvancedPsfsSettings()
        self.assertEqual(False, optionsAdvancedPsfsSettings.isGeneratingPSFs())

        scanPointResults = casinoFile.getScanPointResults()
        self.assertEqual(False, scanPointResults[0].isPsfs())
        self.assertEqual(None, scanPointResults[0].getPointSpreadFunctionMatrix())

        #self.fail("Test if the testcase is working.")

    @attr('ignore')
    def test_CasPsfs(self):
        """
        Tests for method `SimNoPsfs`.
        """

        filename = "SiN_wPSFs_bG_T200nm.cas"
        filepath = resource_filename(__name__, "../../testData/casino3.x/PSFs/" + filename)

        casinoFile = File.File(filepath)

        versionRef = Version.SIM_OPTIONS_VERSION_3_3_0_0
        versionStrRef = "3.3.0.0"

        version = casinoFile.getVersion()
        self.assertEquals(versionRef, version)

        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        optionsAdvancedPsfsSettings = casinoFile.getOptions().getOptionsAdvancedPsfsSettings()

        self.assertEqual(True, optionsAdvancedPsfsSettings.isGeneratingPSFs())

        scanPointResults = casinoFile.getScanPointResults()
        self.assertEqual(False, scanPointResults[0].isPsfs())
        self.assertEqual(None, scanPointResults[0].getPointSpreadFunctionMatrix())

        filename = "SiN_wPSFs_wConserveData_bG_T200nm.cas"
        filepath = resource_filename(__name__, "../../testData/casino3.x/PSFs/" + filename)

        casinoFile = File.File(filepath)

        versionRef = Version.SIM_OPTIONS_VERSION_3_3_0_0
        versionStrRef = "3.3.0.0"

        version = casinoFile.getVersion()
        self.assertEquals(versionRef, version)

        versionStr = casinoFile._extractVersionString(version)
        self.assertEquals(versionStrRef, versionStr)

        optionsAdvancedPsfsSettings = casinoFile.getOptions().getOptionsAdvancedPsfsSettings()

        self.assertEqual(True, optionsAdvancedPsfsSettings.isGeneratingPSFs())

        scanPointResults = casinoFile.getScanPointResults()
        self.assertEqual(True, scanPointResults[0].isPsfs())
        self.assertIsInstance(scanPointResults[0].getPointSpreadFunctionMatrix(), PointSpreadFunctionMatrix.PointSpreadFunctionMatrix)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
