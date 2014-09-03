#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.examples.casino3.test_AnalyseTransmittedElectrons
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Test for module AnalyseTransmittedElectrons.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest
import os.path

# Third party modules.

# Local modules.

# Project modules
from  casinotools.utilities.path import get_current_module_path
import AnalyseTransmittedElectrons

# Globals and constants variables.

class TestAnalyseTransmittedElectrons(unittest.TestCase):
    """
    TestCase class for the module `AnalyseTransmittedElectrons`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.filepath = get_current_module_path(__file__, "../../../testdata/examples/casino3/WaterAuTop_wSE.cas")
        self.analyze = AnalyseTransmittedElectrons.TransmittedElectrons(None)

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        #self.fail("Test if the testcase is working.")

    def test__readFile(self):
        self.assertTrue(os.path.isfile(self.filepath))

        self.analyze._readFile(self.filepath)

        for result in self.analyze._results.values():
            self.assertEquals(1, result.getNumberSimulations())
            self.assertEquals(1, len(result._simulations))

        #self.fail("Test if the testcase is working.")

    def test__extractNameFromFilepath(self):
        nameRef = "WaterAuTop_wSE"
        name = self.analyze._extractNameFromFilepath(self.filepath)

        self.assertEquals(nameRef, name)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
