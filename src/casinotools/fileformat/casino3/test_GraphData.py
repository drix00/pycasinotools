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
__svnId__ = "$Id: test_GraphData.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.GraphData as GraphData
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestGraphData(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
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

        values = results.getValues()
        self.assertAlmostEquals(1.0, values[0])
        self.assertAlmostEquals(0.0, values[-1])

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
