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
import casinotools.file_format.casino3.energy_matrix as EnergyMatrix
import tests.file_format.test_file_reader_writer_tools as test_FileReaderWriterTools
import casinotools.file_format.casino3.options_dist as OptionsDist
import casinotools.file_format.casino3.simulation_options as SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestEnergyMatrix(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        options = SimulationOptions.SimulationOptions()
        options._optionsDist.DEpos_Type = OptionsDist.DIST_DEPOS_TYPE_CARTESIAN
        results = EnergyMatrix.EnergyMatrix(options, None)
        if is_bad_file(self.filepathCas):
            pytest.skip()
        file = open(self.filepathCas, 'rb')
        file.seek(4042541)

        error = results.read(file)
        self.assertEqual(None, error)
        self.assertEqual(125000, results._numberElements)
        self.assertEqual(4042541, results._startPosition)
        self.assertEqual(4042541 + 125000 * 8, results._endPosition)
