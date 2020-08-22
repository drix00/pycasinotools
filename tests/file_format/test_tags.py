#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.test_tags
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.tags` module.
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

# Third party modules.
from pkg_resources import resource_filename
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.tags import create_tag_with_filler, limited_search_tag, search_tag
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


@pytest.fixture()
def sim_file():
    filepath = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
    if is_bad_file(filepath):
        pytest.skip("Bad file for test")

    file = open(filepath, 'rb')
    return file


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_create_tag_with_filler():
    tag_ids = [b"V3.1.3.4", b"V3.1.3.7", b"%SAVE_HEADER%"]

    tag_length = 15
    filler = b'%'

    tag_refs = [b"V3.1.3.4%%%%%%%", b"V3.1.3.7%%%%%%%", b"%SAVE_HEADER%%%"]

    for tag_id, tag_ref in zip(tag_ids, tag_refs):
        tag = create_tag_with_filler(tag_id, tag_length, filler)

        assert tag == tag_ref

    tag_length = 10
    tag_refs = [b"V3.1.3.4%%", b"V3.1.3.7%%", b"%SAVE_HEADER%"]

    for tag_id, tag_ref in zip(tag_ids, tag_refs):
        tag = create_tag_with_filler(tag_id, tag_length, filler)

        assert tag == tag_ref


def test_limited_search_tag(sim_file):
    search_length = 1024

    tag_ids = [b"V3.1.3.4", b"V3.1.3.7", b"%SAVE_HEADER%"]

    is_tag_founds = [False, False, True]

    for tag_id, is_tag_found_ref in zip(tag_ids, is_tag_founds):
        is_tag_found = limited_search_tag(sim_file, tag_id, search_length)

        assert is_tag_found == is_tag_found_ref


def test_search_tag(sim_file):
    tag_ids = [b"V3.1.3.4", b"V3.1.3.7", b"%SAVE_HEADER%"]

    is_tag_founds = [False, False, True]

    for tag_id, is_tag_found_ref in zip(tag_ids, is_tag_founds):
        is_tag_found = search_tag(sim_file, tag_id)

        assert is_tag_found == is_tag_found_ref
