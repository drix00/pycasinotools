#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.utilities.multipleloop

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>


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

# Local modules.

# Project modules.

# Globals and constants variables.


def _outer(a, b):
    """
    Return the outer product/combination of two lists.
    a is a multi- or one-dimensional list,
    b is a one-dimensional list, tuple, NumPy array or scalar (new parameter)
    Return:  outer combination 'all'.

    The function is to be called repeatedly::

        all_combination = _outer(all_combination, p)
    """
    all_combination = []
    if not isinstance(a, list):
        raise TypeError('a must be a list')
    if isinstance(b, (float, int, complex, str)):
        b = [b]  # scalar?

    if len(a) == 0:
        # first call:
        for j in b:
            all_combination.append([j])
    else:
        for j in b:
            for i in a:
                if not isinstance(i, list):
                    raise TypeError('a must be list of list')
                # note: i refers to a list; i.append(j) changes
                # the underlying list (in a), which is not what
                # we want, we need a copy, extend the copy, and
                # add to all
                k = i + [j]  # extend previous parameters with new one
                all_combination.append(k)
    return all_combination


def combine(prm_values):
    """
    Compute the combination of all parameter values in the prm_values
    (nested) list. Main function in this module.

    param prm_values: nested list ``(parameter_name, list_of_parameter_values)``
    or dictionary ``prm_values[parameter_name] = list_of_parameter_values``.
    return: (all, names, varied) where

      - all contains all combinations (experiments)
        all[i] is the list of individual parameter values in
        experiment no i

      - names contains a list of all parameter names

      - varied holds a list of parameter names that are varied
        (i.e. where there is more than one value of the parameter,
        the rest of the parameters have fixed values)


    Code example:

    >>> from numpy import array
    >>> dx = array([1.0/2**k for k in range(2, 5)])
    >>> dt = 3*dx;  dt = dt[:-1]
    >>> p = {'dx': dx, 'dt': dt}
    >>> p
    {'dt': [ 0.75 , 0.375,], 'dx': [ 0.25  , 0.125 , 0.0625,]}
    >>> all_combination, names, varied = combine(p)
    >>> all_combination
    [[0.75, 0.25], [0.375, 0.25], [0.75, 0.125], [0.375, 0.125],
     [0.75, 0.0625], [0.375, 0.0625]]
    """
    if isinstance(prm_values, dict):
        # turn dict into list [(name,values),(name,values),...]:
        prm_values = [(name, prm_values[name]) for name in prm_values]

    all_combination = []
    varied = []
    for name, values in prm_values:
        all_combination = _outer(all_combination, values)
        if isinstance(values, list) and len(values) > 1:
            varied.append(name)
    names = [name for name, values in prm_values]
    return all_combination, names, varied
