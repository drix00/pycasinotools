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
__svnId__ = "$Id: test_EnergyMatrix.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import casinoTools.FileFormat.casino3.EnergyMatrix as EnergyMatrix
import casinoTools.FileFormat.casino3.test_FileReaderWriterTools as test_FileReaderWriterTools
import casinoTools.FileFormat.casino3.OptionsDist as OptionsDist
import casinoTools.FileFormat.casino3.SimulationOptions as SimulationOptions

# Globals and constants variables.

class TestEnergyMatrix(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        options = SimulationOptions.SimulationOptions()
        options._optionsDist.DEpos_Type = OptionsDist.DIST_DEPOS_TYPE_CARTESIAN
        results = EnergyMatrix.EnergyMatrix(options, None)
        file = open(self.filepathCas, 'rb')
        file.seek(4042541)

        error = results.read(file)
        self.assertEquals(None, error)
        self.assertEquals(125000, results._numberElements)
        self.assertEquals(4042541, results._startPosition)
        self.assertEquals(4042541+125000*8, results._endPosition)

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
