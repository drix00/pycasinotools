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
import shutil

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino3.Sample as Sample
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.SampleObjectFactory as SampleObjectFactory
import casinotools.fileformat.casino3.File as CasinoFile
from casinotools.utilities.path import get_current_module_path
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSample(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, "rb")
        file.seek(55)
        sample = Sample.Sample()
        sample.read(file)

        self.assertEqual(30107002, sample._version)
        self.assertEqual(False, sample._useSubstrate)

        self.assertEqual(4, sample._count)

        boxShape = sample._sampleObjects[0]

        self.assertEqual(SampleObjectFactory.SHAPE_BOX, boxShape._type)
        self.assertEqual(30105004, boxShape._version)
        self.assertEqual("Box_0", boxShape._name)
        self.assertEqual("Undefined", boxShape._regionName)
        self.assertEqual((0.0, 0.0, 5000.0), boxShape._translation)
        self.assertEqual((0.0, 0.0, 0.0), boxShape._rotation)
        self.assertEqual((10000.0, 10000.0, 10000.0), boxShape._scale)
        self.assertEqual((0.984375, 0.0, 0.0), boxShape._color)

        self.assertEqual(20, sample._maxSampleTreeLevel)

        #self.fail("Test if the testcase is working.")

    def test_read3202(self):
        if is_bad_file(self.filepathSim_3202):
            raise SkipTest
        file = open(self.filepathSim_3202, "rb")
        file.seek(55)
        sample = Sample.Sample()
        sample.read(file)

        self.assertEqual(30200002, sample._version)
        self.assertEqual(False, sample._useSubstrate)

        self.assertEqual(4, sample._count)

        boxShape = sample._sampleObjects[0]

        self.assertEqual(SampleObjectFactory.SHAPE_BOX, boxShape._type)
        self.assertEqual(30105004, boxShape._version)
        self.assertEqual("Box_0", boxShape._name)
        self.assertEqual("Undefined", boxShape._regionName)
        self.assertEqual((0.0, 0.0, 5000.0), boxShape._translation)
        self.assertEqual((0.0, 0.0, 0.0), boxShape._rotation)
        self.assertEqual((10000.0, 10000.0, 10000.0), boxShape._scale)
        self.assertEqual((0.984375, 0.0, 0.0), boxShape._color)

        self.assertEqual(20, sample._maxSampleTreeLevel)

        #self.fail("Test if the testcase is working.")

    def test_getRotationYZ_deg(self):
        testDataPath = get_current_module_path(__file__, "../../../test_data")

        filepathSim = os.path.join(testDataPath, "casino3.x/NoRotationY.sim")
        if is_bad_file(filepathSim):
            raise SkipTest

        casinoFile = open(filepathSim, "rb")
        casinoFile.seek(55)
        sample = Sample.Sample()
        sample.read(casinoFile)

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(0.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(0.0, rotationZ_deg)

        filepathSim = os.path.join(testDataPath, "casino3.x/RotationY10.sim")
        if is_bad_file(filepathSim):
            raise SkipTest

        casinoFile = open(filepathSim, "rb")
        casinoFile.seek(55)
        sample = Sample.Sample()
        sample.read(casinoFile)

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(10.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(0.0, rotationZ_deg)

        filepathSim = os.path.join(testDataPath, "casino3.x/RotationZ15.sim")
        if is_bad_file(filepathSim):
            raise SkipTest

        casinoFile = open(filepathSim, "rb")
        casinoFile.seek(55)
        sample = Sample.Sample()
        sample.read(casinoFile)

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(0.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(15.0, rotationZ_deg)

        filepathSim = os.path.join(testDataPath, "casino3.x/RotationY20Z35.sim")
        if is_bad_file(filepathSim):
            raise SkipTest

        casinoFile = open(filepathSim, "rb")
        casinoFile.seek(55)
        sample = Sample.Sample()
        sample.read(casinoFile)

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(20.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(35.0, rotationZ_deg)

        #self.fail("Test if the testcase is working.")

    def test_modifyRotationYZ_deg(self):
        testDataPath = get_current_module_path(__file__, "../../../test_data")
        sourceFilepath = os.path.join(testDataPath, "casino3.x/NoRotationY.sim")
        if is_bad_file(sourceFilepath):
            raise SkipTest

        if not os.path.isdir(self.temporaryDir):
            raise SkipTest

        rotationYRef_deg = 10.0
        filename = "RotationY10.sim"
        destinationFilepath = os.path.join(self.temporaryDir, filename)

        shutil.copy2(sourceFilepath, destinationFilepath)

        casinoFile = CasinoFile.File(destinationFilepath, isModifiable=True)
        sample = casinoFile.getFirstSimulation().getSample()

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(0.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(0.0, rotationZ_deg)

        sample.modifyRotationY_deg(rotationYRef_deg)
        del casinoFile

        casinoFile = CasinoFile.File(destinationFilepath, isModifiable=False)
        sample = casinoFile.getFirstSimulation().getSample()

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(rotationYRef_deg, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(0.0, rotationZ_deg)

        del casinoFile

        rotationZRef_deg = 15.0
        filename = "RotationZ15.sim"
        destinationFilepath = os.path.join(self.temporaryDir, filename)

        shutil.copy2(sourceFilepath, destinationFilepath)

        casinoFile = CasinoFile.File(destinationFilepath, isModifiable=True)
        sample = casinoFile.getFirstSimulation().getSample()

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(0.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(0.0, rotationZ_deg)

        sample.modifyRotationZ_deg(rotationZRef_deg)
        del casinoFile

        casinoFile = CasinoFile.File(destinationFilepath, isModifiable=False)
        sample = casinoFile.getFirstSimulation().getSample()

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(0.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(rotationZRef_deg, rotationZ_deg)

        del casinoFile

        rotationYRef_deg = 20.0
        rotationZRef_deg = 35.0
        filename = "RotationY20Z35.sim"
        destinationFilepath = os.path.join(self.temporaryDir, filename)

        shutil.copy2(sourceFilepath, destinationFilepath)

        casinoFile = CasinoFile.File(destinationFilepath, isModifiable=True)
        sample = casinoFile.getFirstSimulation().getSample()

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(0.0, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(0.0, rotationZ_deg)

        sample.modifyRotationY_deg(rotationYRef_deg)
        sample.modifyRotationZ_deg(rotationZRef_deg)
        del casinoFile

        casinoFile = CasinoFile.File(destinationFilepath, isModifiable=False)
        sample = casinoFile.getFirstSimulation().getSample()

        rotationY_deg = sample.getRotationY_deg()
        self.assertAlmostEqual(rotationYRef_deg, rotationY_deg)
        rotationZ_deg = sample.getRotationZ_deg()
        self.assertAlmostEqual(rotationZRef_deg, rotationZ_deg)

        del casinoFile

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
