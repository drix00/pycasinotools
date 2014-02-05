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
__svnId__ = "$Id: test_TrajectoriesData.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
import unittest
import logging
from StringIO import StringIO

# Third party modules.

# Local modules.
import TrajectoriesData
import casinoTools.FileFormat.casino2.test_File as test_File

# Globals and constants variables.

class TestTrajectoriesData(test_File.TestFile):

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
        file.seek(0)
        trajectoriesData = TrajectoriesData.TrajectoriesData()
        trajectoriesData.read(file)

        file.seek(98348)
        trajectoriesData = TrajectoriesData.TrajectoriesData()
        trajectoriesData.read(file)
        self.assertEquals(221, trajectoriesData._numberTrajectories)

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
