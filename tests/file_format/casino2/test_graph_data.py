#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino2.test_graph_data
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino2.graph_data` module.
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
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino2.graph_data import GraphData

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


@pytest.mark.skip(reason="this test does not work")
def test_read(filepath_cas_2_45):
    """
    .. todo:: Make this test work.

    :param filepath_cas_2_45:
    :return:
    """
    with open(filepath_cas_2_45, 'rb') as file:
        file.seek(2013179)

        results = GraphData(file=file)
        assert results._version == 30105020

        assert results._size == 1000
        assert results._borneInf == pytest.approx(0.0)
        assert results._borneSup == pytest.approx(8.900000000000E+01)
        assert results._isLog == 0
        assert results._isUneven == 0

        assert results._title == "z Max"
        assert results._xTitle == "Depth (nm)"
        assert results._yTitle == "Hits (Normalized)"

        assert results._values[0] == pytest.approx(1.0)
        assert results._values[-1] == pytest.approx(0.0)
