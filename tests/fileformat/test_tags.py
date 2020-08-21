#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.fileformat.test_tags
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.fileformat.tags` module.
"""

###############################################################################
# Copyright 2020 Hendrix Demers
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

# Third party modules.
from pkg_resources import resource_filename
import pytest

# Local modules.

# Project modules.
from casinotools.fileformat.tags import create_tag_with_filler, limited_search_tag, search_tag
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


class TestTags(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        filepath = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
        if is_bad_file(filepath):
            pytest.skip()
        self.file = open(filepath, 'rb')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_createTagWithFiller(self):
        tag_ids = [b"V3.1.3.4", b"V3.1.3.7", b"%SAVE_HEADER%"]

        tag_length = 15
        filler = b'%'

        tag_refs = [b"V3.1.3.4%%%%%%%", b"V3.1.3.7%%%%%%%", b"%SAVE_HEADER%%%"]

        for tagID, tagRef in zip(tag_ids, tag_refs):
            tag = create_tag_with_filler(tagID, tag_length, filler)

            self.assertEqual(tagRef, tag)

        tag_length = 10
        tag_refs = [b"V3.1.3.4%%", b"V3.1.3.7%%", b"%SAVE_HEADER%"]

        for tagID, tagRef in zip(tag_ids, tag_refs):
            tag = create_tag_with_filler(tagID, tag_length, filler)

            self.assertEqual(tagRef, tag)

    def test_limitedSearchTag(self):
        search_length = 1024

        tag_ids = [b"V3.1.3.4", b"V3.1.3.7", b"%SAVE_HEADER%"]

        is_tag_founds = [False, False, True]

        for tagID, isTagFoundRef in zip(tag_ids, is_tag_founds):
            is_tag_found = limited_search_tag(self.file, tagID, search_length)

            self.assertEqual(isTagFoundRef, is_tag_found)

    def test_searchTag(self):
        tag_ids = [b"V3.1.3.4", b"V3.1.3.7", b"%SAVE_HEADER%"]

        is_tag_founds = [False, False, True]

        for tagID, isTagFoundRef in zip(tag_ids, is_tag_founds):
            is_tag_found = search_tag(self.file, tagID)

            self.assertEqual(isTagFoundRef, is_tag_found)
