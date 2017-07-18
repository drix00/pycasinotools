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
import casinotools.fileformat.casino3.Region as Region
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestRegion(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        file.seek(6560)
        region = Region.Region()
        region.read(file)

        self.assertEqual(30107003, region._version)
        self.assertAlmostEqual(50.0, region._carrierDiffusionLength)
        self.assertEqual(1, region._numberElements)
        self.assertAlmostEqual(2.33, region.Rho)
        self.assertAlmostEqual(-1.0, region._workFunction)
        self.assertAlmostEqual(-1.0, region._averagePlasmonEnergy)
        self.assertEqual(1, region.ID)
        self.assertEqual(0, region.Substrate)
        self.assertEqual(0, region.User_Density)
        self.assertEqual(0, region.User_Composition)
        self.assertEqual(0, region._checked)

        self.assertEqual("SiSubtrate", region.Name)

        self.assertEqual(1, region._numberSampleObjects)
        self.assertEqual(1, region._sampleObjectIDs[0])

        self.assertAlmostEqual(0.0, region._mollerInit)
        self.assertAlmostEqual(0.235, region._triangleColor_X)
        self.assertAlmostEqual(0.235, region._triangleColor_Y)
        self.assertAlmostEqual(1.0, region._triangleColor_Z)

        self.assertEqual("Si", region._chemicalName)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
