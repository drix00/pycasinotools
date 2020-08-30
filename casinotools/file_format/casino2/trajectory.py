#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.trajectory
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools
from casinotools.file_format.casino2.scattering_event import ScatteringEvent

# Globals and constants variables.


class Trajectory(FileReaderWriterTools):
    def __init__(self, is_skip_reading_data=False):
        self._is_skip_reading_data = is_skip_reading_data

        self.FRetro = 0
        self.FTrans = 0
        self.FDetec = 0
        self.NbColl = 0
        self.Zmax = 0.0
        self.LPM = 0.0
        self.DedsM = 0.0
        self.PhiM = 0.0
        self.ThetaM = 0.0
        self.MoyenX = 0.0
        self.MoyenY = 0.0
        self.MoyenZ = 0.0
        self.Display = 0

        self.NbElec = 0

        self._scatteringEvents = []

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self.FRetro = self.read_int(file)
        self.FTrans = self.read_int(file)
        self.FDetec = self.read_int(file)
        self.NbColl = self.read_long(file)
        self.Zmax = self.read_double(file)
        self.LPM = self.read_double(file)
        self.DedsM = self.read_double(file)
        self.PhiM = self.read_double(file)
        self.ThetaM = self.read_double(file)
        self.MoyenX = self.read_double(file)
        self.MoyenY = self.read_double(file)
        self.MoyenZ = self.read_double(file)
        self.Display = self.read_int(file)

        self.NbElec = self.read_long(file)

        self._scatteringEvents = []
        if not self._is_skip_reading_data:
            for dummy in range(self.NbElec):
                event = ScatteringEvent()
                event.read(file)
                self._scatteringEvents.append(event)
        else:
            offset = ScatteringEvent().get_skip_offset()
            offset *= self.NbElec
            file.seek(offset, os.SEEK_CUR)

    def is_backscattered(self):
        return bool(self.FRetro)

    def is_transmitted(self):
        return bool(self.FTrans)

    def is_absorbed(self):
        return not self.is_backscattered() and not self.is_transmitted()

    def get_scattering_events(self):
        return self._scatteringEvents
