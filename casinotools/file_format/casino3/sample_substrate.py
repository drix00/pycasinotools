#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_substrate
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
from casinotools.file_format.casino3.sample_object import SampleObject
from casinotools.file_format.file_reader_writer_tools import read_int

# Globals and constants variables.


class Edge(object):
    def read(self, file):
        pass
        # raise NotImplementedError


class SampleSubstrate(SampleObject):
    def __init__(self, shape_type=None):
        super(SampleSubstrate, self).__init__(shape_type)

        self._file = None
        self._startPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

        self._numberEdges = 0
        self._edges = []

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        super(SampleSubstrate, self).read(file)

        self._numberEdges = read_int(file)

        self._edges = []
        for dummyIndex in range(self._numberEdges):
            edge = Edge()
            edge.read(file)
            self._edges.append(edge)

    def export(self, export_file):
        # todo: implement the export method.
        logging.error("implement the export method.")
