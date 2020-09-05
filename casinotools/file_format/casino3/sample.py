#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, read_float_list, \
    write_double
from casinotools.file_format.tags import find_tag
from casinotools.file_format.casino3.sample_object_factory import create_object_from_type, SHAPE_SUBSTRATE, SHAPE_SPHERE
from casinotools.file_format.casino3.sample_object_factory import SHAPE_PLANE
from casinotools.file_format.casino3.sample_tree import SampleTree
from casinotools.file_format.casino3.region import Region
from casinotools.file_format.casino3.version import SIM_OPTIONS_VERSION_3_1_8_2

# Globals and constants variables.
OFFSET_ROTATION_Y = "offset_rotation_y"
OFFSET_ROTATION_Z = "offset_rotation_z"


class ShapeError(Exception):
    pass


class Sample:
    def __init__(self):
        self._file = None
        self._start_position = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._version = 0

        self._sample_objects = []
        self._regions = []

        self._offsets = {}

        self._rotation_angle_y_deg = 0.0
        self._rotation_angle_z_deg = 0.0

    def read(self, file):
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()

        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = b"*CASINOSAMPLE%%"
        if find_tag(file, tag_id):
            self._version = read_int(file)

            if self._version >= 3010301:
                return self._read_3131(file)
            else:
                raise ValueError("version_not_supported")

    def _read_3131(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_read_3131", file.tell())

        tag_id = b"*SUBSTRATE%%%%%"
        if find_tag(file, tag_id):
            self._useSubstrate = read_int(file)

            self._substrate = create_object_from_type(SHAPE_SUBSTRATE)
            self._substrate.read(file)

        tag_id = b"*SAMPLEOBJECTS%"
        if find_tag(file, tag_id):
            self._count = read_int(file)

            for dummy in range(self._count):
                shape_type = read_int(file)

                sample_object = create_object_from_type(shape_type)

                sample_object.read(file)

                if self._version >= 30200002:
                    object_id = read_int(file)
                    self.add_sample_object_with_id(sample_object, object_id)
                else:
                    self.add_sample_object(sample_object)

        if self._version < 30107001:
            tag_id = b"*MAC%%%%%%%%%%%"
            if find_tag(file, tag_id):
                # float MAC[100][100][3]
                # file.read((char*)&MAC,sizeof(MAC[0][0][0]*100*100*3));
                number_elements = 100 * 100 * 3
                self._mac = read_float_list(file, number_elements)

        tag_id = b"*SAMPLEDATA%%%%"
        if find_tag(file, tag_id):
            self._maxSampleTreeLevel = read_int(file)

        if self._version >= SIM_OPTIONS_VERSION_3_1_8_2:
            self._offsets[OFFSET_ROTATION_Y] = file.tell()
            self._rotation_angle_y_deg = read_double(file)
            self._offsets[OFFSET_ROTATION_Z] = file.tell()
            self._rotation_angle_z_deg = read_double(file)

        self._presence = read_int(file)
        if self._presence:
            self._sampleTree = SampleTree()
            self._sampleTree.read(file)

        tag_id = b"*REGIONDATA%%%%"
        if find_tag(file, tag_id):
            self._numberRegions = read_int(file)

        for dummy in range(self._numberRegions):
            region_info = Region()
            region_info.read(file)

            self.add_region(region_info)

        # TODO calculate regions for the sample's triangles.

    def add_sample_object(self, sample_object):
        self._sample_objects.append(sample_object)

    def add_sample_object_with_id(self, sample_object, object_id):
        self._sample_objects.append(sample_object)

    def add_region(self, region):
        self._regions.append(region)

    def get_regions(self):
        return self._regions

    def get_shapes(self):
        return self._sample_objects

    def get_first_sphere_shape(self):
        for shape in self._sample_objects:
            shape_type = shape.get_type()
            if shape_type == SHAPE_SPHERE:
                return shape

        raise ShapeError("Shape not found.")

    def get_plane_shapes(self):
        shapes = []
        for shape in self._sample_objects:
            shape_type = shape.get_type()
            if shape_type == SHAPE_PLANE:
                shapes.append(shape)

        return shapes

    def get_version(self):
        return self._version

    def get_rotation_y_deg(self):
        return self._rotation_angle_y_deg

    def set_rotation_y_deg(self, rotation_angle_deg):
        self._rotation_angle_y_deg = rotation_angle_deg

    def modify_rotation_y_deg(self, rotation_angle_deg):
        self._file.seek(self._offsets[OFFSET_ROTATION_Y])
        write_double(self._file, rotation_angle_deg)
        self._rotation_angle_y_deg = rotation_angle_deg

    def get_rotation_z_deg(self):
        return self._rotation_angle_z_deg

    def set_rotation_z_deg(self, rotation_angle_deg):
        self._rotation_angle_z_deg = rotation_angle_deg

    def modify_rotation_z_deg(self, rotation_angle_deg):
        self._file.seek(self._offsets[OFFSET_ROTATION_Z])
        write_double(self._file, rotation_angle_deg)
        self._rotation_angle_z_deg = rotation_angle_deg

    def write(self, file):
        pass

    def export(self, export_file):
        # todo: implement the export method.
        self._export_header(export_file)
        self._export_version(export_file)
        self._export_substrate(export_file)
        self._export_sample_objects(export_file)
        self._export_sample_data(export_file)
        self._export_region_data(export_file)

    def _export_header(self, export_file):
        line = "-"*80
        write_line(export_file, line)

        line = "{}".format("Sample")
        write_line(export_file, line)

        line = "-"*40
        write_line(export_file, line)

    def _export_version(self, export_file):
        version = self.get_version()
        version_string = _extract_version_string(version)
        line = "File version: %s (%i)" % (version_string, version)
        write_line(export_file, line)

    def _export_substrate(self, export_file):
        text = self._extract_boolean_string(self._useSubstrate)
        line = "Use substrate: {}".format(text)
        write_line(export_file, line)

        self._substrate.export(export_file)

    def _export_sample_objects(self, export_file):
        line = "number of sample objects: {:d}".format(self._count)
        write_line(export_file, line)

        sample_object_id = 0
        for sampleObject in self._sample_objects:
            sample_object_id += 1
            line = "Sample object: {:d}".format(sample_object_id)
            write_line(export_file, line)

            sampleObject.export(export_file)

    def _export_sample_data(self, export_file):
        line = "Maximum sample tree level: {:d}".format(self._maxSampleTreeLevel)
        write_line(export_file, line)

        line = "Sample rotation angle Y (deg): {:g}" % (self._rotation_angle_y_deg)
        write_line(export_file, line)

        line = "Sample rotation angle z (deg): {:g}" % (self._rotation_angle_z_deg)
        write_line(export_file, line)

        text = self._extract_boolean_string(self._presence)
        line = "Presence: {}".format(text)
        write_line(export_file, line)

        if self._presence:
            self._sampleTree.export(export_file)

    def _export_region_data(self, export_file):
        line = "number of regions: {:d}".format(self._numberRegions)
        write_line(export_file, line)

        sample_region_id = 0
        for region in self._regions:
            sample_region_id += 1
            line = "Sample region: {:d}".format(sample_region_id)
            write_line(export_file, line)

            region.export(export_file)
