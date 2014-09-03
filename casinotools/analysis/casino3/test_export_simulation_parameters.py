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

# Local modules.
from casinotools.analysis.casino3 import export_simulation_parameters
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestExportSimulationParameters(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        path = Files.getCurrentModulePath(__file__, "../../../testdata/analysis/casino3/ExportParameters")
        filename = "ProblemSampleRotation_fz0nm_t0deg.sim"
        self._filepath = os.path.join(path, filename)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        exportFilepath = export_simulation_parameters._getExportFilepath(self._filepath)
        if os.path.isfile(exportFilepath):
            os.remove(exportFilepath)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_setUp(self):
        self.assertTrue(os.path.isfile(self._filepath))
        #self.fail("Test if the testcase is working.")

    def test_export(self):
        exportParameters = export_simulation_parameters.ExportSimulationParameters()

        exportParameters.export(self._filepath)

        exportFilepath = export_simulation_parameters._getExportFilepath(self._filepath)
        self.assertTrue(os.path.isfile(exportFilepath))

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
