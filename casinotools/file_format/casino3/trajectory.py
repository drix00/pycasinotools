#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.trajectory
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
import os
import struct

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools
from casinotools.file_format.casino3.trajectory_collision import TrajectoryCollision, get_size_scattering_event

# Globals and constants variables.
TRAJECTORY_TYPE_NONE = 0x00
TRAJECTORY_TYPE_BACKSCATTERED = 0x01
TRAJECTORY_TYPE_TRANSMITTED = 0x02
TRAJECTORY_TYPE_DETECTED = 0x04
TRAJECTORY_TYPE_SECONDARY = 0x08
TRAJECTORY_DISPLAY = 0x100


class Trajectory(FileReaderWriterTools):
    def __init__(self):
        self._file = None
        self._start_position = 0
        self._start_position_collisions = 0
        self._end_position = 0
        self._file_pathname = ""
        self._file_descriptor = 0

        self._version = None
        self._trajectory_collisions = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._start_position = file.tell()
        self._file_pathname = file.name
        self._file_descriptor = file.fileno()
        # logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read",
        #               self._start_position)

        self._start_position = file.tell()
        # self._read_header_fast(file)
        self._read_header(file)

        self._start_position_collisions = file.tell()
        size_scattering_event = get_size_scattering_event()
        skip_offset = size_scattering_event * self._number_scattering_events
        file.seek(skip_offset, os.SEEK_CUR)

        self._end_position = file.tell()
        # logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._end_position)

    def _read_header(self, file):
        self._file.seek(self._start_position)
        self._version = self.read_int(file)
        # TRAJECTORY_TYPE_BACKSCATTERED
        self._type = self.read_int(file)
        # TRAJECTORY_TYPE_TRANSMITTED
        self._type |= self.read_int(file)
        # TRAJECTORY_TYPE_DETECTED
        self._type |= self.read_int(file)
        # TRAJECTORY_TYPE_SECONDARY
        self._type |= self.read_int(file)
        # TRAJECTORY_DISPLAY (0 or 1 for this version)
        if self.read_int(file):
            self._type |= TRAJECTORY_DISPLAY

        self._order = self.read_int(file)
        self._dir_x = self.read_double(file)
        self._dir_y = self.read_double(file)
        self._dir_z = self.read_double(file)

        self._read_number_scattering_events(file)

    def _read_header_fast(self, file):
        size = struct.calcsize("=7i3d4x16s")
        file.seek(size, os.SEEK_CUR)

        self._read_number_scattering_events_fast(file)

    def _read_number_scattering_events(self, file):
        # logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__,
        #               "_read_number_scattering_events", file.tell())
        tag_id = b"NbElec"
        self.find_tag(file, tag_id)
        # logging.debug("File position after find_tag of %s.%s: %i", self.__class__.__name__,
        #               "_read_number_scattering_events", file.tell())
        self._number_scattering_events = self.read_int(file)
        # logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__,
        #               "_read_number_scattering_events", file.tell())

    def _read_number_scattering_events_fast(self, file):
        # tag_id = "NbElec"
        # self.find_tag(file, tag_id)
        self._number_scattering_events = self.read_int(file)

    def _read_scattering_events(self):
        self._read_scattering_events_optimized()

    def _read_scattering_events_original(self):
        close_file = False
        if self._file.closed:
            self._file = open(self._file_pathname, 'rb')
            close_file = True

        self._file.seek(self._start_position_collisions)
        self._trajectory_collisions = []
        for dummy in range(self._number_scattering_events):
            trajectory_collision = TrajectoryCollision()
            trajectory_collision.read(self._file)
            self._trajectory_collisions.append(trajectory_collision)

        if close_file:
            self._file.close()

    def _read_scattering_events_optimized(self):
        close_file = False
        if self._file.closed:
            self._file = open(self._file_pathname, 'rb')
            close_file = True

        self._file.seek(self._start_position_collisions)

        values_format = "5d2i"*self._number_scattering_events
        items = self.read_multiple_values(self._file, values_format)

        self._trajectory_collisions = [TrajectoryCollision(items[index * 7:(index * 7) + 7])
                                       for index in range(self._number_scattering_events)]

        if close_file:
            self._file.close()

    def get_number_scattering_events(self):
        return self._number_scattering_events

    def get_scattering_event(self, index):
        if self._trajectory_collisions is None:
            self._read_scattering_events()

        return self._trajectory_collisions[index]

    def get_scattering_events(self):
        if self._trajectory_collisions is None:
            self._read_scattering_events()

        return self._trajectory_collisions

    def get_scattering_events_by_type(self, collision_type):
        if self._trajectory_collisions is None:
            self._read_scattering_events()

        collisions = []
        for collision in self._trajectory_collisions:
            if collision.get_collision_type() == collision_type:
                collisions.append(collision)

        return collisions

    def delete_all_trajectory_collisions(self):
        del self._trajectory_collisions
        self._trajectory_collisions = None

    def get_version(self):
        if self._version is None:
            self._read_header(self._file)

        return self._version

    def get_type(self):
        if self._type is None:
            self._read_header(self._file)

        return self._type

    def get_type_name(self):
        name = ""
        if self.is_type_none():
            name += "None "
        elif self.is_type_backscattered():
            name += "BSE "
        elif self.is_type_transmitted():
            name += "TE "
        elif self.is_type_detected():
            name += "Detected "
        elif self.is_type_secondary():
            name += "SE "
        elif self.is_type_displayed():
            name += "Displayed "

        return name

    def is_type_none(self):
        return self._is_type(TRAJECTORY_TYPE_NONE)

    def is_type_backscattered(self):
        return self._is_type(TRAJECTORY_TYPE_BACKSCATTERED)

    def is_type_transmitted(self):
        return self._is_type(TRAJECTORY_TYPE_TRANSMITTED)

    def is_type_detected(self):
        return self._is_type(TRAJECTORY_TYPE_DETECTED)

    def is_type_secondary(self):
        return self._is_type(TRAJECTORY_TYPE_SECONDARY)

    def is_type_displayed(self):
        return self._is_type(TRAJECTORY_DISPLAY)

    def _is_type(self, trajectory_type):
        return self.get_type() & trajectory_type
