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
import casinotools.fileformat.casino2.Trajectory as Trajectory
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestTrajectory(test_File.TestFile):

    def test_read(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        with open(self.filepathCas, 'rb') as file:
            self._read_tests(file)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathCas):
            raise SkipTest
        f = open(self.filepathCas, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(196464)
        trajectory = Trajectory.Trajectory()
        trajectory.read(file)

        self.assertEqual(0, trajectory.FRetro)
        self.assertEqual(0, trajectory.FTrans)
        self.assertEqual(0, trajectory.FDetec)
        self.assertEqual(88, trajectory.NbColl)

        self.assertAlmostEqual(1.373841228321E+02, trajectory.Zmax)
        self.assertAlmostEqual(0.0, trajectory.LPM)
        self.assertAlmostEqual(-2.794824207165E-02, trajectory.DedsM)
        self.assertAlmostEqual(3.281595883225E+00, trajectory.PhiM)
        self.assertAlmostEqual(2.596906806472E-01, trajectory.ThetaM)
        self.assertAlmostEqual(-3.785237138949E+01, trajectory.MoyenX)
        self.assertAlmostEqual(-2.676401848051E+01, trajectory.MoyenY)
        self.assertAlmostEqual(1.070857314139E+02, trajectory.MoyenZ)

        self.assertEqual(1, trajectory.Display)
        self.assertEqual(89, trajectory.NbElec)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
