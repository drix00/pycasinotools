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
import casinotools.fileformat.casino3.options_energy_by_pos as OptionsEnergyByPos
import tests.fileformat.test_file_reader_writer_tools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestOptionsEnergyByPos(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            pytest.skip()
        file = open(self.filepathSim, 'rb')
        reader = OptionsEnergyByPos.OptionsEnergyByPos()
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(0, reader.Diffuse)
        self.assertEqual(1, reader.Depos_Summation)
        self.assertAlmostEqual(0.1, reader.DEpos_IsoLevel)
        self.assertAlmostEqual(-1.0, reader.CarrierSurfaceRecombination)
        self.assertEqual(1, reader.normalize)

        reader = OptionsEnergyByPos.OptionsEnergyByPos()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEqual(None, error)
        self.assertEqual(30107002, reader._version)
        self.assertEqual(0, reader.Diffuse)
        self.assertEqual(1, reader.Depos_Summation)
        self.assertAlmostEqual(0.1, reader.DEpos_IsoLevel)
        self.assertAlmostEqual(-1.0, reader.CarrierSurfaceRecombination)
        self.assertEqual(1, reader.normalize)

        #self.fail("Test if the testcase is working.")
