#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.OptionsDist as OptionsDist
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestOptionsDist(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        reader = OptionsDist.OptionsDist()
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertAlmostEquals(1.0, reader.DenrMax / OptionsDist.autoFlag)

        self.assertAlmostEquals(1000.0, reader.DEposCyl_Z)
        self.assertEquals(0, reader.DEposCyl_Z_Log)
        self.assertEquals(OptionsDist.DIST_DEPOS_POSITION_ABSOLUTE, reader.DEpos_Position)

        reader = OptionsDist.OptionsDist()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertAlmostEquals(1.0, reader.DenrMax / OptionsDist.autoFlag)

        self.assertAlmostEquals(1000.0, reader.DEposCyl_Z)
        self.assertEquals(0, reader.DEposCyl_Z_Log)
        self.assertEquals(OptionsDist.DIST_DEPOS_POSITION_ABSOLUTE, reader.DEpos_Position)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
