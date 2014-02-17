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
__svnId__ = "$Id: test_ScanPointPositions.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.ScanPointPositions as ScanPointPositions
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestScanPointPositions(test_FileReaderWriterTools.TestFileReaderWriterTools):
    def test_read(self):
        reader = ScanPointPositions.ScanPointPositions()
        file = open(self.filepathSim, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(5, reader.getNumberPoints())

        reader = ScanPointPositions.ScanPointPositions()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(5, reader.getNumberPoints())

        positionsRef = []
        positionsRef.append((0.0, 0.0, 0.0))
        positionsRef.append((40.0, 0.0, 0.0))
        positionsRef.append((45.0, 0.0, 0.0))
        positionsRef.append((50.0, 0.0, 0.0))
        positionsRef.append((100.0, 0.0, 0.0))

        for point, pointRef in zip(reader.getPositions(), positionsRef):
            for i in xrange(3):
                self.assertAlmostEquals(pointRef[i], point[i])

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
