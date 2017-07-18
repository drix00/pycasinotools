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
import casinotools.fileformat.casino2.SimulationOptions as SimulationOptions
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSimulationOptions(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        simulationOptions = SimulationOptions.SimulationOptions()
        simulationOptions.read(file, 26)

        self.assertAlmostEqual(0.0, simulationOptions._bseCoefficient)

        self.assertAlmostEqual(10.0, simulationOptions.Beam_Diameter)
        self.assertEqual(10000, simulationOptions.Electron_Number)

        self.assertEqual(False, simulationOptions.UseEnBack)
        self.assertAlmostEqual(10.0, simulationOptions.WorkDist)
        self.assertAlmostEqual(1.0, simulationOptions.DetectScaleX)
        self.assertAlmostEqual(1.0, simulationOptions.DetectScaleY)

        self.assertEqual(True, simulationOptions.FEmissionRX)
        self.assertEqual(500, simulationOptions.NbreCoucheRX)
        self.assertAlmostEqual(10.0, simulationOptions.EpaisCouche)
        self.assertAlmostEqual(40.0, simulationOptions.TOA)
        self.assertAlmostEqual(0.0, simulationOptions.PhieRX)
        self.assertAlmostEqual(0.0, simulationOptions.RkoMax)
        self.assertAlmostEqual(0.0, simulationOptions.RkoMaxW)

        self.assertAlmostEqual(0.050, simulationOptions.Eminimum)
        self.assertEqual(200, simulationOptions.Electron_Display)
        self.assertEqual(5, simulationOptions.Electron_Save)
        self.assertEqual(2, simulationOptions.Memory_Keep)
        self.assertEqual(0, simulationOptions.First)
        self.assertEqual(1, simulationOptions.Keep_Sim)

        self.assertEqual(0, simulationOptions.Display_Colision)
        self.assertEqual(0, simulationOptions.Display_Color)
        self.assertEqual(0, simulationOptions.Display_Projection)
        self.assertEqual(1, simulationOptions.Display_Back)
        self.assertEqual(1, simulationOptions.Display_Refresh)
        self.assertAlmostEqual(0.60, simulationOptions.Minimum_Trajectory_Display_Distance)

        self.assertEqual(0, simulationOptions.FForme)
        self.assertAlmostEqual(1.0, simulationOptions.Total_Thickness / 1.0e10)
        self.assertAlmostEqual(1.0, simulationOptions.Half_Width / 1.0e10)

        self.assertEqual(1, simulationOptions.ShowFadedSqr)
        self.assertEqual(1, simulationOptions.ShowRegions)
        self.assertEqual(1, simulationOptions.SetPointstoRelativePosition)
        self.assertEqual(1, simulationOptions.Summation)
        self.assertEqual(0, simulationOptions.XZorXY)
        self.assertEqual(0, simulationOptions.Yplane)
        self.assertEqual(0, simulationOptions.Zplane)

        self.assertAlmostEqual(30.0, simulationOptions.EFilterMax)
        self.assertAlmostEqual(0.0, simulationOptions.EFilterMin)

        self.assertAlmostEqual(1.648000000000E+02, simulationOptions.RatioX)
        self.assertAlmostEqual(1.340000000000E+02, simulationOptions.RatioY)
        self.assertAlmostEqual(1.648000000000E+02, simulationOptions.RatioZ)
        self.assertAlmostEqual(0.0, simulationOptions.Tot_Ret_En)

        self.assertEqual(5, simulationOptions.NumVtabs)
        self.assertEqual(5, simulationOptions.NumHtabs)

        #self.fail("Test if the testcase is working.")

    def testSetLinescanParameters(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        f.seek(0)
        simulationOptions = SimulationOptions.SimulationOptions()
        simulationOptions.read(f, 26)
        f.close()

        simulationOptions.setLinescanParameters(0, 100, 10)

        # Values were also verified inside the GUI
        self.assertEqual(1, simulationOptions.Scan_Image)
        self.assertAlmostEqual(0, simulationOptions._positionStart_nm, 4)
        self.assertAlmostEqual(100, simulationOptions._positionEnd_nm, 4)
        self.assertAlmostEqual(10, simulationOptions._positionStep_nm, 4)
        self.assertEqual(10, simulationOptions._positionNumberStep)

    def testSetPosition(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        f.seek(0)
        simulationOptions = SimulationOptions.SimulationOptions()
        simulationOptions.read(f, 26)
        f.close()

        simulationOptions.setPosition(50)

        # Values were also verified inside the GUI
        self.assertEqual(0, simulationOptions.Scan_Image)
        self.assertAlmostEqual(50, simulationOptions._positionStart_nm, 4)
        self.assertAlmostEqual(50, simulationOptions._positionEnd_nm, 4)
        self.assertAlmostEqual(1.0, simulationOptions._positionStep_nm, 4)
        self.assertEqual(1, simulationOptions._positionNumberStep)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
