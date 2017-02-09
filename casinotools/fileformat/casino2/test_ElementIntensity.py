#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.ElementIntensity as ElementIntensity
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestElementIntensity(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest

        with open(self.filepathCas, 'rb') as casinoFile:
            self._read_tests(casinoFile)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest

        f = open(self.filepathCas, 'rb')
        casinoFile = BytesIO(f.read())
        casinoFile.mode = 'rb'
        f.close()
        self._read_tests(casinoFile)

    def _read_tests(self, casinoFile):
        casinoFile.seek(696872)
        element = ElementIntensity.ElementIntensity()
        element.read(casinoFile)

        self.assertEqual("B", element.Name)
        self.assertAlmostEqual(3.444919288026E+02, element.IntensityK[0])

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
