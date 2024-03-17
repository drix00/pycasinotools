#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options.options_runtime
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read and write runtime options file.
"""

###############################################################################
# Copyright 2024 Hendrix Demers
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
# Filename to store the defaults settings
OPTIONS_RUNTIME_DEF_FILENAME = "Runtime_Settings_Defaults.dat"

# thread_priority
OPT_THREAD_PRIORITY_ABOVE_NORMAL = 0
OPT_THREAD_PRIORITY_NORMAL = 1
OPT_THREAD_PRIORITY_BELOW_NORMAL = 2
OPT_THREAD_PRIORITY_IDLE = 3
OPT_THREAD_PRIORITY_DEFAULT = OPT_THREAD_PRIORITY_BELOW_NORMAL

# const for the Memory_Keep option :
# MEMORY_KEEP_NONE : keep no trajectory in memory
# MEMORY_KEEP_ALL : keep all trajectories
# MEMORY_KEEP_DISPLAY : keep the number of displayed trajectories in memory
MEMORY_KEEP_NONE = 0x00
MEMORY_KEEP_ALL = 0x01
MEMORY_KEEP_DISPLAY = 0x02
MEMORY_KEEP_DEFAULT = MEMORY_KEEP_DISPLAY

NB_SCAN_POINTS_PER_THREAD_DEFAULT = 5


class OptionsRuntime:
    def __init__(self):
        # Number of calculated electrons to be displayed.
        trajectories_display = 200

        # The number of scan points one thread will calculate :
        # When launching a simulation, a thread will have this number of scan points
        # to calculate. A higher number of scan points per thread is useful when
        # scan points are quick to calculate which would cause the overhead of creating
        # a thread high in relation to it's calculation time. A lower number mean
        # a higher responsiveness when changing the number of calculating thread
        # on the fly.
        number_scan_points_per_thread = NB_SCAN_POINTS_PER_THREAD_DEFAULT

        # Determine if the different trajectories will be kept or deleted.
        # see const declaration for possible values.
        memory_keep = MEMORY_KEEP_DEFAULT

        # Maximum number of threads.
        maximum_concurrent_simulations = 1

        # Determine with which priority the thread will be created.
        # Depending on what is the user system, if the user is working at the same time on
        # the system and the other processes on the system.
        # The lower is the value, the lower is the priority. From 0 (idle) to 3 (above normal).
        thread_priority = OPT_THREAD_PRIORITY_DEFAULT

    def read(self, file_path):
        pass

    def write(self, file_path):
        pass

    def resolve_thread_priority(self):
        pass

