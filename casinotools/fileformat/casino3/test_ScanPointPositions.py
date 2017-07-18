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
import casinotools.fileformat.casino3.ScanPointPositions as ScanPointPositions
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestScanPointPositions(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        reader = ScanPointPositions.ScanPointPositions()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(5, reader.getNumberPoints())

        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        reader = ScanPointPositions.ScanPointPositions()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(5, reader.getNumberPoints())

        positionsRef = []
        positionsRef.append((0.0, 0.0, 0.0))
        positionsRef.append((40.0, 0.0, 0.0))
        positionsRef.append((45.0, 0.0, 0.0))
        positionsRef.append((50.0, 0.0, 0.0))
        positionsRef.append((100.0, 0.0, 0.0))

        for point, pointRef in zip(reader.getPositions(), positionsRef):
            for i in range(3):
                self.assertAlmostEqual(pointRef[i], point[i])

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
