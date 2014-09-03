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
import casinotools.fileformat.casino3.Trajectory as Trajectory
import casinotools.fileformat.test_FileReaderWriterTools as test_FileReaderWriterTools

# Globals and constants variables.

class TestTrajectory(test_FileReaderWriterTools.TestFileReaderWriterTools):

    def test_read(self):
        results = Trajectory.Trajectory()
        file = open(self.filepathCas, 'rb')
        file.seek(4042541)

        self.assertTrue(file is not None)
        error = results.read(file)
        self.assertEquals(None, error)
        version = results.getVersion()
        self.assertEquals(30105012, version)

        self.assertEquals(256, results._type)

        self.assertEquals(1, results._order)
        self.assertAlmostEquals(-3.071803288788E-01, results._dirX)
        self.assertAlmostEquals(8.927911784036E-02, results._dirY)
        self.assertAlmostEquals(9.474542124386E-01, results._dirZ)
        self.assertEquals(28, results._numberScatteringEvents)

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
