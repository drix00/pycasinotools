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
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.OptionsDist as OptionsDist
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSimulationOptions(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):

        for filepath in [self.filepathSim, self.filepathCas]:
            if is_bad_file(filepath):
                raise SkipTest
            file = open(filepath, 'rb')
            simulationOptions = SimulationOptions.SimulationOptions()
            error = simulationOptions.read(file)

            self.assertEqual(None, error)
            self.assertEqual(30107002, simulationOptions._version)

            # ADF
            self.assertEqual(30107002, simulationOptions._optionsADF._version)
            self.assertAlmostEqual(1.0, simulationOptions._optionsADF.DQE)
            self.assertEqual(1, simulationOptions._optionsADF.Enabled)
            self.assertEqual(0, simulationOptions._optionsADF.keepData)
            self.assertAlmostEqual(0.5, simulationOptions._optionsADF.MaxAngle)
            self.assertAlmostEqual(0.2, simulationOptions._optionsADF.MinAngle)
            self.assertEqual(0, simulationOptions._optionsADF.MaxPoints)

            # AdvBackSet
            self.assertEqual(30107002, simulationOptions._optionsAdvBackSet._version)
            self.assertEqual(False, simulationOptions._optionsAdvBackSet.UseEnBack)
            self.assertAlmostEqual(10.0, simulationOptions._optionsAdvBackSet.WorkDist)
            self.assertAlmostEqual(1.0, simulationOptions._optionsAdvBackSet.DetectScaleX)
            self.assertAlmostEqual(1.0, simulationOptions._optionsAdvBackSet.DetectScaleY)
            self.assertEqual(False, simulationOptions._optionsAdvBackSet.ValidMatrix)

            self.assertAlmostEqual(0.0, simulationOptions._optionsAdvBackSet.BEMin_Angle)
            self.assertAlmostEqual(0.0, simulationOptions._optionsAdvBackSet.BEMax_Angle)
            self.assertAlmostEqual(0.0, simulationOptions._optionsAdvBackSet.EFilterMax)
            self.assertAlmostEqual(0.0, simulationOptions._optionsAdvBackSet.EFilterMin)

            for i in range(101):
                self.assertAlmostEqual(1.0, simulationOptions._optionsAdvBackSet.EFilterVal[i])

            self.assertEqual(0, simulationOptions._optionsAdvBackSet.FEFilter)

            # Dist
            self.assertEqual(30107002, simulationOptions._optionsDist._version)
            self.assertAlmostEqual(1.0, simulationOptions._optionsDist.DenrMax / OptionsDist.autoFlag)

            self.assertAlmostEqual(1000.0, simulationOptions._optionsDist.DEposCyl_Z)
            self.assertEqual(0, simulationOptions._optionsDist.DEposCyl_Z_Log)
            self.assertEqual(OptionsDist.DIST_DEPOS_POSITION_ABSOLUTE, simulationOptions._optionsDist.DEpos_Position)

            # EnergyByPos
            self.assertEqual(30107002, simulationOptions._optionsEnergyByPos._version)
            self.assertEqual(0, simulationOptions._optionsEnergyByPos.Diffuse)
            self.assertEqual(1, simulationOptions._optionsEnergyByPos.Depos_Summation)
            self.assertAlmostEqual(0.1, simulationOptions._optionsEnergyByPos.DEpos_IsoLevel)
            self.assertAlmostEqual(-1.0, simulationOptions._optionsEnergyByPos.CarrierSurfaceRecombination)
            self.assertEqual(1, simulationOptions._optionsEnergyByPos.normalize)

            # Micro
            self.assertEqual(30107002, simulationOptions._optionsMicro._version)
            self.assertEqual(0, simulationOptions._optionsMicro.scanning_mode)
            self.assertAlmostEqual(0.0, simulationOptions._optionsMicro.X_plane_position)

            self.assertAlmostEqual(1.0, simulationOptions._optionsMicro.scanPtDist)
            self.assertEqual(1, simulationOptions._optionsMicro.keep_simulation_data)

            # Physic
            self.assertEqual(30107002, simulationOptions._optionsPhysic._version)
            self.assertEqual(3, simulationOptions._optionsPhysic.FRan)
            self.assertEqual(1, simulationOptions._optionsPhysic.FDeds)
            self.assertEqual(5, simulationOptions._optionsPhysic.FTotalCross)
            self.assertEqual(5, simulationOptions._optionsPhysic.FPartialCross)
            self.assertEqual(1, simulationOptions._optionsPhysic.FCosDirect)
            self.assertEqual(3, simulationOptions._optionsPhysic.FSecIon)
            self.assertEqual(0, simulationOptions._optionsPhysic.FPotMoy)

            self.assertEqual(10, simulationOptions._optionsPhysic.max_secondary_order)
            self.assertAlmostEqual(0.05, simulationOptions._optionsPhysic.Min_Energy_Nosec)
            self.assertAlmostEqual(0.0004, simulationOptions._optionsPhysic.Residual_Energy_Loss)
            self.assertAlmostEqual(-1, simulationOptions._optionsPhysic.Min_Energy_With_Sec)
            self.assertAlmostEqual(-1, simulationOptions._optionsPhysic.Min_Gen_Secondary_Energy)

            # Xray
            self.assertEqual(30107002, simulationOptions._optionsXray._version)
            self.assertAlmostEqual(40.0, simulationOptions._optionsXray.TOA)
            self.assertAlmostEqual(0.0, simulationOptions._optionsXray.PhieRX)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
