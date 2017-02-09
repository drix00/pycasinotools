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
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.DiffusedEnergyMatrix as DiffusedEnergyMatrix
import casinotools.fileformat.casino3.OptionsDist as OptionsDist
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestDiffusedEnergyMatrix(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        options = SimulationOptions.SimulationOptions()
        options._optionsDist.DEpos_Type = OptionsDist.DIST_DEPOS_TYPE_CARTESIAN
        results = DiffusedEnergyMatrix.DiffusedEnergyMatrix(options, None)
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathCas, 'rb')
        file.seek(1012742)

        error = results.read(file)
        self.assertEqual(None, error)
        self.assertEqual(30107000, results._version)
        self.assertEqual(125000, results._numberElements)
        self.assertEqual(1012762, results._startPosition)
        self.assertEqual(2012806, results._endPosition)
        #TODO why the end position is more than startPosition + _numberElements*sizeof(double)?

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
