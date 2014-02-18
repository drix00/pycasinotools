#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 1755 $"
__svnDate__ = "$Date: 2010-01-20 17:06:10 -0500 (Wed, 20 Jan 2010) $"
__svnId__ = "$Id: test_Region.py 1755 2010-01-20 22:06:10Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import Region
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestRegion(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        file.seek(6560)
        region = Region.Region()
        region.read(file)

        self.assertEquals(30107003, region._version)
        self.assertAlmostEquals(50.0, region._carrierDiffusionLength)
        self.assertEquals(1, region._numberElements)
        self.assertAlmostEquals(2.33, region.Rho)
        self.assertAlmostEquals(-1.0, region._workFunction)
        self.assertAlmostEquals(-1.0, region._averagePlasmonEnergy)
        self.assertEquals(1, region.ID)
        self.assertEquals(0, region.Substrate)
        self.assertEquals(0, region.User_Density)
        self.assertEquals(0, region.User_Composition)
        self.assertEquals(0, region._checked)

        self.assertEquals("SiSubtrate", region.Name)

        self.assertEquals(1, region._numberSampleObjects)
        self.assertEquals(1, region._sampleObjectIDs[0])

        self.assertAlmostEquals(0.0, region._mollerInit)
        self.assertAlmostEquals(0.235, region._triangleColor_X)
        self.assertAlmostEquals(0.235, region._triangleColor_Y)
        self.assertAlmostEquals(1.0, region._triangleColor_Z)

        self.assertEquals("Si", region._chemicalName)

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
