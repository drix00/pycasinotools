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

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.SimulationResults as SimulationResults
import casinotools.fileformat.casino2.test_File as test_File
import casinotools.fileformat.casino2.SimulationOptions as SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSimulationResults(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        with open(self.filepathCas, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        f = open(self.filepathCas, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        version = 26
        options = SimulationOptions.SimulationOptions()
        options.read(file, version)
        file.seek(696824)
        simulationResults = SimulationResults.SimulationResults()
        simulationResults.read(file, options, version)

        self.assertEqual(1, simulationResults.BE_Intensity_Size)
        self.assertEqual(3.950000000000E-02, simulationResults.BE_Intensity[0])

        element = simulationResults._elementIntensityList[0]
        self.assertEqual("B", element.Name)
        self.assertAlmostEqual(3.444919288026E+02, element.IntensityK[0])

        element = simulationResults._elementIntensityList[1]
        self.assertEqual("C", element.Name)
        self.assertAlmostEqual(4.687551040349E+01, element.IntensityK[0])

        self.assertEqual(1000, simulationResults.NbPointDZMax)
        self.assertEqual(500, simulationResults.NbPointDENR)
        self.assertEqual(500, simulationResults.NbPointDENT)
        self.assertEqual(500, simulationResults.NbPointDRSR)
        #self.assertEqual(0, simulationResults.NbPointDNCR)
        self.assertEqual(50, simulationResults.NbPointDEpos_X)
        self.assertEqual(50, simulationResults.NbPointDEpos_Y)
        self.assertEqual(50, simulationResults.NbPointDEpos_Z)
        self.assertAlmostEqual(1.608165461510E-02, simulationResults.DEpos_maxE)
        self.assertEqual(91, simulationResults.NbPointDBANG)
        self.assertEqual(91, simulationResults.NbPointDAngleVSEnergie)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
