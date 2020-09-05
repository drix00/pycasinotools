#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_xray
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
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, read_float
from casinotools.file_format.tags import find_tag

# Globals and constants variables.

# Filename to store the defaults settings
OPTIONS_XRAY_DEF_FILENAME = "XRay_Settings_Defaults.dat"


# // XRays
# /// Take off angle of the X-ray detector
#    double toa
# /// Polar angle of the X-Ray detector
#    float phi_rx
class OptionsXray:
    def __init__(self):
        self._version = 0
        self.toa = 0.0
        self.phi_rx = 0.0

        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#    Tags::AddTag(file,"*XRAY_OPT_BEG", 15)
#    writeVersion(file)
#
#    safe_write<double>(file, toa)
#    safe_write<float>(file, phi_rx)
#
#    Tags::AddTag(file, "*XRAY_OPT_END", 15)

    def read(self, file):
        tag_id = b"*XRAY_OPT_BEG"
        find_tag(file, tag_id)

        self._version = read_int(file)

        self.toa = read_double(file)
        self.phi_rx = read_float(file)

        tag_id = b"*XRAY_OPT_END"
        find_tag(file, tag_id)

    def reset(self):
        self.toa = 40.0
        self.phi_rx = 0.0
