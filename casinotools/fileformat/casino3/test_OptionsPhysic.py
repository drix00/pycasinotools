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
import casinotools.fileformat.casino3.OptionsPhysic as OptionsPhysic
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestOptionsPhysic(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        reader = OptionsPhysic.OptionsPhysic()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(3, reader.FRan)
        self.assertEqual(1, reader.FDeds)
        self.assertEqual(5, reader.FTotalCross)
        self.assertEqual(5, reader.FPartialCross)
        self.assertEqual(1, reader.FCosDirect)
        self.assertEqual(3, reader.FSecIon)
        self.assertEqual(0, reader.FPotMoy)

        self.assertEqual(10, reader.max_secondary_order)
        self.assertAlmostEqual(0.05, reader.Min_Energy_Nosec)
        self.assertAlmostEqual(0.0004, reader.Residual_Energy_Loss)
        self.assertAlmostEqual(-1, reader.Min_Energy_With_Sec)
        self.assertAlmostEqual(-1, reader.Min_Gen_Secondary_Energy)

        reader = OptionsPhysic.OptionsPhysic()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(3, reader.FRan)
        self.assertEqual(1, reader.FDeds)
        self.assertEqual(5, reader.FTotalCross)
        self.assertEqual(5, reader.FPartialCross)
        self.assertEqual(1, reader.FCosDirect)
        self.assertEqual(3, reader.FSecIon)
        self.assertEqual(0, reader.FPotMoy)

        self.assertEqual(10, reader.max_secondary_order)
        self.assertAlmostEqual(0.05, reader.Min_Energy_Nosec)
        self.assertAlmostEqual(0.0004, reader.Residual_Energy_Loss)
        self.assertAlmostEqual(-1, reader.Min_Energy_With_Sec)
        self.assertAlmostEqual(-1, reader.Min_Gen_Secondary_Energy)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
