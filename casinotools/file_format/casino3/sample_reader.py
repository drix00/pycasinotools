#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.sample_reader
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
import struct
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.tags import find_tag

# Globals and constants variables.


class SampleReader(object):
    def __init__(self):
        self._sample = None
        self._version = 0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = b"*CASINOSAMPLE%%"

        if find_tag(file, tag_id):
            value_format = "i"
            size = struct.calcsize(value_format)
            buffer = file.read(size)
            items = struct.unpack_from(value_format, buffer)
            self._version = int(items[0])

        return None

    def get_sample(self):
        return self._sample
