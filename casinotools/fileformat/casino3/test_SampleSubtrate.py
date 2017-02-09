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
import casinotools.fileformat.casino3.SampleObjectFactory as SampleObjectFactory
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.fileformat.casino3.SampleShape.ShapeType import SHAPE_SUBSTRATE
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSampleSubtrate(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        file = open(self.filepathSim, "rb")
        file.seek(103)
        sample = SampleObjectFactory.CreateObjectFromType(SHAPE_SUBSTRATE)
        sample.read(file)

        self.assertEqual(30105004, sample._version)

        self.assertEqual("Substrate", sample._name)
        self.assertEqual("Substrate", sample._regionName)

        self.assertEqual((0.0, 0.0, 0.0), sample._translation)
        self.assertEqual((0.0, 0.0, 0.0), sample._rotation)
        self.assertEqual((100000.0, 100000.0, 100000.0), sample._scale)
        self.assertEqual((0.0, 0.0, 1.0), sample._color)


        self.assertEqual(0, sample._numberEdges)

        self.assertEqual(SampleObjectFactory.SHAPE_SUBSTRATE, sample._type)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
