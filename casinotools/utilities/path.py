#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.utilities.path
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Utility methods related to path operation used by casinotools.
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
import os.path
import logging
import fnmatch

# Third party modules.

# Local modules.

# Project modules

# Globals and constants variables.


def get_current_module_path(module_path, relative_path=""):
    base_path = os.path.dirname(module_path)
    logging.debug(base_path)

    filepath = os.path.join(base_path, relative_path)
    logging.debug(filepath)
    filepath = os.path.normpath(filepath)

    return filepath


def create_path(path):
    """
    Create a path from the input string if does not exists.

    Does not try to distinct between file and directory in the input string.
    path = "dir1/filename.ext" => "dir1/filename.ext/"
    where the new directory "filename.ext" is created.

    @param[in] path input string.

    @return the path with the path separator at the end.

    """
    path = os.path.normpath(path)
    if not os.path.isdir(path):
        os.makedirs(path)

    if len(path) > 0 and path[-1] != os.sep:
        path += os.sep

    return path


def find_all_files(root, patterns='*', ignore_path_patterns='', ignore_name_patterns='', single_level=False,
                   yield_folders=False):
    """
    Find all files in a root folder.
    From Python Cookbook section 2.16 pages 88--90
    """
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    ignore_path_patterns = ignore_path_patterns.split(';')

    root = os.path.abspath(root)
    for path, sub_dirs, files in os.walk(root):
        if yield_folders:
            files.extend(sub_dirs)

        add_path = True
        for ignorePathPattern in ignore_path_patterns:
            if fnmatch.fnmatch(path, ignorePathPattern):
                add_path = False

        files.sort()

        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    add_name = True
                    for ignorePattern in ignore_name_patterns:
                        if fnmatch.fnmatch(name, ignorePattern):
                            add_name = False

                    if add_path and add_name:
                        yield os.path.join(path, name)
                        break

        if single_level:
            logging.debug("single_level")
            break


def _is_git_lfs_file(input_file):
    try:
        lines = input_file.readlines()
    except UnicodeDecodeError:
        return False

    if lines[0].startswith("version https://git-lfs.github.com/spec"):
        return True
    else:
        return False


def is_git_lfs_file(file_path):
    if isinstance(file_path, str):
        with open(file_path, 'r') as input_file:
            return _is_git_lfs_file(input_file)

    return _is_git_lfs_file(file_path)


def is_bad_file(file_path):
    if isinstance(file_path, str):
        if os.path.isfile(file_path) and not is_git_lfs_file(file_path):
            return False
        else:
            return True
    elif not is_git_lfs_file(file_path):
        return False
    else:
        return True
