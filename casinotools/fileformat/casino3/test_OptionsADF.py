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
import casinotools.fileformat.casino3.OptionsADF as OptionsADF
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestOptionsADF(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        reader = OptionsADF.OptionsADF()
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertAlmostEquals(1.0, reader.DQE)
        self.assertEquals(1, reader.Enabled)
        self.assertEquals(0, reader.keepData)
        self.assertAlmostEquals(0.5, reader.MaxAngle)
        self.assertAlmostEquals(0.2, reader.MinAngle)
        self.assertEquals(0, reader.MaxPoints)

        reader = OptionsADF.OptionsADF()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertAlmostEquals(1.0, reader.DQE)
        self.assertEquals(1, reader.Enabled)
        self.assertEquals(0, reader.keepData)
        self.assertAlmostEquals(0.5, reader.MaxAngle)
        self.assertAlmostEquals(0.2, reader.MinAngle)
        self.assertEquals(0, reader.MaxPoints)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
