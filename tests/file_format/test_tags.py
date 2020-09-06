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
import struct

# Third party modules.
from pkg_resources import resource_filename
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.tags import _create_tag_with_filler, limited_search_tag, find_tag, add_tag, add_tag_old, \
    _stream_search_slow, _stream_search_fast, find_tag_position
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


@pytest.fixture()
def sim_file():
    filepath = resource_filename(__name__, "../../test_data/casino3.x/v3.1/v3.1.7.2/SiSubstrateThreeLines_Points.sim")
    if is_bad_file(filepath):  # pragma: no cover
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


@pytest.mark.parametrize("tag_id, tag_ref",
                         [(b"V3.1.3.4", b"V3.1.3.4%%%%%%%"),
                          (b"V3.1.3.7",  b"V3.1.3.7%%%%%%%"),
                          (b"%SAVE_HEADER%",  b"%SAVE_HEADER%%%"),
                          ])
def test_create_tag_with_filler_length15(tag_id, tag_ref):
    tag_length = 15
    filler = b'%'

    tag = _create_tag_with_filler(tag_id, tag_length, filler)
    assert tag == tag_ref


@pytest.mark.parametrize("tag_id, tag_ref",
                         [(b"V3.1.3.4", b"V3.1.3.4%%"),
                          (b"V3.1.3.7",  b"V3.1.3.7%%"),
                          (b"%SAVE_HEADER%",  b"%SAVE_HEADER%"),
                          ])
def test_create_tag_with_filler_length10(tag_id, tag_ref):
    tag_length = 10
    filler = b'%'

    tag = _create_tag_with_filler(tag_id, tag_length, filler)
    assert tag == tag_ref


@pytest.mark.parametrize("tag_id, is_tag_found_ref",
                         [(b"V3.1.3.4", False),
                          (b"V3.1.3.7", False),
                          (b"%SAVE_HEADER%", True),
                          ])
def test_limited_search_tag(sim_file, tag_id, is_tag_found_ref):
    search_length = 1024
    is_tag_found = limited_search_tag(sim_file, tag_id, search_length)
    assert is_tag_found == is_tag_found_ref


@pytest.mark.parametrize("tag_id, is_tag_found_ref",
                         [(b"V3.1.3.4", False),
                          (b"V3.1.3.7", False),
                          (b"%SAVE_HEADER%", True),
                          ])
def test_find_tag(sim_file, tag_id, is_tag_found_ref):
    is_tag_found = find_tag(sim_file, tag_id)
    assert is_tag_found == is_tag_found_ref


@pytest.mark.parametrize("tag_id, is_tag_found_ref",
                         [(b"V3.1.3.4", False),
                          (b"V3.1.3.7", False),
                          (b"%SAVE_HEADER%", True),
                          ])
def test_stream_search_slow(sim_file, tag_id, is_tag_found_ref):
    is_tag_found = _stream_search_slow(sim_file, tag_id)
    assert is_tag_found == is_tag_found_ref


@pytest.mark.parametrize("tag_id, is_tag_found_ref",
                         [(b"V3.1.3.4", False),
                          (b"V3.1.3.7", False),
                          (b"%SAVE_HEADER%", True),
                          ])
def test_stream_search_fast(sim_file, tag_id, is_tag_found_ref):
    is_tag_found = _stream_search_fast(sim_file, tag_id)
    assert is_tag_found == is_tag_found_ref


@pytest.mark.parametrize("tag_id, tag_ref",
                         [(b"V3.1.3.4", b"V3.1.3.4%%"),
                          (b"V3.1.3.7",  b"V3.1.3.7%%"),
                          (b"%SAVE_HEADER%",  b"%SAVE_HEADER%"),
                          ])
def test_add_tag(tmpdir, tag_id, tag_ref):
    tag_length = 15
    size_int = struct.calcsize("i")
    file_path = tmpdir / "test_add_tag.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        add_tag(fp, tag_id, tag_length)
        assert fp.tell() == start_pos + size_int + tag_length + 1

    with open(file_path, 'rb') as fp:
        assert find_tag(fp, tag_id) is True
        assert find_tag(fp, tag_ref) is False


@pytest.mark.parametrize("tag_id, tag_ref",
                         [(b"V3.1.3.4", b"V3.1.3.4%%"),
                          (b"V3.1.3.7",  b"V3.1.3.7%%"),
                          (b"%SAVE_HEADER%",  b"%SAVE_HEADER%"),
                          ])
def test_add_tag_old(tmpdir, tag_id, tag_ref):
    tag_length = 15
    file_path = tmpdir / "test_add_tag.sim"
    with open(file_path, 'wb') as fp:
        start_pos = fp.tell()
        add_tag_old(fp, tag_id, tag_length)
        assert fp.tell() == start_pos + tag_length + 1

    with open(file_path, 'rb') as fp:
        assert find_tag(fp, tag_id) is True
        assert find_tag(fp, tag_ref) is False


def test_find_tag_position(filepath_cas_2_45):
    tag = b"*DZMAX%%%%%%%%%"
    with open(filepath_cas_2_45, 'rb') as file:
        assert find_tag_position(file, tag) == 98356
        assert find_tag_position(file, tag) == 689238


def test_find_tag_position_cas(filepath_cas_2_5_1_0):
    tag = b"*DZMAX%%%%%%%%%"
    with open(filepath_cas_2_5_1_0, 'rb') as file:
        assert find_tag_position(file, tag) == 50284
        assert find_tag_position(file, tag) == 1371743
        assert find_tag_position(file, tag) == 0


def test_find_tag_position_sim(filepath_sim_2_5_1_0):
    tag = b"*DZMAX%%%%%%%%%"
    with open(filepath_sim_2_5_1_0, 'rb') as file:
        assert find_tag_position(file, tag) == 0
