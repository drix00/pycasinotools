#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.utilities.test_values2
.. moduleauthor:: Hendrix Demers <Demers.Hendrix@hydro.qc.ca>

Tests for the :py:mod:`casinotools.utilities.values2` module.
"""


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

# Standard library modules.
from dataclasses import asdict, replace

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.utilities.values2 import Options, Varied, generate_experiments, flatten, deflatten
from casinotools.utilities.multipleloop import combine

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


@pytest.fixture()
def options_input():
    options_input = Options()

    return options_input


@pytest.fixture()
def options_input_level1():
    options_input = Options()

    options_input.value1 = [1, 2, 3]

    return options_input


@pytest.fixture()
def options_input_level2(options_input_level1):
    options_input = Options()

    options_input.sub_options_b.value5 = [56, 34]

    return options_input


def test_one_varied_values(options_input):
    options_input.value1 = Varied([1, 2])

    experiments = generate_experiments(options_input)

    assert len(experiments) == 2

    options_1 = experiments[0]
    assert options_1.value1 == 1

    options_2 = experiments[1]
    assert options_2.value1 == 2


def test_asdict(options_input):
    assert asdict(options_input) == {'sub_options_a': {'value3': 3, 'value4': 4},
                                     'sub_options_b': {'value5': 5, 'value6': 6},
                                     'value1': 1, 'value2': 2}


def test_multipleloop(options_input):
    options = flatten(asdict(options_input))
    all, names, varied = combine(options)

    assert all == [[1, 2, 3, 4, 5, 6]]
    assert names == ['value1',
                     'value2',
                     'sub_options_a.value3',
                     'sub_options_a.value4',
                     'sub_options_b.value5',
                     'sub_options_b.value6']
    assert varied == []

    new_dict = deflatten(dict(zip(names, all[0])))

    
    new_options = Options(**new_dict)

    assert new_options == options_input


def test_multipleloop_level1(options_input_level1):
    options = flatten(asdict(options_input))
    all, names, varied = combine(options)

    assert all == [['value3', 'value5', 1, 2],
                   ['value4', 'value5', 1, 2],
                   ['value3', 'value6', 1, 2],
                   ['value4', 'value6', 1, 2],
                   ['value3', 'value5', 2, 2],
                   ['value4', 'value5', 2, 2],
                   ['value3', 'value6', 2, 2],
                   ['value4', 'value6', 2, 2],
                   ['value3', 'value5', 3, 2],
                   ['value4', 'value5', 3, 2],
                   ['value3', 'value6', 3, 2],
                   ['value4', 'value6', 3, 2]]
    assert names == ['sub_options_a', 'sub_options_b', 'value1', 'value2']
    assert varied == ['value1']


def test_flatten(options_input):
    options = flatten(asdict(options_input))

    assert options == {'value1': 1,
                       'value2': 2,
                       'sub_options_a.value3': 3,
                       'sub_options_a.value4': 4,
                       'sub_options_b.value5': 5,
                       'sub_options_b.value6': 6}


def test_deflatten():
    options = {'value1': 1,
                'value2': 2,
                'sub_options_a.value3': 3,
                'sub_options_a.value4': 4,
                'sub_options_b.value5': 5,
                'sub_options_b.value6': 6}

    new_options = deflatten(options)
    assert new_options == {'sub_options_a': {'value3': 3, 'value4': 4},
                           'sub_options_b': {'value5': 5, 'value6': 6},
                           'value1': 1, 'value2': 2}
