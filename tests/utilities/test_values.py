#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.utilities.test_values

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.utilities.values` module.
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
import copy

# Third party modules.
import pytest
import attr
import cattr

# Local modules.

# Project modules.
from casinotools.utilities.values import Options, Varied, generate_experiments, flatten, deflatten
from casinotools.utilities.multiple_loop import combine

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
    options = Options()
    options.default()

    return options


@pytest.fixture()
def options_input_level1():
    options = Options()
    options.default()
    options.value1 = [1, 2, 3]

    return options


@pytest.fixture()
def options_input_level2():
    options = Options()
    options.default()
    options.sub_options_b.value5 = [56, 34]

    return options


@pytest.fixture()
def options_input_complex():
    options = Options()
    options.default()
    options.value1 = [1, 2, 3]
    options.sub_options_b.value5 = [56, 34]

    return options


def test_asdict(options_input):
    assert attr.asdict(options_input) == {'sub_options_a': {'value3': 3, 'value4': 4},
                                          'sub_options_b': {'value5': 5, 'value6': 6},
                                          'value1': 1, 'value2': 2}


def test_one_varied_values(options_input):
    options = copy.deepcopy(options_input)
    options.value1 = Varied([1, 2])

    experiments = generate_experiments(options)

    assert len(experiments) == 2

    options_1 = experiments[0]
    assert options_1.value1 == 1

    options_2 = experiments[1]
    assert options_2.value1 == 2


def test_cattr_structure(options_input):
    options = cattr.unstructure(options_input)

    assert options == {'sub_options_a': {'value3': 3, 'value4': 4},
                       'sub_options_b': {'value5': 5, 'value6': 6},
                       'value1': 1, 'value2': 2}

    new_options = cattr.structure(options, Options)

    assert new_options == options_input


def test_cattr_structure_modified_level1(options_input):
    options_input.value1 = 42

    options = cattr.unstructure(options_input)

    assert options == {'sub_options_a': {'value3': 3, 'value4': 4},
                       'sub_options_b': {'value5': 5, 'value6': 6},
                       'value1': 42, 'value2': 2}

    new_options = cattr.structure(options, Options)

    assert new_options == options_input

    options = Options()
    assert options != new_options
    assert options != options_input


def test_cattr_structure_modified_level2(options_input):
    options_input.sub_options_a.value3 = 42

    options = cattr.unstructure(options_input)

    assert options == {'sub_options_a': {'value3': 42, 'value4': 4},
                       'sub_options_b': {'value5': 5, 'value6': 6},
                       'value1': 1, 'value2': 2}

    new_options = cattr.structure(options, Options)
    assert new_options == options_input

    options = Options()
    options.default()
    assert options != new_options
    assert options == options_input


def test_multipleloop(options_input):
    options = flatten(cattr.unstructure(options_input))
    all_combinations, names, varied = combine(options)

    assert all_combinations == [[1, 2, 3, 4, 5, 6]]
    assert names == ['value1',
                     'value2',
                     'sub_options_a.value3',
                     'sub_options_a.value4',
                     'sub_options_b.value5',
                     'sub_options_b.value6']
    assert varied == []

    new_dict = deflatten(dict(zip(names, all_combinations[0])))

    new_options = cattr.structure(new_dict, Options)

    assert new_options == options_input


def test_multipleloop_level1(options_input_level1):
    options = flatten(cattr.unstructure(options_input_level1))
    all_combinations, names, varied = combine(options)

    assert all_combinations == [[1, 2, 3, 4, 5, 6],
                                [2, 2, 3, 4, 5, 6],
                                [3, 2, 3, 4, 5, 6]]
    assert names == ['value1', 'value2', 'sub_options_a.value3', 'sub_options_a.value4', 'sub_options_b.value5',
                     'sub_options_b.value6']
    assert varied == ['value1']

    options = Options()
    options.value1 = 1
    new_dict = deflatten(dict(zip(names, all_combinations[0])))
    new_options = cattr.structure(new_dict, Options)
    assert new_options == options

    options.value1 = 2
    new_dict = deflatten(dict(zip(names, all_combinations[1])))
    new_options = cattr.structure(new_dict, Options)
    assert new_options == options

    options.value1 = 3
    new_dict = deflatten(dict(zip(names, all_combinations[2])))
    new_options = cattr.structure(new_dict, Options)
    assert new_options == options


def test_multipleloop_level2(options_input_level2):
    options = flatten(cattr.unstructure(options_input_level2))
    all_combinations, names, varied = combine(options)

    assert all_combinations == [[1, 2, 3, 4, 56, 6],
                                [1, 2, 3, 4, 34, 6]]
    assert names == ['value1', 'value2', 'sub_options_a.value3', 'sub_options_a.value4', 'sub_options_b.value5',
                     'sub_options_b.value6']
    assert varied == ['sub_options_b.value5']

    options = Options()
    options.default()
    options.sub_options_b.value5 = 56
    new_dict = deflatten(dict(zip(names, all_combinations[0])))
    new_options = cattr.structure(new_dict, Options)
    assert new_options == options

    options.sub_options_b.value5 = 34
    new_dict = deflatten(dict(zip(names, all_combinations[1])))
    new_options = cattr.structure(new_dict, Options)
    assert new_options == options

    options = Options()
    options.default()
    assert new_options != options


# def test_multipleloop_complex(options_input_complex):
#     options = flatten(cattr.unstructure(options_input_complex))
#     all, names, varied = combine(options)
#
#     assert all == [[1, 2, 3, 4, 56, 6],
#                    [2, 2, 3, 4, 56, 6],
#                    [3, 2, 3, 4, 56, 6],
#                    [1, 2, 3, 4, 34, 6],
#                    [2, 2, 3, 4, 34, 6],
#                    [3, 2, 3, 4, 34, 6]]
#     assert names == ['value1', 'value2', 'sub_options_a.value3', 'sub_options_a.value4', 'sub_options_b.value5',
#                      'sub_options_b.value6']
#     assert varied == ['value1', 'sub_options_b.value5']
#
#     options = Options()
#     options.value1 = 1
#     options.sub_options_b.value5 = 56
#     new_dict = deflatten(dict(zip(names, all[0])))
#     new_options = cattr.structure(new_dict, Options)
#     assert new_options == options
#
#     options.value1 = 2
#     options.sub_options_b.value5 = 56
#     new_dict = deflatten(dict(zip(names, all[1])))
#     new_options = cattr.structure(new_dict, Options)
#     assert new_options == options
#
#     options.value1 = 3
#     options.sub_options_b.value5 = 56
#     new_dict = deflatten(dict(zip(names, all[2])))
#     new_options = cattr.structure(new_dict, Options)
#     assert new_options == options
#
#     options.value1 = 1
#     options.sub_options_b.value5 = 34
#     new_dict = deflatten(dict(zip(names, all[3])))
#     new_options = cattr.structure(new_dict, Options)
#     assert new_options == options
#
#     options.value1 = 2
#     options.sub_options_b.value5 = 34
#     new_dict = deflatten(dict(zip(names, all[4])))
#     new_options = cattr.structure(new_dict, Options)
#     assert new_options == options
#
#     options.value1 = 3
#     options.sub_options_b.value5 = 34
#     new_dict = deflatten(dict(zip(names, all[5])))
#     new_options = cattr.structure(new_dict, Options)
#     assert new_options == options


def test_flatten():
    options = Options()
    options.default()
    options_dict = flatten(cattr.unstructure(options))

    assert options_dict == {'value1': 1,
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
