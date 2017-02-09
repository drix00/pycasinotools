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
import casinotools.fileformat.casino3.TransmittedAngles as TransmittedAngles
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestTransmittedAngles(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        file.seek(2012966)
        results = TransmittedAngles.TransmittedAngles()
        error = results.read(file)

        self.assertEqual(None, error)

        self.assertEqual(0, results._numberTransmittedElectrons)
        self.assertEqual(0, results._numberTransmittedDetectedElectrons)
        self.assertEqual(0, results._numberAngles)

        self.assertEqual(0, results._numberBinnedAngles)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
