#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2620 $"
__svnDate__ = "$Date: 2011-12-07 11:01:42 -0500 (Wed, 07 Dec 2011) $"
__svnId__ = "$Id: test_ElementIntensity.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.

# Local modules.
import casinotools.fileformat.casino2.ElementIntensity as ElementIntensity
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestElementIntensity(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathCas, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathCas, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(696872)
        element = ElementIntensity.ElementIntensity()
        element.read(file)

        self.assertEquals("B", element.Name)
        self.assertAlmostEquals(3.444919288026E+02, element.IntensityK[0])

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
