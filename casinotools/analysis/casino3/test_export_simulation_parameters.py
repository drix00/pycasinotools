#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import unittest
import os

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
from casinotools.analysis.casino3 import export_simulation_parameters

# Globals and constants variables.

class TestExportSimulationParameters(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        basepath = os.path.dirname(__file__)
        path = os.path.join(basepath, "../../../testdata/analysis/casino3/ExportParameters")
        path = os.path.normpath(path)

        filename = "ProblemSampleRotation_fz0nm_t0deg.sim"
        self._filepath = os.path.join(path, filename)
        if not os.path.isfile(self._filepath):
            raise SkipTest

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        exportFilepath = export_simulation_parameters._getExportFilepath(self._filepath)
        if os.path.isfile(exportFilepath):
            os.remove(exportFilepath)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_setUp(self):
        if not os.path.isfile(self._filepath):
            raise SkipTest
        self.assertTrue(os.path.isfile(self._filepath))

        #self.fail("Test if the testcase is working.")

    def test_export(self):
        exportParameters = export_simulation_parameters.ExportSimulationParameters()

        exportParameters.export(self._filepath)

        exportFilepath = export_simulation_parameters._getExportFilepath(self._filepath)
        self.assertTrue(os.path.isfile(exportFilepath))

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.main()
