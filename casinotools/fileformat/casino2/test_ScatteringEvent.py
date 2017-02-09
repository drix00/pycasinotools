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
import casinotools.fileformat.casino2.ScatteringEvent as ScatteringEvent
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestScatteringEvent(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        with open(self.filepathCas, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        f = open(self.filepathCas, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(196552)
        event = ScatteringEvent.ScatteringEvent()
        event.read(file)

        self.assertAlmostEqual(-2.903983831406E+00, event.X)
        self.assertAlmostEqual(-3.020418643951E+00, event.Y)
        self.assertAlmostEqual(0.0, event.Z)
        self.assertAlmostEqual(4.000000000000E+00, event.E)
        self.assertEqual(0, event.Intersect)
        self.assertEqual(0, event.id)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
