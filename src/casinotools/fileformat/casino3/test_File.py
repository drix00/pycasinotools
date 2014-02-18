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
__svnId__ = "$Id: test_File.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.File as File
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestFile(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_init(self):
        casinoFile = File.File(self.filepathSim)

        self.assertEquals(self.filepathSim, casinoFile.getFilepath())

        #self.fail("Test if the testcase is working.")

    def test_getFileType(self):
        casinoFile = File.File(self.filepathSim)
        type = casinoFile.getFileType()
        self.assertEquals(File.SIMULATION_CONFIGURATIONS, type)

#        casinoFile = File.File(self.filepathCas)
#        type = casinoFile.getFileType()
#        self.assertEquals(File.SIMULATION_RESULTS, type)

        #self.fail("Test if the testcase is working.")

    def test__readExtension(self):
        casinoFile = File.File(self.filepathSim)
        file = casinoFile._open(self.filepathSim)
        extension = casinoFile._readExtension(file)
        self.assertEquals(File.SIMULATION_CONFIGURATIONS, extension)

        file = open(self.filepathCas, 'r')
        extension = casinoFile._readExtension(file)
        self.assertEquals(File.SIMULATION_RESULTS, extension)

        #self.fail("Test if the testcase is working.")

    def test__readVersion(self):
        casinoFile = File.File(self.filepathSim)
        file = casinoFile._open(self.filepathSim)
        version = casinoFile._readVersion(file)
        self.assertEquals(30107002, version)

        #self.fail("Test if the testcase is working.")

    def test_open(self):
        casinoFile = File.File(self.filepathSim)
        casinoFile.open()

        self.assertEquals(30107002, casinoFile._version)
        self.assertEquals(1, casinoFile._numberSimulations)

        #self.fail("Test if the testcase is working.")

    def testReadCasFile(self):
        casinoFile = File.File(self.filepathCas)
        casinoFile.open()

        self.assertEquals(30107002, casinoFile._version)
        self.assertEquals(1, casinoFile._numberSimulations)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
