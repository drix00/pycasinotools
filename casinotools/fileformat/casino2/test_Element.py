#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
try:
    from io import BytesIO
except ImportError: # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.Element as Element
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestElement(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        element = Element.Element()
        element.read(file, 500)
        self.assertEqual(49953, file.tell())

        self.assertEqual(5, element.Z)
        self.assertEqual('B', element.Nom)
        self.assertAlmostEqual(2.340000000000E+00, element.Rho)
        self.assertAlmostEqual(1.081000000000E+01, element.A)
        self.assertAlmostEqual(5.750000000000E-02, element.J)
        self.assertAlmostEqual(7.790367583747E-01, element.K)
        self.assertAlmostEqual(1.0, element.ef)
        self.assertAlmostEqual(7.000000000000E+07, element.kf)
        self.assertAlmostEqual(2.270000000000E+01, element.ep)

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
