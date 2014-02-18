#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2378 $"
__svnDate__ = "$Date: 2011-06-20 15:45:48 -0400 (Mon, 20 Jun 2011) $"
__svnId__ = "$Id: test_SimulationResults.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.SimulationResults as SimulationResults
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions

# Globals and constants variables.

class TestSimulationResults(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        options = SimulationOptions.SimulationOptions()
        file = open(self.filepathCas, 'rb')
        options.read(file)
        file.close()
        del file

        results = SimulationResults.SimulationResults()
        file = open(self.filepathCas, 'rb')
        file.seek(12648)
        error = results.read(file, options)

        self.assertEquals(None, error)
        self.assertEquals(1, results._numberSimulations)

        self.assertEquals(20031202, results._version)

        self.assertAlmostEquals(0.8, results._initialEnergy_keV)
        self.assertEquals(0.0, results._rkoMax)

        self.assertEquals(30107002, results._versionSimulationResults)
        self.assertTrue(results._isTotalEnergyDensitySaved)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
