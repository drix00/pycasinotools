#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.fileformat.casino4.test_file
   :synopsis: Tests for the module :py:mod:`casinotools.fileformat.casino4.file`
   
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.fileformat.casino4.file`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = "0.1"
__date__ = "Jun 14, 2016"
__copyright__ = "Copyright (c) 2016 Hendrix Demers"
__license__ = "Apache License Version 2"

# Standard library modules.
import unittest
import os.path
import shutil

# Third party modules.
from nose.plugins.skip import SkipTest
from pkg_resources import resource_filename #@UnresolvedImport

# Local modules.

# Project modules
import casinotools.fileformat.casino4.file as casino4_file
from casinotools.utilities.path import create_path, get_current_module_path
from casinotools.fileformat.casino4.version import CURRENT_VERSION, VERSION_4_0_0

# Globals and constants variables.

class TestFile(unittest.TestCase):
    """
    TestCase class for the module `casinotools.fileformat.casino4.file`.
    """
    
    def setUp(self):
        """
        Setup method.
        """
        
        unittest.TestCase.setUp(self)
        
        path = get_current_module_path(__file__, "../../../test_data/temp/casino4")
        self.temporary_folder = create_path(path)

        self.filepath_cpp_sim = resource_filename(__name__, "../../../test_data/casino4/cpp/version_4_0_0_0_cpp.sim.hdf5")
        self.filepath_py_sim = resource_filename(__name__, "../../../test_data/casino4/py/version_4_0_0_py.sim.hdf5")

    def tearDown(self):
        """
        Teardown method.
        """
        
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.temporary_folder, ignore_errors=True)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """
        
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_init(self):
        filepath_sim = "version_4_0_0.sim.hdf5"

        casino_file = casino4_file.File(filepath_sim)

        self.assertEqual(filepath_sim, casino_file.filepath)

        #self.fail("Test if the testcase is working.")
    
    def test_set_default_values(self):
        """
        Tests for method :py:meth:`set_default_values`.
        """
     
        casino_file = casino4_file.File(self.filepath_cpp_sim)
        
        self.assertEqual(VERSION_4_0_0, casino_file.version)
        self.assertEqual(CURRENT_VERSION, casino_file.version)
        
        #self.fail("Test if the testcase is working.")
    
    def test_open(self):
        """
        Tests for method :py:meth:`open`.
        """
        if not os.path.isfile(self.filepath_py_sim):
            raise SkipTest
     
        casino_file = casino4_file.File(self.filepath_py_sim)
        
        casino_file.open()
        
        self.assertEqual(VERSION_4_0_0, casino_file.version)
        self.assertEqual(CURRENT_VERSION, casino_file.version)
        
        #self.fail("Test if the testcase is working.")
    
    def test_getFileType(self):
        if not os.path.isfile(self.filepath_cpp_sim):
            raise SkipTest
        casino_file = casino4_file.File(self.filepath_cpp_sim)

        type = casino_file.getFileType()
        self.assertEqual(casino4_file.SIMULATION_CONFIGURATIONS, type)

#        casino_file = File.File(self.filepathCas)
#        type = casino_file.getFileType()
#        self.assertEqual(File.SIMULATION_RESULTS, type)

        self.fail("Test if the testcase is working.")

    def test__readExtension(self):
        if not os.path.isfile(self.filepath_cpp_sim):
            raise SkipTest
        casino_file = casino4_file.File(self.filepath_cpp_sim)
        file = casino_file._open(self.filepath_cpp_sim)
        extension = casino_file._readExtension(file)
        self.assertEqual(casino4_file.SIMULATION_CONFIGURATIONS, extension)

        file = open(self.filepathCas, 'rb')
        extension = casino_file._readExtension(file)
        self.assertEqual(casino4_file.SIMULATION_RESULTS, extension)

        self.fail("Test if the testcase is working.")
       
if __name__ == '__main__':  #pragma: no cover
    import nose
    import sys
    argv = sys.argv
    #argv.append("--with-coverage")
    #argv.append("--cover-package=casinotools.fileformat.casino4.file")
    nose.runmodule(argv=argv)
