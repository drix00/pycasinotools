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
__svnId__ = "$Id: test_ScatteringEvent.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
import unittest
import logging
from StringIO import StringIO

# Third party modules.

# Local modules.
import ScatteringEvent
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestScatteringEvent(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathCas, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathCas, 'rb')
        file = StringIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(196552)
        event = ScatteringEvent.ScatteringEvent()
        event.read(file)

        self.assertAlmostEquals(-2.903983831406E+00, event.X)
        self.assertAlmostEquals(-3.020418643951E+00, event.Y)
        self.assertAlmostEquals(0.0, event.Z)
        self.assertAlmostEquals(4.000000000000E+00, event.E)
        self.assertEquals(0, event.Intersect)
        self.assertEquals(0, event.id)

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
