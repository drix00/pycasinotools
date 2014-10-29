#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest

# Third party modules.

# Local modules.

# Project modules
import _parameters

# Globals and constants variables.

class TestParameters(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_NoneFilepath(self):
        parameters = _parameters.Parameters(None)
        self.assertEquals(0, len(parameters))

        #self.fail("Test if the testcase is working.")

    def test_EmptyFilepath(self):
        parameters = _parameters.Parameters("")
        self.assertEquals(0, len(parameters))

        #self.fail("Test if the testcase is working.")

    def test_BadFilepath(self):
        parameters = _parameters.Parameters(None)
        filepath = "DiscreteTomography_testDataGoldinCarbon"
        self.assertRaises(ValueError, parameters._extractFromFilepath, filepath)

        #self.fail("Test if the testcase is working.")

    def test__extractFromFilepath(self):
        parameters = _parameters.Parameters(None)

        filepath = "DataSetBatenburg_GoldinCarbon_Center_X_T500nm_tiltY+0.0deg_woSE_XY_w520nm_h50nm_13000pts_E200.0keV_br0.50nm_a2.0mrad_N50ke.cas"
        parameters._extractFromFilepath(filepath)
        self.assertEquals(15, len(parameters))

        self.assertEquals("DataSetBatenburg", parameters[parameters.KEY_SIMULATION_NAME])
        self.assertEquals("GoldinCarbon", parameters[parameters.KEY_SAMPLE_NAME])
        self.assertEquals("Center", parameters[parameters.KEY_SAMPLE_POSITION])
        self.assertEquals("X", parameters[parameters.KEY_SAMPLE_ORIENTATION])
        self.assertEquals("500", parameters[parameters.KEY_SAMPLE_THICKNESS])
        self.assertEquals("+0.0", parameters[parameters.KEY_TILT_Y])
        self.assertEquals("woSE", parameters[parameters.KEY_SECONDARY_ELECTRON])
        self.assertEquals("XY", parameters[parameters.KEY_LINESCAN_DIRECTION])
        self.assertEquals("520", parameters[parameters.KEY_LINESCAN_WIDTH])
        self.assertEquals("50", parameters[parameters.KEY_LINESCAN_HEIGHT])
        self.assertEquals("13000", parameters[parameters.KEY_LINESCAN_NUMBER_POINTS])
        self.assertEquals("200.0", parameters[parameters.KEY_ENERGY])
        self.assertEquals("0.50", parameters[parameters.KEY_BEAM_RADIUS])
        self.assertEquals("2.0", parameters[parameters.KEY_BEAM_SEMI_ANGLE])
        self.assertEquals("50k", parameters[parameters.KEY_NUMBER_ELECTRONS])

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.main()
