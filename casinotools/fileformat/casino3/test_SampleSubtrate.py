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
import casinotools.fileformat.casino3.SampleObjectFactory as SampleObjectFactory
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.fileformat.casino3.SampleShape.ShapeType import SHAPE_SUBSTRATE
# Globals and constants variables.

class TestSampleSubtrate(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if not os.path.isfile(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, "rb")
        file.seek(103)
        sample = SampleObjectFactory.CreateObjectFromType(SHAPE_SUBSTRATE)
        sample.read(file)

        self.assertEquals(30105004, sample._version)

        self.assertEquals("Substrate", sample._name)
        self.assertEquals("Substrate", sample._regionName)

        self.assertEquals((0.0, 0.0, 0.0), sample._translation)
        self.assertEquals((0.0, 0.0, 0.0), sample._rotation)
        self.assertEquals((100000.0, 100000.0, 100000.0), sample._scale)
        self.assertEquals((0.0, 0.0, 1.0), sample._color)


        self.assertEquals(0, sample._numberEdges)

        self.assertEquals(SampleObjectFactory.SHAPE_SUBSTRATE, sample._type)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
