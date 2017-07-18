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
import casinotools.fileformat.casino3.ScanPointResults as ScanPointResults
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestScanPointResults(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        options = SimulationOptions.SimulationOptions()
        options.read(file)
        file.close()
        del file

        results = ScanPointResults.ScanPointResults()
        file = open(self.filepathCas, 'rb')
        #file.seek(12648)
        error = results.read(file, options)

        self.assertEqual(None, error)

        self.assertEqual(30107002, results._version)

        self.assertAlmostEqual(0.8, results._initialEnergy_keV)
        self.assertAlmostEqual(0.0, results._rkoMax)
        self.assertAlmostEqual(24.04826155663, results._rkoMaxW)

        self.assertEqual(1000000, results._numberSimulatedTrajectories)
        self.assertEqual(2, results._beingProcessed)

        self.assertAlmostEqual(5.468900000000E-02, results._backscatteredCoefficient)
        self.assertAlmostEqual(0.0, results._backscatteredDetectedCoefficient)
        self.assertAlmostEqual(0.0, results._secondaryCoefficient)
        self.assertAlmostEqual(0.0, results._transmittedCoefficient)
        self.assertAlmostEqual(0.0, results._transmittedDetectedCoefficient)
        self.assertEqual(54689, results._numberBackscatteredElectrons)
        self.assertAlmostEqual(0.0, results._numberBackscatteredElectronsDetected)
        self.assertEqual(0, results._numberSecondaryElectrons)

        self.assertEqual(8, results._numberResults)

        for i in range(1, 8 + 1):
            self.assertEqual(i, results._regionIntensityInfos[i - 1]._regionID)

        # DZMax distribution results.
        self.assertEqual(True, results._isDZMax)
        self.assertEqual(30105020, results.dzMax._version)

        self.assertEqual(1000, results.dzMax._size)
        self.assertAlmostEqual(0.0, results.dzMax._borneInf)
        self.assertAlmostEqual(8.900000000000E+01, results.dzMax._borneSup)
        self.assertEqual(0, results.dzMax._isLog)
        self.assertEqual(0, results.dzMax._isUneven)

        self.assertEqual("Z Max", results.dzMax._title)
        self.assertEqual("Depth (nm)", results.dzMax._xTitle)
        self.assertEqual("Hits (Normalized)", results.dzMax._yTitle)

        values = results.dzMax.getValues()
        self.assertAlmostEqual(1.0, values[0])
        self.assertAlmostEqual(0.0, values[-1])

        self.assertEqual(True, results._isDEnergy_Density)
        self.assertAlmostEqual(1.518294795870E-01, results.DEnergy_Density_Max_Energy)

        self.assertEqual(199, results.getNumberSavedTrajectories())

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
