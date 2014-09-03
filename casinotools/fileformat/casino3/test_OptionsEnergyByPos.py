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
import casinotools.fileformat.casino3.OptionsEnergyByPos as OptionsEnergyByPos
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestOptionsEnergyByPos(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        reader = OptionsEnergyByPos.OptionsEnergyByPos()
        file = open(self.filepathSim, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertEquals(0, reader.Diffuse)
        self.assertEquals(1, reader.Depos_Summation)
        self.assertAlmostEquals(0.1, reader.DEpos_IsoLevel)
        self.assertAlmostEquals(-1.0, reader.CarrierSurfaceRecombination)
        self.assertEquals(1, reader.normalize)

        reader = OptionsEnergyByPos.OptionsEnergyByPos()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertEquals(0, reader.Diffuse)
        self.assertEquals(1, reader.Depos_Summation)
        self.assertAlmostEquals(0.1, reader.DEpos_IsoLevel)
        self.assertAlmostEquals(-1.0, reader.CarrierSurfaceRecombination)
        self.assertEquals(1, reader.normalize)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
