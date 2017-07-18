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
import casinotools.fileformat.casino3.Element as Element
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestElement(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        file = open(self.filepathSim, 'rb')
        file.seek(7159)
        element = Element.Element()
        element.read(file)

        self.assertEqual(30105010, element._version)
        self.assertEqual(0, element._elementID)
        self.assertAlmostEqual(0.660569621292935, element._weightFraction)
        self.assertAlmostEqual(0.372901678657074, element._atomicFraction)
        self.assertAlmostEqual(0.0, element._sigmaTElastic)
        self.assertEqual(311, element._repetition)

        self.assertEqual(6.0, element.Z)
        self.assertEqual('C', element.Nom)
        self.assertAlmostEqual(2.62, element.Rho)
        self.assertAlmostEqual(12.011, element.A)
        self.assertAlmostEqual(0.0, element.J)
        self.assertAlmostEqual(0.0, element.K_Gauvin)
        self.assertAlmostEqual(-9.584629012423031e+36, element.K_Monsel)
        self.assertAlmostEqual(1.0, element.ef)
        self.assertAlmostEqual(7.000000000000E+07, element.kf)
        self.assertAlmostEqual(15.0, element.ep)

        for index in range(3):
            self.assertAlmostEqual(0.0, element.Int_PRZ[index])
            self.assertAlmostEqual(0.0, element.Int_PRZ_ABS[index])

    def test_NUATOM(self):
        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('Ag')
        self.assertEqual(1, fnuatom)
        self.assertAlmostEqual(10.50, rho)
        self.assertEqual(47, z)
        self.assertEqual(107.868, a)
        self.assertAlmostEqual(5.5, ef)
        self.assertAlmostEqual(1.19, kf * 1.0e-8)
        self.assertAlmostEqual(15, ep)

        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('ag')
        self.assertEqual(0, fnuatom)
        self.assertAlmostEqual(0.0, rho)
        self.assertEqual(0, z)
        self.assertEqual(0.0, a)
        self.assertAlmostEqual(0.0, ef)
        self.assertAlmostEqual(0.0, kf)
        self.assertAlmostEqual(0.0, ep)

        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('V')
        self.assertEqual(1, fnuatom)
        self.assertAlmostEqual(5.8, rho)
        self.assertEqual(23, z)
        self.assertEqual(50.9415, a)
        self.assertAlmostEqual(1.0, ef)
        self.assertAlmostEqual(7.0, kf * 1.0e-7)
        self.assertAlmostEqual(21.8, ep)

        #self.fail("Test if the testcase is working.")

    def test__computeK(self):
        kRef = 7.790367583747E-01
        k = Element._computeK(5)
        self.assertAlmostEqual(kRef, k)

        kRef = 7.843098263659E-01
        k = Element._computeK(6)
        self.assertAlmostEqual(kRef, k)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
