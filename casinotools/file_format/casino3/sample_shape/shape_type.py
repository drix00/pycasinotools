#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_shape.shape_type
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
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
SHAPE_SUBSTRATE = -1
SHAPE_UNDEFINED = 0
SHAPE_PLANE = 1
SHAPE_BOX = 2
SHAPE_SPHERE = 3
SHAPE_CONE = 4
SHAPE_CYLINDER = 5
SHAPE_ROUND_RECTANGLE = 6
SHAPE_TRUNC_PYRAMID = 7
SHAPE_MESH_OBJECT = 999


def get_string(shape):
    if shape == SHAPE_SUBSTRATE:
        return "substrate"
    elif shape == SHAPE_UNDEFINED:
        return "undefined"
    elif shape == SHAPE_PLANE:
        return "plane"
    elif shape == SHAPE_BOX:
        return "box"
    elif shape == SHAPE_SPHERE:
        return "sphere"
    elif shape == SHAPE_CONE:
        return "cone"
    elif shape == SHAPE_CYLINDER:
        return "cylinder"
    elif shape == SHAPE_ROUND_RECTANGLE:
        return "rounded rectangle"
    elif shape == SHAPE_TRUNC_PYRAMID:
        return "truncated pyramid"
    elif shape == SHAPE_MESH_OBJECT:
        return "mesh object"
