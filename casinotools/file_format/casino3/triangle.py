#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.triangle
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Triangle used by CASINO for the sample geometry.
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
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

# Globals and constants variables.


class Triangle(FileReaderWriterTools):
    def __init__(self):
        self._point0 = None
        self._point1 = None
        self._point2 = None

        self._normal = None

        self._id = None
        self._inside_id = None
        self._outside_id = None

    def read(self, file):
        self._id = self.read_int(file)
        self._point0 = self.read_double_list(file, 3)
        self._point1 = self.read_double_list(file, 3)
        self._point2 = self.read_double_list(file, 3)

        self._normal = self.read_double_list(file, 3)

        # Obsolete.
        self.read_float(file)

        self._inside_id = self.read_int(file)
        self._outside_id = self.read_int(file)

    def export(self, export_file):
        line = "id: {:d}".format(self._id)
        self.write_line(export_file, line)

        line = "Point 0:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'z'], self._point0):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Point 1:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'z'], self._point1):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Point 2:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'z'], self._point2):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "Normal:"
        self.write_line(export_file, line)
        for label, value in zip(["X", 'Y', 'z'], self._normal):
            line = "\t%s: %g" % (label, value)
            self.write_line(export_file, line)

        line = "inside id: {:d}".format(self._inside_id)
        self.write_line(export_file, line)

        line = "outside id: {:d}".format(self._outside_id)
        self.write_line(export_file, line)
