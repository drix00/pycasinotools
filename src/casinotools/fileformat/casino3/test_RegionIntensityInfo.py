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
__svnId__ = "$Id: test_RegionIntensityInfo.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.RegionIntensityInfo as RegionIntensityInfo
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestRegionIntensityInfo(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        results = RegionIntensityInfo.RegionIntensityInfo()
        file = open(self.filepathCas, 'rb')
        file.seek(2012986)
        error = results.read(file)

        self.assertEquals(None, error)

        self.assertEquals(30105022, results._version)
        self.assertAlmostEquals(0.0, results._energyIntensity)
        self.assertEquals(1, results._regionID)
        self.assertAlmostEquals(0.0, results._normalizedEnergyIntensity)

        error = results.read(file)
        self.assertEquals(None, error)
        self.assertEquals(30105022, results._version)
        self.assertAlmostEquals(0.0, results._energyIntensity)
        self.assertEquals(2, results._regionID)
        self.assertAlmostEquals(0.0, results._normalizedEnergyIntensity)

        error = results.read(file)
        self.assertEquals(None, error)
        self.assertEquals(30105022, results._version)
        self.assertAlmostEquals(7.268071702406E+05, results._energyIntensity)
        self.assertEquals(3, results._regionID)
        self.assertAlmostEquals(7.268071702406E-01, results._normalizedEnergyIntensity)

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
