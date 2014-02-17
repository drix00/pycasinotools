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
__svnId__ = "$Id: test_Composition.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
import unittest
import logging
from StringIO import StringIO

# Third party modules.

# Local modules.
import Composition
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestComposition(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathSim, 'rb')
        buf = StringIO(f.read())
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

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
