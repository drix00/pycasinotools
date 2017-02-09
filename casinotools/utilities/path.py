#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.utilities.path
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Utility methods related to path operation used by casinotools.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import logging
import fnmatch
from io import IOBase

# Third party modules.

# Local modules.

# Project modules

# Globals and constants variables.

def get_current_module_path(modulePath, relativePath=""):
    basepath = os.path.dirname(modulePath)
    logging.debug(basepath)

    filepath = os.path.join(basepath, relativePath)
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

def find_all_files(root, patterns='*', ignorePathPatterns='', ignoreNamePatterns='', single_level=False, yield_folders=False):
    """
    Find all files in a root folder.
    From Python Cookbook section 2.16 pages 88--90
    """
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    ignorePathPatterns = ignorePathPatterns.split(';')

    root = os.path.abspath(root)
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)

        addPath = True
        for ignorePathPattern in ignorePathPatterns:
            if fnmatch.fnmatch(path, ignorePathPattern):
                addPath = False

        files.sort()

        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    addName = True
                    for ignorePattern in ignoreNamePatterns:
                        if fnmatch.fnmatch(name, ignorePattern):
                            addName = False

                    if addPath and addName:
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

if __name__ == '__main__': #pragma: no cover
    import nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
