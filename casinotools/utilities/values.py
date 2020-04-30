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
import copy
from collections.abc import Sequence, Iterable

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


def list_all_variables(options_input):
    print(options_input.__dict__)
    for variable in options_input.__dict__:
        value = options_input.__dict__[variable]

        print(variable, value, type(value))


def loop_variables(experiments):
    if has_varied_value(experiments):
        total_experiments = []
        for experiment in experiments:
            options_input = copy.deepcopy(experiment)
            print(options_input.__dict__)
            for variable in options_input.__dict__:
                # if isinstance(variable, VariedOptions):
                value = options_input.__dict__[variable]

                if hasattr(value, "is_varied"):
                    new_experiments = []
                    for item in value:
                        options = copy.deepcopy(options_input)
                        setattr(options, variable, item)
                        new_experiments.append(options)

                    total_experiments.extend(new_experiments)
                    break

        total_experiments = loop_variables(total_experiments)
    else:
        total_experiments = experiments

    return total_experiments


def has_varied_value(experiments):
    if not isinstance(experiments, Iterable):
        experiments = [experiments]

    for experiment in experiments:
        for variable in experiment.__dict__:
            value = experiment.__dict__[variable]

            if hasattr(value, "is_varied"):
                return True
    return False


def generate_experiments(options_input):
    options = copy.deepcopy(options_input)
    experiments = [options]

    experiments = loop_variables(experiments)

    return experiments


def multiple_values():
    pass


class Varied(Sequence):
    def __init__(self, values):
        self.is_varied = True
        self.values = values

    def __getitem__(self, index):
        return self.values[index]

    def __len__(self):
        len(self.values)


class VariedOptions:
    is_varied = False


if __name__ == '__main__':  # pragma: no cover
    import inspect

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
    options_input.value1 = Varied([1, 2])
    options_input.sub_options_a.value4 = Varied([-1, -2])

    print(getattr(options_input, 'value2'))
    print(vars(options_input))
    parent_name = options_input.__class__.__name__
    members = inspect.getmembers(options_input)
    # print(members)
    for name, value in members:
        if not name.startswith("__") and not inspect.isbuiltin(value) and not inspect.isroutine(value):
            print("{}.{}".format(parent_name, name))
            inner_members = inspect.getmembers(value)
            for inner_name, inner_value in inner_members:
                if not inner_name.startswith("__") and not inspect.isbuiltin(inner_value) and not inspect.isroutine(value):
                    print("{}.{}.{}".format(parent_name, name, inner_name))

    # experiments = generate_experiments(options_input)
    #
    # assert len(experiments) == 4
    #
    # options_1 = experiments[0]
    # assert options_1.value1 == 1
    # assert options_1.sub_options_a.value4 == -1
    #
    # options_2 = experiments[1]
    # assert options_2.value1 == 2
    # assert options_1.sub_options_a.value4 == -1
    #
    # options_3 = experiments[2]
    # assert options_1.value1 == 1
    # assert options_1.sub_options_a.value4 == -2
    #
    # options_4 = experiments[3]
    # assert options_2.value1 == 2
    # assert options_1.sub_options_a.value4 == -2
