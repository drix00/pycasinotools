#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule::

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>


"""

# Copyright 2019 Hendrix Demers
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

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.utilities.values import generate_experiments, Varied, has_varied_value, VariedOptions

# Globals and constants variables.


def test_one_varied_values(options_input):
    options_input.value1 = Varied([1, 2])

    experiments = generate_experiments(options_input)

    assert len(experiments) == 2

    options_1 = experiments[0]
    assert options_1.value1 == 1

    options_2 = experiments[1]
    assert options_2.value1 == 2


def test_two_varied_values(options_input):
    options_input.value1 = Varied([1, 2])
    options_input.value2 = Varied([3, 4])

    experiments = generate_experiments(options_input)

    assert len(experiments) == 4

    options_1 = experiments[0]
    assert options_1.value1 == 1
    assert options_1.value2 == 3

    options_2 = experiments[1]
    assert options_2.value1 == 1
    assert options_2.value2 == 4

    options_3 = experiments[2]
    assert options_3.value1 == 2
    assert options_3.value2 == 3

    options_4 = experiments[3]
    assert options_4.value1 == 2
    assert options_4.value2 == 4


def test_one_sub_varied_values(options_input):
    options_input.sub_options_a.value3 = Varied([1, 2])

    experiments = generate_experiments(options_input)

    assert len(experiments) == 2

    options_1 = experiments[0]
    assert options_1.value1 == 1

    options_2 = experiments[1]
    assert options_2.value1 == 2


def test_has_varied_value(options_input):
    assert has_varied_value(options_input) is False

    options_input.value1 = Varied([1, 2])
    assert has_varied_value(options_input) is True


def test_has_sub_varied_value(options_input):
    assert has_varied_value(options_input) is False

    options_input.sub_options_a.value3 = Varied([1, 2])
    assert has_varied_value(options_input) is True


@pytest.fixture()
def options_input():
    class SubOptionsA:
        def __init__(self):
            self.value3 = 3
            self.value4 = 4

    class SubOptionsB:
        def __init__(self):
            self.value5 = 5
            self.value6 = 6

    class Options:
        def __init__(self):
            self.value1 = 1
            self.value2 = 2

            self.sub_options_a = SubOptionsA()
            self.sub_options_b = SubOptionsB()

    options_input = Options()

    return options_input
