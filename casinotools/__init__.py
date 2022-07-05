#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Main casinotools package initialization module.
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
from pathlib import Path

# Third party modules.

# Local modules.

# Project modules

# Globals and constants variables.

__author__ = """Hendrix Demers"""
__email__ = 'hendrix.demers@mail.mcgill.ca'
__version__ = '0.3'
__project_name__ = "pyCasinoTools"


def get_current_module_path(module_path: str, relative_path: str = "") -> Path:
    """
    Extract the current module path and combine it with the relative path and return it.

    :param str module_path: Pass the `__file__` python keyword for this parameter
    :param str relative_path: The relative path to combine with the module path
    :return: The path obtained when combine the module path and relative path
    :rtype: Path
    """
    base_path = Path(module_path).parent
    file_path = base_path.joinpath(relative_path)
    file_path = file_path.resolve()

    return file_path
