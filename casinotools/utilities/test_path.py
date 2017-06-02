#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.utilities.test_path

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.utilities.path`.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import unittest
import os.path
from tempfile import TemporaryFile, SpooledTemporaryFile

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.

# Project modules.
import casinotools.utilities.path as path


# Globals and constants variables.

class TestPath(unittest.TestCase):
    """
    TestCase class for the module `casinotools.utilities.path`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.create_git_lfs_file()

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

    def create_git_lfs_file(self):
        self.git_lfs_file = TemporaryFile("w+t")
        self.git_lfs_file.write("version https://git-lfs.github.com/spec/v1\n")
        self.git_lfs_file.write("oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1258daaa5e2ca24d17e2393\n")
        self.git_lfs_file.write("size 12345\n")
        self.git_lfs_file.write("\n")
        self.git_lfs_file.seek(0)

    def test_is_git_lfs_file_bad(self):
        file_path = resource_filename(__name__, "test_path.py")
        if not os.path.isfile(file_path):
            raise SkipTest
        self.assertEqual(False, path.is_git_lfs_file(file_path))

        #self.fail("Test if the testcase is working.")

    def test_is_git_lfs_file_good(self):
        self.assertEqual(True, path.is_git_lfs_file(self.git_lfs_file))

        #self.fail("Test if the testcase is working.")

    def test_is_bad_file(self):
        file_path = resource_filename(__name__, "test_path.py")
        if not os.path.isfile(file_path):
            raise SkipTest
        self.assertEqual(False, path.is_bad_file(file_path))

        #self.fail("Test if the testcase is working.")

    def test_is_bad_file_git_lfs(self):
        self.assertEqual(True, path.is_bad_file(self.git_lfs_file))

        #self.fail("Test if the testcase is working.")

    def test_is_bad_file_no_file(self):
        file_path = resource_filename(__name__, "../../test_data/this_file_does_not_exist.txt")
        self.assertEqual(True, path.is_bad_file(file_path))

        #self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose

    nose.runmodule()
