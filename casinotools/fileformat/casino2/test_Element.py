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

# Local modules.
import casinotools.fileformat.casino2.Element as Element
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestElement(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathSim, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(0)
        element = Element.Element()
        element.read(file, 500)
        self.assertEquals(49953, file.tell())

        self.assertEquals(5, element.Z)
        self.assertEquals('B', element.Nom)
        self.assertAlmostEquals(2.340000000000E+00, element.Rho)
        self.assertAlmostEquals(1.081000000000E+01, element.A)
        self.assertAlmostEquals(5.750000000000E-02, element.J)
        self.assertAlmostEquals(7.790367583747E-01, element.K)
        self.assertAlmostEquals(1.0, element.ef)
        self.assertAlmostEquals(7.000000000000E+07, element.kf)
        self.assertAlmostEquals(2.270000000000E+01, element.ep)

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
