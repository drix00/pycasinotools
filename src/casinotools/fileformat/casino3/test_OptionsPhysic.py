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
__svnId__ = "$Id: test_OptionsPhysic.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.OptionsPhysic as OptionsPhysic
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestOptionsPhysic(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        reader = OptionsPhysic.OptionsPhysic()
        file = open(self.filepathSim, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertEquals(3, reader.FRan)
        self.assertEquals(1, reader.FDeds)
        self.assertEquals(5, reader.FTotalCross)
        self.assertEquals(5, reader.FPartialCross)
        self.assertEquals(1, reader.FCosDirect)
        self.assertEquals(3, reader.FSecIon)
        self.assertEquals(0, reader.FPotMoy)

        self.assertEquals(10, reader.max_secondary_order)
        self.assertAlmostEquals(0.05, reader.Min_Energy_Nosec)
        self.assertAlmostEquals(0.0004, reader.Residual_Energy_Loss)
        self.assertAlmostEquals(-1, reader.Min_Energy_With_Sec)
        self.assertAlmostEquals(-1, reader.Min_Gen_Secondary_Energy)

        reader = OptionsPhysic.OptionsPhysic()
        file = open(self.filepathCas, 'rb')
        error = reader.read(file)

        self.assertEquals(None, error)
        self.assertEquals(30107002, reader._version)
        self.assertEquals(3, reader.FRan)
        self.assertEquals(1, reader.FDeds)
        self.assertEquals(5, reader.FTotalCross)
        self.assertEquals(5, reader.FPartialCross)
        self.assertEquals(1, reader.FCosDirect)
        self.assertEquals(3, reader.FSecIon)
        self.assertEquals(0, reader.FPotMoy)

        self.assertEquals(10, reader.max_secondary_order)
        self.assertAlmostEquals(0.05, reader.Min_Energy_Nosec)
        self.assertAlmostEquals(0.0004, reader.Residual_Energy_Loss)
        self.assertAlmostEquals(-1, reader.Min_Energy_With_Sec)
        self.assertAlmostEquals(-1, reader.Min_Gen_Secondary_Energy)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
