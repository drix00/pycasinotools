#!/usr/bin/env python
""" """

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

# Local modules.

# Project modules
from casinotools.analysis.casino3 import parameters

# Globals and constants variables.

class TestParameters(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_getThicknessFromFilename(self):
        thicknessRef_nm = 500

        filename = "Linescan_C_bG_Z500nm_T500nm"
        thickness_nm = parameters.getThicknessFromFilename(filename)
        self.assertEquals(thicknessRef_nm, int(thickness_nm))

        filename = "Linescan_C_bG_Z500nm_T500nm.sim"
        thickness_nm = parameters.getThicknessFromFilename(filename)
        self.assertEquals(thicknessRef_nm, int(thickness_nm))

        filename = "Linescan_C_bG_Z500nm.sim"
        self.assertRaises(ValueError, parameters.getThicknessFromFilename, filename)

        filename = "LinescanCbGZ500nmT500nm.sim"
        self.assertRaises(ValueError, parameters.getThicknessFromFilename, filename)

        filename = "Linescan-C-bG-Z500nm-T500nm.sim"
        self.assertRaises(ValueError, parameters.getThicknessFromFilename, filename)

        filename = "Linescan_C_bG_Z500nm_t500nm.sim"
        self.assertRaises(ValueError, parameters.getThicknessFromFilename, filename)

        filename = "Linescan_C_bG_Z500nm_T500NM.sim"
        self.assertRaises(ValueError, parameters.getThicknessFromFilename, filename)

        #self.fail("Test if the testcase is working.")

    def test_extractRepetitionId(self):
        text = "Id01X"
        valueRef = "01"
        value = parameters._extracRepetitionId(text)
        self.assertEquals(valueRef, value)

        text = "Id10X"
        valueRef = "10"
        value = parameters._extracRepetitionId(text)
        self.assertEquals(valueRef, value)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.main()
