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

# Local modules.
import casinotools.fileformat.casino2.GraphData as GraphData
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestGraphData(test_File.TestFile):

    def NOtest_read(self):
        file = open(self.filepathCas, 'rb')
        file.seek(2013179)

        results = GraphData.GraphData(file)
        self.assertEquals(30105020, results._version)

        self.assertEquals(1000, results._size)
        self.assertAlmostEquals(0.0, results._borneInf)
        self.assertAlmostEquals(8.900000000000E+01, results._borneSup)
        self.assertEquals(0, results._isLog)
        self.assertEquals(0, results._isUneven)

        self.assertEquals("Z Max", results._title)
        self.assertEquals("Depth (nm)", results._xTitle)
        self.assertEquals("Hits (Normalized)", results._yTitle)

        self.assertAlmostEquals(1.0, results._values[0])
        self.assertAlmostEquals(0.0, results._values[-1])

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
