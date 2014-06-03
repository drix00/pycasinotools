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
__svnId__ = "$Id: test_SimulationOptions.py 2620 2011-12-07 16:01:42Z ppinard $"

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.

# Local modules.
import casinotools.fileformat.casino2.SimulationOptions as SimulationOptions
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestSimulationOptions(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        simulationOptions = SimulationOptions.SimulationOptions()
        simulationOptions.read(file, 26)

        self.assertAlmostEquals(0.0, simulationOptions._bseCoefficient)

        self.assertAlmostEquals(10.0, simulationOptions.Beam_Diameter)
        self.assertEquals(10000, simulationOptions.Electron_Number)

        self.assertEquals(False, simulationOptions.UseEnBack)
        self.assertAlmostEquals(10.0, simulationOptions.WorkDist)
        self.assertAlmostEquals(1.0, simulationOptions.DetectScaleX)
        self.assertAlmostEquals(1.0, simulationOptions.DetectScaleY)

        self.assertEquals(True, simulationOptions.FEmissionRX)
        self.assertEquals(500, simulationOptions.NbreCoucheRX)
        self.assertAlmostEquals(10.0, simulationOptions.EpaisCouche)
        self.assertAlmostEquals(40.0, simulationOptions.TOA)
        self.assertAlmostEquals(0.0, simulationOptions.PhieRX)
        self.assertAlmostEquals(0.0, simulationOptions.RkoMax)
        self.assertAlmostEquals(0.0, simulationOptions.RkoMaxW)

        self.assertAlmostEquals(0.050, simulationOptions.Eminimum)
        self.assertEquals(200, simulationOptions.Electron_Display)
        self.assertEquals(5, simulationOptions.Electron_Save)
        self.assertEquals(2, simulationOptions.Memory_Keep)
        self.assertEquals(0, simulationOptions.First)
        self.assertEquals(1, simulationOptions.Keep_Sim)

        self.assertEquals(0, simulationOptions.Display_Colision)
        self.assertEquals(0, simulationOptions.Display_Color)
        self.assertEquals(0, simulationOptions.Display_Projection)
        self.assertEquals(1, simulationOptions.Display_Back)
        self.assertEquals(1, simulationOptions.Display_Refresh)
        self.assertAlmostEquals(0.60, simulationOptions.Minimum_Trajectory_Display_Distance)

        self.assertEquals(0, simulationOptions.FForme)
        self.assertAlmostEquals(1.0, simulationOptions.Total_Thickness / 1.0e10)
        self.assertAlmostEquals(1.0, simulationOptions.Half_Width / 1.0e10)

        self.assertEquals(1, simulationOptions.ShowFadedSqr)
        self.assertEquals(1, simulationOptions.ShowRegions)
        self.assertEquals(1, simulationOptions.SetPointstoRelativePosition)
        self.assertEquals(1, simulationOptions.Summation)
        self.assertEquals(0, simulationOptions.XZorXY)
        self.assertEquals(0, simulationOptions.Yplane)
        self.assertEquals(0, simulationOptions.Zplane)

        self.assertAlmostEquals(30.0, simulationOptions.EFilterMax)
        self.assertAlmostEquals(0.0, simulationOptions.EFilterMin)

        self.assertAlmostEquals(1.648000000000E+02, simulationOptions.RatioX)
        self.assertAlmostEquals(1.340000000000E+02, simulationOptions.RatioY)
        self.assertAlmostEquals(1.648000000000E+02, simulationOptions.RatioZ)
        self.assertAlmostEquals(0.0, simulationOptions.Tot_Ret_En)

        self.assertEquals(5, simulationOptions.NumVtabs)
        self.assertEquals(5, simulationOptions.NumHtabs)

        #self.fail("Test if the testcase is working.")

    def testSetLinescanParameters(self):
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
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
