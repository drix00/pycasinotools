#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_object_factory
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
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.casino3.sample_substrate import SampleSubstrate
from casinotools.file_format.casino3.sample_shape.sphere_shape import SphereShape
from casinotools.file_format.casino3.sample_object import SampleObject
from casinotools.file_format.casino3.sample_shape.shape_type import \
    (SHAPE_PLANE, SHAPE_BOX, SHAPE_SPHERE, SHAPE_CONE, SHAPE_CYLINDER,
     SHAPE_ROUND_RECTANGLE, SHAPE_TRUNC_PYRAMID, SHAPE_MESH_OBJECT, SHAPE_SUBSTRATE)
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, read_double_list

# Globals and constants variables.


def create_object_from_type(shape_type):
    if shape_type == SHAPE_PLANE:
        return PlaneShape(shape_type)
    elif shape_type == SHAPE_BOX:
        return BoxShape(shape_type)
    elif shape_type == SHAPE_SPHERE:
        return SphereShape(shape_type)
    elif shape_type == SHAPE_CONE:
        return ConeShape(shape_type)
    elif shape_type == SHAPE_CYLINDER:
        return CylindreShape(shape_type)
    elif shape_type == SHAPE_ROUND_RECTANGLE:
        return RoundedRectangleShape(shape_type)
    elif shape_type == SHAPE_TRUNC_PYRAMID:
        return TruncatedPyramidShape(shape_type)
    elif shape_type == SHAPE_MESH_OBJECT:
        return MeshObject(shape_type)
    elif shape_type == SHAPE_SUBSTRATE:
        return SampleSubstrate(shape_type)
    else:
        return SampleObject(shape_type)


class PlaneShape(SampleObject):
    def __init__(self, shape_type):
        super(PlaneShape, self).__init__(shape_type)

    def read(self, file):
        super(PlaneShape, self).read(file)


class BoxShape(SampleObject):
    def __init__(self, shape_type):
        super(BoxShape, self).__init__(shape_type)
        self._type = SHAPE_BOX
        self._scale = [10.0, 10.0, 10.0]
        self._color = [1.0, 1.0, 1.0]


class ConeShape(SampleObject):
    def __init__(self, shape_type):
        super(ConeShape, self).__init__(shape_type)

    def read(self, file):
        logging.error("ConeShape read method not implemented.")


class CylindreShape(SampleObject):
    def __init__(self, shape_type):
        super(CylindreShape, self).__init__(shape_type)

        self._file = None
        self._start_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._radius = 5.0
        self._div_theta = 12.0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        super(CylindreShape, self).read(file)

        self._radius = read_double(file)
        self._div_theta = read_int(file)


class RoundedRectangleShape(SampleObject):
    def __init__(self, shape_type):
        super(RoundedRectangleShape, self).__init__(shape_type)

    def read(self, file):
        logging.error("RoundedRectangleShape read method not implemented.")


class TruncatedPyramidShape(SampleObject):
    def __init__(self, shape_type):
        super(TruncatedPyramidShape, self).__init__(shape_type)

        self._file = None
        self._start_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._type = SHAPE_TRUNC_PYRAMID
        self._scale = [1.0, 1.0, 1.0]
        self._color = [0.4, 0.275, 0.5]

        self._x = 10
        self._y = 10
        self._z = 10

        self._angle_a_deg = 70.0
        self._angle_b_deg = 90.0
        self._angle_c_deg = 70.0
        self._angle_d_deg = 90.0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._start_position)

        super(TruncatedPyramidShape, self).read(file)

        if self.version < 30105004:
            for dummyIndex in range(8):
                _dummy_corner = read_double_list(file, 3)

        self._x = read_double(file)
        self._y = read_double(file)
        self._z = read_double(file)
        self._angle_a_deg = read_double(file)
        self._angle_b_deg = read_double(file)
        self._angle_c_deg = read_double(file)
        self._angle_d_deg = read_double(file)


class MeshObject(SampleObject):
    def __init__(self, shape_type):
        super(MeshObject, self).__init__(shape_type)

    def read(self, file):
        logging.error("MeshObject read method not implemented.")
