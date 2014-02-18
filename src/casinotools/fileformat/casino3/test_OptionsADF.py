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
__svnId__ = "$Id: test_OptionsADF.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.OptionsADF as OptionsADF
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestOptionsADF(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        reader = OptionsADF.OptionsADF()
        file = open(self.filepathSim, 'rb')
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
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
