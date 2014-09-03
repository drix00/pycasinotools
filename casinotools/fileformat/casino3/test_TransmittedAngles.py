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
import casinotools.fileformat.casino3.TransmittedAngles as TransmittedAngles
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestTransmittedAngles(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        results = TransmittedAngles.TransmittedAngles()
        file = open(self.filepathCas, 'rb')
        file.seek(2012966)
        error = results.read(file)

        self.assertEquals(None, error)

        self.assertEquals(0, results._numberTransmittedElectrons)
        self.assertEquals(0, results._numberTransmittedDetectedElectrons)
        self.assertEquals(0, results._numberAngles)

        self.assertEquals(0, results._numberBinnedAngles)

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
