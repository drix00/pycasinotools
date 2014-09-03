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
import casinotools.fileformat.casino3.Element as Element
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestElement(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        file.seek(7159)
        element = Element.Element()
        element.read(file)

        self.assertEquals(30105010, element._version)
        self.assertEquals(0, element._elementID)
        self.assertAlmostEquals(0.660569621292935, element._weightFraction)
        self.assertAlmostEquals(0.372901678657074, element._atomicFraction)
        self.assertAlmostEquals(0.0, element._sigmaTElastic)
        self.assertEquals(311, element._repetition)

        self.assertEquals(6.0, element.Z)
        self.assertEquals('C', element.Nom)
        self.assertAlmostEquals(2.62, element.Rho)
        self.assertAlmostEquals(12.011, element.A)
        self.assertAlmostEquals(0.0, element.J)
        self.assertAlmostEquals(0.0, element.K_Gauvin)
        self.assertAlmostEquals(-9.584629012423031e+36, element.K_Monsel)
        self.assertAlmostEquals(1.0, element.ef)
        self.assertAlmostEquals(7.000000000000E+07, element.kf)
        self.assertAlmostEquals(15.0, element.ep)

        for index in range(3):
            self.assertAlmostEquals(0.0, element.Int_PRZ[index])
            self.assertAlmostEquals(0.0, element.Int_PRZ_ABS[index])

    def test_NUATOM(self):
        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('Ag')
        self.assertEquals(1, fnuatom)
        self.assertAlmostEquals(10.50, rho)
        self.assertEquals(47, z)
        self.assertEquals(107.868, a)
        self.assertAlmostEquals(5.5, ef)
        self.assertAlmostEquals(1.19, kf * 1.0e-8)
        self.assertAlmostEquals(15, ep)

        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('ag')
        self.assertEquals(0, fnuatom)
        self.assertAlmostEquals(0.0, rho)
        self.assertEquals(0, z)
        self.assertEquals(0.0, a)
        self.assertAlmostEquals(0.0, ef)
        self.assertAlmostEquals(0.0, kf)
        self.assertAlmostEquals(0.0, ep)

        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('V')
        self.assertEquals(1, fnuatom)
        self.assertAlmostEquals(5.8, rho)
        self.assertEquals(23, z)
        self.assertEquals(50.9415, a)
        self.assertAlmostEquals(1.0, ef)
        self.assertAlmostEquals(7.0, kf * 1.0e-7)
        self.assertAlmostEquals(21.8, ep)

        #self.fail("Test if the testcase is working.")

    def test__computeK(self):
        kRef = 7.790367583747E-01
        k = Element._computeK(5)
        self.assertAlmostEquals(kRef, k)

        kRef = 7.843098263659E-01
        k = Element._computeK(6)
        self.assertAlmostEquals(kRef, k)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
