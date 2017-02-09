#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.OptionsAdvBackSet as OptionsAdvBackSet
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestOptionsAdvBackSet(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        reader = OptionsAdvBackSet.OptionsAdvBackSet()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(False, reader.UseEnBack)
        self.assertAlmostEqual(10.0, reader.WorkDist)
        self.assertAlmostEqual(1.0, reader.DetectScaleX)
        self.assertAlmostEqual(1.0, reader.DetectScaleY)
        self.assertEqual(False, reader.ValidMatrix)

        self.assertAlmostEqual(0.0, reader.BEMin_Angle)
        self.assertAlmostEqual(0.0, reader.BEMax_Angle)
        self.assertAlmostEqual(0.0, reader.EFilterMax)
        self.assertAlmostEqual(0.0, reader.EFilterMin)

        for i in range(101):
            self.assertAlmostEqual(1.0, reader.EFilterVal[i])

        self.assertEqual(0, reader.FEFilter)

        reader = OptionsAdvBackSet.OptionsAdvBackSet()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(False, reader.UseEnBack)
        self.assertAlmostEqual(10.0, reader.WorkDist)
        self.assertAlmostEqual(1.0, reader.DetectScaleX)
        self.assertAlmostEqual(1.0, reader.DetectScaleY)
        self.assertEqual(False, reader.ValidMatrix)

        self.assertAlmostEqual(0.0, reader.BEMin_Angle)
        self.assertAlmostEqual(0.0, reader.BEMax_Angle)
        self.assertAlmostEqual(0.0, reader.EFilterMax)
        self.assertAlmostEqual(0.0, reader.EFilterMin)

        for i in range(101):
            self.assertAlmostEqual(1.0, reader.EFilterVal[i])

        self.assertEqual(0, reader.FEFilter)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
