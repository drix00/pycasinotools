#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2378 $"
__svnDate__ = "$Date: 2011-06-20 15:45:48 -0400 (Mon, 20 Jun 2011) $"
__svnId__ = "$Id: test_DiffusedEnergyMatrix.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinotools.fileformat.casino3.DiffusedEnergyMatrix as DiffusedEnergyMatrix
import casinotools.fileformat.casino3.OptionsDist as OptionsDist
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions

# Globals and constants variables.

class TestDiffusedEnergyMatrix(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        options = SimulationOptions.SimulationOptions()
        options._optionsDist.DEpos_Type = OptionsDist.DIST_DEPOS_TYPE_CARTESIAN
        results = DiffusedEnergyMatrix.DiffusedEnergyMatrix(options, None)
        file = open(self.filepathCas, 'rb')
        file.seek(1012742)

        error = results.read(file)
        self.assertEquals(None, error)
        self.assertEquals(30107000, results._version)
        self.assertEquals(125000, results._numberElements)
        self.assertEquals(1012762, results._startPosition)
        self.assertEquals(2012806, results._endPosition)
        #TODO why the end position is more than startPosition + _numberElements*sizeof(double)?

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
