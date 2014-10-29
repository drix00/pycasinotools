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
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.Composition as Composition
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestComposition(test_File.TestFile):

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest

        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest

        f = open(self.filepathSim, 'rb')
        buf = BytesIO(f.read())
        buf.mode = 'rb'
        f.close()
        self._read_tests(buf)

    def _read_tests(self, file):
        file.seek(1889)
        composition = Composition.Composition()
        composition.read(file)

        self.assertEquals(0, composition.NuEl)
        self.assertAlmostEquals(7.981000000000E-01, composition.FWt)
        self.assertAlmostEquals(8.145442797934E-01, composition.FAt)
        self.assertAlmostEquals(0.0, composition.SigmaT)
        self.assertAlmostEquals(0.0, composition.SigmaTIne)
        self.assertEquals(1, composition.Rep)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
