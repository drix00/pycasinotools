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
import casinotools.fileformat.casino2.Trajectory as Trajectory
import casinotools.fileformat.casino2.test_File as test_File

# Globals and constants variables.

class TestTrajectory(test_File.TestFile):

    def test_read(self):
        file = open(self.filepathCas, 'rb')
        self._read_tests(file)

    def test_read_StringIO(self):
        f = open(self.filepathCas, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file)

    def _read_tests(self, file):
        file.seek(196464)
        trajectory = Trajectory.Trajectory()
        trajectory.read(file)

        self.assertEquals(0, trajectory.FRetro)
        self.assertEquals(0, trajectory.FTrans)
        self.assertEquals(0, trajectory.FDetec)
        self.assertEquals(88, trajectory.NbColl)

        self.assertAlmostEquals(1.373841228321E+02, trajectory.Zmax)
        self.assertAlmostEquals(0.0, trajectory.LPM)
        self.assertAlmostEquals(-2.794824207165E-02, trajectory.DedsM)
        self.assertAlmostEquals(3.281595883225E+00, trajectory.PhiM)
        self.assertAlmostEquals(2.596906806472E-01, trajectory.ThetaM)
        self.assertAlmostEquals(-3.785237138949E+01, trajectory.MoyenX)
        self.assertAlmostEquals(-2.676401848051E+01, trajectory.MoyenY)
        self.assertAlmostEquals(1.070857314139E+02, trajectory.MoyenZ)

        self.assertEquals(1, trajectory.Display)
        self.assertEquals(89, trajectory.NbElec)

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
