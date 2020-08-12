#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.utilities.values

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>


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
import collections
import copy
from typing import Sequence, Iterable

# Third party modules.
import attr

# Local modules.

# Project modules.

# Globals and constants variables.


@attr.s
class SubOptionsA:
    value3 = attr.ib(default=3)
    value4 = attr.ib(default=4)


@attr.s
class SubOptionsB:
    value5 = attr.ib(default=5)
    value6 = attr.ib(default=6)


@attr.s
class Options:
    value1 = attr.ib(default=1)
    value2 = attr.ib(default=2)

    sub_options_a: SubOptionsA = attr.ib(default=SubOptionsA(3, 4))
    sub_options_b: SubOptionsB = attr.ib(default=SubOptionsB(5, 6))

    def default(self):
        self.value1 = 1
        self.value2 = 2

        # self.sub_options_a = SubOptionsA()
        self.sub_options_a.value3 = 3
        self.sub_options_a.value4 = 4

        # self.sub_options_b = SubOptionsB()
        self.sub_options_b.value5 = 5
        self.sub_options_b.value6 = 6


class Varied(Sequence):
    def __init__(self, values):
        self.is_varied = True
        self.values = values

    def __getitem__(self, index):
        return self.values[index]

    def __len__(self):
        len(self.values)


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


def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def deflatten(d, parent_key='', sep='.'):
    new_dict = {}
    for k, v in d.items():
        keys = k.split(sep)
        temp_dict = new_dict
        for key in keys[:-1]:
            temp_dict.setdefault(key, {})
            temp_dict = temp_dict[key]
        temp_dict[keys[-1]] = v

    return new_dict
