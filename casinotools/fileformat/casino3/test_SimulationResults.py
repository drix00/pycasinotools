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
import casinotools.fileformat.casino3.SimulationResults as SimulationResults
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSimulationResults(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        options = SimulationOptions.SimulationOptions()
        options.read(file)
        file.close()
        del file

        results = SimulationResults.SimulationResults()
        file = open(self.filepathCas, 'rb')
        file.seek(12648)
        error = results.read(file, options)

        self.assertEqual(None, error)
        self.assertEqual(1, results._numberSimulations)

        self.assertEqual(20031202, results._version)

        self.assertAlmostEqual(0.8, results._initialEnergy_keV)
        self.assertEqual(0.0, results._rkoMax)

        self.assertEqual(30107002, results._versionSimulationResults)
        self.assertTrue(results._isTotalEnergyDensitySaved)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
