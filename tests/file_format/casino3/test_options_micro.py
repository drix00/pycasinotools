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
import casinotools.file_format.casino3.options_micro as OptionsMicro
import tests.file_format.test_file_reader_writer_tools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestOptionsMicro(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()
        file = open(self.filepathSim, 'rb')
        reader = OptionsMicro.OptionsMicro()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(0, reader.scanning_mode)
        self.assertAlmostEqual(0.0, reader.X_plane_position)

        self.assertAlmostEqual(1.0, reader.scanPtDist)
        self.assertEqual(1, reader.keep_simulation_data)

        reader = OptionsMicro.OptionsMicro()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(0, reader.scanning_mode)
        self.assertAlmostEqual(0.0, reader.X_plane_position)

        self.assertAlmostEqual(1.0, reader.scanPtDist)
        self.assertEqual(1, reader.keep_simulation_data)

        #self.fail("Test if the testcase is working.")
