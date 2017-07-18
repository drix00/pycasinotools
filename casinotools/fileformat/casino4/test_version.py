#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.fileformat.casino4.test_version
   :synopsis: Tests for the module :py:mod:`casinotools.fileformat.casino4.version`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.fileformat.casino4.version`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = "0.1"
__date__ = "Jun 22, 2016"
__copyright__ = "Copyright (c) 2016 Hendrix Demers"
__license__ = "Apache License Version 2"

# Standard library modules.
import unittest
from pkg_resources import resource_filename #@UnresolvedImport
import os.path

# Third party modules.
import h5py
from nose import SkipTest

# Local modules.

# Project modules
from casinotools.fileformat.casino4.version import Version
from casinotools.fileformat.casino4.version import CURRENT_VERSION, VERSION_4_0_0

# Globals and constants variables.

class TestVersion(unittest.TestCase):
    """
    TestCase class for the module `Version`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

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
        self.assert_(True)

    def test_to_string(self):
        """
        Tests for method `toString`.
        """

        version =  Version(1, 2, 3, 4)
        stringRef = "1.2.3.4"
        versionString = version.to_string()
        self.assertEquals(stringRef, versionString)

        version =  Version(1, 2, 3, 4)
        stringRef = "1_2_3_4"
        versionString = version.to_string('_')
        self.assertEquals(stringRef, versionString)

        #self.fail("Test if the testcase is working.")

    def test_from_string(self):
        """
        Tests for method `fromString`.
        """

        version =  Version(1, 2, 3, 4)
        stringRef = "5.6.7.8"
        version.from_string(stringRef)
        versionString = version.to_string()
        self.assertEquals(stringRef, versionString)

        self.assertEquals(5, version.major)
        self.assertEquals(6, version.minor)
        self.assertEquals(7, version.revision)
        self.assertEquals(8, version.build)

        #self.fail("Test if the testcase is working.")

    def test_VersionConstants(self):
        """
        Tests for method `VersionConstants`.
        """

        stringRef = "4.0.0.0"
        versionString = VERSION_4_0_0.to_string()
        self.assertEquals(stringRef, versionString)
        self.assertEquals(4, VERSION_4_0_0.major)
        self.assertEquals(0, VERSION_4_0_0.minor)
        self.assertEquals(0, VERSION_4_0_0.revision)
        self.assertEquals(0, VERSION_4_0_0.build)

        self.assertEquals(VERSION_4_0_0, CURRENT_VERSION)

        #self.fail("Test if the testcase is working.")

    def test_comparison(self):
        """
        Test comparison operation on Version class.
        """
        self.assertTrue(VERSION_4_0_0 == VERSION_4_0_0)
        self.assertFalse(VERSION_4_0_0 != VERSION_4_0_0)
        self.assertFalse(VERSION_4_0_0 > VERSION_4_0_0)
        self.assertTrue(VERSION_4_0_0 >= VERSION_4_0_0)
        self.assertFalse(VERSION_4_0_0 < VERSION_4_0_0)
        self.assertTrue(VERSION_4_0_0 <= VERSION_4_0_0)

        #self.fail("Test if the testcase is working.")

    def test_current_version(self):
        """
        Tests for method for the `CURRENT_VERSION`.
        """

        self.assertEquals(CURRENT_VERSION, VERSION_4_0_0)

        #self.fail("Test if the testcase is working.")

    def test_read_write(self):
        """
        Tests for methods :py:meth:`read` and :py:meth:`write`.
        """

        hdf5_file = h5py.File("test_read_write.hdf5", 'w', driver="core", backing_store=False)

        version_ref =  Version(1, 2, 3, 4)
        version_ref.write(hdf5_file)
        self.assertEqual(Version(1, 2, 3, 4), version_ref)
        self.assertNotEqual(CURRENT_VERSION, version_ref)

        version = Version(4, 0, 0, 0)
        self.assertEqual(VERSION_4_0_0, version)
        version.read(hdf5_file)
        self.assertEqual(version_ref, version)
        self.assertNotEqual(VERSION_4_0_0, version)

        #self.fail("Test if the testcase is working.")

    def test_bad_read(self):
        """
        Tests for method :py:meth:`bad_read`.
        """
        hdf5_file = h5py.File("test_read_write.hdf5", 'w', driver="core", backing_store=False)

        version_ref =  Version(1, 2, 3, 4)
        version = Version(4, 0, 0, 0)
        self.assertEqual(VERSION_4_0_0, version)

        self.assertRaises(KeyError, version.read, hdf5_file)

        self.assertNotEqual(version_ref, version)
        self.assertEqual(VERSION_4_0_0, version)

        #self.fail("Test if the testcase is working.")

    def test_bad_write(self):
        """
        Tests for method :py:meth:`bad_write`.
        """
        filepath_py_sim = resource_filename(__name__, "../../../test_data/casino4/py/version_4_0_0_py.sim.hdf5")
        if not os.path.exists(filepath_py_sim):
            raise SkipTest

        hdf5_file = h5py.File(filepath_py_sim, 'r', driver="core", backing_store=False)

        version_ref =  Version(1, 2, 3, 4)

        self.assertRaises(OSError, version_ref.write, hdf5_file)

        self.assertEqual(Version(1, 2, 3, 4), version_ref)
        self.assertNotEqual(CURRENT_VERSION, version_ref)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.runmodule()
