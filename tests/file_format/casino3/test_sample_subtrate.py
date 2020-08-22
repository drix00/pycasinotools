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
import pytest

# Local modules.
import casinotools.file_format.casino3.sample_object_factory as SampleObjectFactory
import tests.file_format.test_file_reader_writer_tools as test_FileReaderWriterTools
from casinotools.file_format.casino3.sample_shape.shape_type import SHAPE_SUBSTRATE
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestSampleSubtrate(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()
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
