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
__svnId__ = "$Id: test_ScanPointResults.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.ScanPointResults as ScanPointResults
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions

# Globals and constants variables.

class TestScanPointResults(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        options = SimulationOptions.SimulationOptions()
        file = open(self.filepathCas, 'rb')
        options.read(file)
        file.close()
        del file

        results = ScanPointResults.ScanPointResults()
        file = open(self.filepathCas, 'rb')
        #file.seek(12648)
        error = results.read(file, options)

        self.assertEquals(None, error)

        self.assertEquals(30107002, results._version)

        self.assertAlmostEquals(0.8, results._initialEnergy_keV)
        self.assertAlmostEquals(0.0, results._rkoMax)
        self.assertAlmostEquals(24.04826155663, results._rkoMaxW)

        self.assertEquals(1000000, results._numberSimulatedTrajectories)
        self.assertEquals(2, results._beingProcessed)

        self.assertAlmostEquals(5.468900000000E-02, results._backscatteredCoefficient)
        self.assertAlmostEquals(0.0, results._backscatteredDetectedCoefficient)
        self.assertAlmostEquals(0.0, results._secondaryCoefficient)
        self.assertAlmostEquals(0.0, results._transmittedCoefficient)
        self.assertAlmostEquals(0.0, results._transmittedDetectedCoefficient)
        self.assertEquals(54689, results._numberBackscatteredElectrons)
        self.assertAlmostEquals(0.0, results._numberBackscatteredElectronsDetected)
        self.assertEquals(0, results._numberSecondaryElectrons)

        self.assertEquals(8, results._numberResults)

        for i in xrange(1, 8 + 1):
            self.assertEquals(i, results._regionIntensityInfos[i - 1]._regionID)

        # DZMax distribution results.
        self.assertEquals(True, results._isDZMax)
        self.assertEquals(30105020, results.dzMax._version)

        self.assertEquals(1000, results.dzMax._size)
        self.assertAlmostEquals(0.0, results.dzMax._borneInf)
        self.assertAlmostEquals(8.900000000000E+01, results.dzMax._borneSup)
        self.assertEquals(0, results.dzMax._isLog)
        self.assertEquals(0, results.dzMax._isUneven)

        self.assertEquals("Z Max", results.dzMax._title)
        self.assertEquals("Depth (nm)", results.dzMax._xTitle)
        self.assertEquals("Hits (Normalized)", results.dzMax._yTitle)

        values = results.dzMax.getValues()
        self.assertAlmostEquals(1.0, values[0])
        self.assertAlmostEquals(0.0, values[-1])

        self.assertEquals(True, results._isDEnergy_Density)
        self.assertAlmostEquals(1.518294795870E-01, results.DEnergy_Density_Max_Energy)

        self.assertEquals(199, results.getNumberSavedTrajectories())

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
