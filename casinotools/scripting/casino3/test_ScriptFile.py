#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest
import logging
import tempfile
import shutil
import filecmp
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
from casinotools.scripting.casino3 import ScriptFile
from  casinotools.utilities.path import get_current_module_path
from casinotools.scripting.casino3 import CasinoSimulationExperiment
from casinotools.scripting.casino3 import SimulationParameters as sp

# Globals and constants variables.

class TestScriptFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.scriptFilepathRef = get_current_module_path(__file__, "../../../testData/scripting/casino3/ScriptFile.txt")
        self.temporaryPath = tempfile.mkdtemp()
        basename = "TestCasinoBatchFile"

        self._scriptFile = ScriptFile.ScriptFile(basename)
        self._scriptFile.setPath(self.temporaryPath)

        simFilepath = "results/GoldNanoparticle_00mrad_XY100nm.sim"
        self._scriptFile.setSimulationFilepath(simFilepath)
        self._scriptFile.setEnergy_keV(200)
        self._scriptFile.setTrajectoryNumbers(100)

        self._scriptFile.setSampleRadius(1, "Sphere_0")
        self._scriptFile.setSampleTranslationZ(-1.001, "Sphere_0")

        self._scriptFile.setSampleDivision(20, "Sphere_0")

        resultFilepath = "results/ParticleSize_200keV_000100/$(sim_name)_200keV_000100_20_r$(ranged_value1)nm.cas"
        self._scriptFile.setResultsFilepath(resultFilepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.temporaryPath)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_createFile(self):
        self._scriptFile.createFile()
        scriptFilepath = self._scriptFile._generateScriptFilepath()
        logging.debug(scriptFilepath)

        if not os.path.isfile(self.scriptFilepathRef):
            raise SkipTest
        linesRef = open(self.scriptFilepathRef, 'rb').readlines()
        lines = open(scriptFilepath, 'rb').readlines()

        for lineRef, line in zip(linesRef, lines):
            logging.debug(line[:-1])
            self.assertEquals(lineRef, line)

        self.assertEquals(len(linesRef), len(lines))
        self.assertTrue(filecmp.cmp(scriptFilepath, self.scriptFilepathRef, shallow=True))

        #self.fail("Test if the testcase is working.")

    def test_createLinesOrder(self):
        numberCommands = len(self._scriptFile._linesOrder)
        self.assertEquals(24, numberCommands)

        #self.fail("Test if the testcase is working.")

    def test_commands(self):
        lineRef = 'LOAD "results/GoldNanoparticle_00mrad_XY100nm.sim";'
        self._scriptFile.COMMAND_LOAD.setValue("results/GoldNanoparticle_00mrad_XY100nm.sim")
        line = self._scriptFile.COMMAND_LOAD.generateLine()
        self.assertEquals(lineRef, line)

        lineRef = 'SIM "results/ParticleSize_200keV_000100/$(sim_name)_200keV_000100_20_r$(ranged_value1)nm.cas";'
        self._scriptFile.COMMAND_SIM.setValue("results/ParticleSize_200keV_000100/$(sim_name)_200keV_000100_20_r$(ranged_value1)nm.cas")
        line = self._scriptFile.COMMAND_SIM.generateLine()
        self.assertEquals(lineRef, line)

        lineRef = "SET ENERGY 200.0;"
        self._scriptFile.COMMAND_ENERGY.setValue(200.0)
        line = self._scriptFile.COMMAND_ENERGY.generateLine()
        self.assertEquals(lineRef, line)

        lineRef = "RANGE_SAMPLE RADIUS Sphere_0 1 1 1;"
        self._scriptFile.COMMAND_SAMPLE_RADIUS.setValue(1, "Sphere_0")
        line = self._scriptFile.COMMAND_SAMPLE_RADIUS.generateLine()
        self.assertEquals(lineRef, line)

        lineRef = "RANGE_SAMPLE TRANSLATION.z Sphere_0 (-1.001) (-1.001) 1;"
        self._scriptFile.COMMAND_SAMPLE_TRANSLATION_Z.setValue(-1.001, "Sphere_0")
        line = self._scriptFile.COMMAND_SAMPLE_TRANSLATION_Z.generateLine()
        self.assertEquals(lineRef, line)

        #self.fail("Test if the testcase is working.")

    def test_Name(self):
        textRef = 'results/GoldNanoparticle_00mrad_XY100nm.sim'
        self._scriptFile.COMMAND_LOAD.setValue("results/GoldNanoparticle_00mrad_XY100nm.sim")
        text = str(self._scriptFile.COMMAND_LOAD)
        self.assertEquals(textRef, text)

        textRef = 'results/ParticleSize_200keV_000100/$(sim_name)_200keV_000100_20_r$(ranged_value1)nm.cas'
        self._scriptFile.COMMAND_SIM.setValue("results/ParticleSize_200keV_000100/$(sim_name)_200keV_000100_20_r$(ranged_value1)nm.cas")
        text = str(self._scriptFile.COMMAND_SIM)
        self.assertEquals(textRef, text)

        textRef = "200.0keV"
        self._scriptFile.COMMAND_ENERGY.setValue(200.0)
        text = str(self._scriptFile.COMMAND_ENERGY)
        self.assertEquals(textRef, text)


        textRef = "Sphere_0_r1nm"
        self._scriptFile.COMMAND_SAMPLE_RADIUS.setValue(1, "Sphere_0")
        text = str(self._scriptFile.COMMAND_SAMPLE_RADIUS)
        self.assertEquals(textRef, text)

        textRef = "Sphere_0_z-1.001nm"
        self._scriptFile.COMMAND_SAMPLE_TRANSLATION_Z.setValue(-1.001, "Sphere_0")
        text = str(self._scriptFile.COMMAND_SAMPLE_TRANSLATION_Z)
        self.assertEquals(textRef, text)

        #self.fail("Test if the testcase is working.")

    def test_setExperiment(self):
        names = [sp.ENERGIES, sp.NUMBER_ELECTRONS, sp.FILENAMES]
        values = [200.0, 12563, "some.sim"]
        basename = "Basename"
        experiment = CasinoSimulationExperiment.CasinoSimulationExperiment(names, values)

        scriptFile = ScriptFile.ScriptFile(basename)
        scriptFile.setExperiment(experiment)

        scriptFile.setPath(self.temporaryPath)

        scriptFile.setSimulationPath(self.temporaryPath)

        scriptFile.setResultsPath(self.temporaryPath)

        scriptFile.createFile()

        scriptFilename = scriptFile.getScriptFilename()
        resultFilepath = scriptFile.getResultsFilepath()

        scriptFilenameRef = "Script_Basename_some_E200.0keV_N12563e.txt"
        self.assertEquals(scriptFilenameRef, scriptFilename)

        resultFilepathRef = os.path.join(self.temporaryPath, "Basename_some_E200.0keV_N12563e.cas")
        self.assertEquals(resultFilepathRef, resultFilepath)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':    #pragma: no cover
    import nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
