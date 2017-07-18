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
import casinotools.fileformat.casino3.GraphData as GraphData
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestGraphData(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        file.seek(2013179)

        results = GraphData.GraphData(file)
        self.assertEqual(30105020, results._version)

        self.assertEqual(1000, results._size)
        self.assertAlmostEqual(0.0, results._borneInf)
        self.assertAlmostEqual(8.900000000000E+01, results._borneSup)
        self.assertEqual(0, results._isLog)
        self.assertEqual(0, results._isUneven)

        self.assertEqual("Z Max", results._title)
        self.assertEqual("Depth (nm)", results._xTitle)
        self.assertEqual("Hits (Normalized)", results._yTitle)

        values = results.getValues()
        self.assertAlmostEqual(1.0, values[0])
        self.assertAlmostEqual(0.0, values[-1])

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
