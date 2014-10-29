#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.OptionsDist as OptionsDist

# Globals and constants variables.

class TestSimulationOptions(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):

        for filepath in [self.filepathSim, self.filepathCas]:
            if not os.path.isfile(filepath):
                raise SkipTest
            file = open(filepath, 'rb')
            simulationOptions = SimulationOptions.SimulationOptions()
            error = simulationOptions.read(file)

            self.assertEquals(None, error)
            self.assertEquals(30107002, simulationOptions._version)

            # ADF
            self.assertEquals(30107002, simulationOptions._optionsADF._version)
            self.assertAlmostEquals(1.0, simulationOptions._optionsADF.DQE)
            self.assertEquals(1, simulationOptions._optionsADF.Enabled)
            self.assertEquals(0, simulationOptions._optionsADF.keepData)
            self.assertAlmostEquals(0.5, simulationOptions._optionsADF.MaxAngle)
            self.assertAlmostEquals(0.2, simulationOptions._optionsADF.MinAngle)
            self.assertEquals(0, simulationOptions._optionsADF.MaxPoints)

            # AdvBackSet
            self.assertEquals(30107002, simulationOptions._optionsAdvBackSet._version)
            self.assertEquals(False, simulationOptions._optionsAdvBackSet.UseEnBack)
            self.assertAlmostEquals(10.0, simulationOptions._optionsAdvBackSet.WorkDist)
            self.assertAlmostEquals(1.0, simulationOptions._optionsAdvBackSet.DetectScaleX)
            self.assertAlmostEquals(1.0, simulationOptions._optionsAdvBackSet.DetectScaleY)
            self.assertEquals(False, simulationOptions._optionsAdvBackSet.ValidMatrix)

            self.assertAlmostEquals(0.0, simulationOptions._optionsAdvBackSet.BEMin_Angle)
            self.assertAlmostEquals(0.0, simulationOptions._optionsAdvBackSet.BEMax_Angle)
            self.assertAlmostEquals(0.0, simulationOptions._optionsAdvBackSet.EFilterMax)
            self.assertAlmostEquals(0.0, simulationOptions._optionsAdvBackSet.EFilterMin)

            for i in range(101):
                self.assertAlmostEquals(1.0, simulationOptions._optionsAdvBackSet.EFilterVal[i])

            self.assertEquals(0, simulationOptions._optionsAdvBackSet.FEFilter)

            # Dist
            self.assertEquals(30107002, simulationOptions._optionsDist._version)
            self.assertAlmostEquals(1.0, simulationOptions._optionsDist.DenrMax / OptionsDist.autoFlag)

            self.assertAlmostEquals(1000.0, simulationOptions._optionsDist.DEposCyl_Z)
            self.assertEquals(0, simulationOptions._optionsDist.DEposCyl_Z_Log)
            self.assertEquals(OptionsDist.DIST_DEPOS_POSITION_ABSOLUTE, simulationOptions._optionsDist.DEpos_Position)

            # EnergyByPos
            self.assertEquals(30107002, simulationOptions._optionsEnergyByPos._version)
            self.assertEquals(0, simulationOptions._optionsEnergyByPos.Diffuse)
            self.assertEquals(1, simulationOptions._optionsEnergyByPos.Depos_Summation)
            self.assertAlmostEquals(0.1, simulationOptions._optionsEnergyByPos.DEpos_IsoLevel)
            self.assertAlmostEquals(-1.0, simulationOptions._optionsEnergyByPos.CarrierSurfaceRecombination)
            self.assertEquals(1, simulationOptions._optionsEnergyByPos.normalize)

            # Micro
            self.assertEquals(30107002, simulationOptions._optionsMicro._version)
            self.assertEquals(0, simulationOptions._optionsMicro.scanning_mode)
            self.assertAlmostEquals(0.0, simulationOptions._optionsMicro.X_plane_position)

            self.assertAlmostEquals(1.0, simulationOptions._optionsMicro.scanPtDist)
            self.assertEquals(1, simulationOptions._optionsMicro.keep_simulation_data)

            # Physic
            self.assertEquals(30107002, simulationOptions._optionsPhysic._version)
            self.assertEquals(3, simulationOptions._optionsPhysic.FRan)
            self.assertEquals(1, simulationOptions._optionsPhysic.FDeds)
            self.assertEquals(5, simulationOptions._optionsPhysic.FTotalCross)
            self.assertEquals(5, simulationOptions._optionsPhysic.FPartialCross)
            self.assertEquals(1, simulationOptions._optionsPhysic.FCosDirect)
            self.assertEquals(3, simulationOptions._optionsPhysic.FSecIon)
            self.assertEquals(0, simulationOptions._optionsPhysic.FPotMoy)

            self.assertEquals(10, simulationOptions._optionsPhysic.max_secondary_order)
            self.assertAlmostEquals(0.05, simulationOptions._optionsPhysic.Min_Energy_Nosec)
            self.assertAlmostEquals(0.0004, simulationOptions._optionsPhysic.Residual_Energy_Loss)
            self.assertAlmostEquals(-1, simulationOptions._optionsPhysic.Min_Energy_With_Sec)
            self.assertAlmostEquals(-1, simulationOptions._optionsPhysic.Min_Gen_Secondary_Energy)

            # Xray
            self.assertEquals(30107002, simulationOptions._optionsXray._version)
            self.assertAlmostEquals(40.0, simulationOptions._optionsXray.TOA)
            self.assertAlmostEquals(0.0, simulationOptions._optionsXray.PhieRX)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
