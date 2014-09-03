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

# Local modules.
import casinotools.fileformat.casino3.Sample as Sample
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.SampleObjectFactory as SampleObjectFactory

# Globals and constants variables.

class TestSample(test_FileReaderWriterTools.TestFileReaderWriterTools):
    def test_read(self):
        file = open(self.filepathSim, "rb")
        file.seek(55)
        sample = Sample.Sample()
        sample.read(file)

        self.assertEquals(30107002, sample._version)
        self.assertEquals(False, sample._useSubstrate)

        self.assertEquals(4, sample._count)

        boxShape = sample._sampleObjects[0]

        self.assertEquals(SampleObjectFactory.SHAPE_BOX, boxShape._type)
        self.assertEquals(30105004, boxShape._version)
        self.assertEquals("Box_0", boxShape._name)
        self.assertEquals("Undefined", boxShape._regionName)
        self.assertEquals((0.0, 0.0, 5000.0), boxShape._translation)
        self.assertEquals((0.0, 0.0, 0.0), boxShape._rotation)
        self.assertEquals((10000.0, 10000.0, 10000.0), boxShape._scale)
        self.assertEquals((0.984375, 0.0, 0.0), boxShape._color)

        self.assertEquals(20, sample._maxSampleTreeLevel)

        #self.fail("Test if the testcase is working.")

    def test_read3202(self):
        file = open(self.filepathSim_3202, "rb")
        file.seek(55)
        sample = Sample.Sample()
        sample.read(file)

        self.assertEquals(30200002, sample._version)
        self.assertEquals(False, sample._useSubstrate)

        self.assertEquals(4, sample._count)

        boxShape = sample._sampleObjects[0]

        self.assertEquals(SampleObjectFactory.SHAPE_BOX, boxShape._type)
        self.assertEquals(30105004, boxShape._version)
        self.assertEquals("Box_0", boxShape._name)
        self.assertEquals("Undefined", boxShape._regionName)
        self.assertEquals((0.0, 0.0, 5000.0), boxShape._translation)
        self.assertEquals((0.0, 0.0, 0.0), boxShape._rotation)
        self.assertEquals((10000.0, 10000.0, 10000.0), boxShape._scale)
        self.assertEquals((0.984375, 0.0, 0.0), boxShape._color)

        self.assertEquals(20, sample._maxSampleTreeLevel)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
