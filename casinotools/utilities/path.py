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
    if not os.path.exists(path):
        os.makedirs(path)

    if len(path) > 0 and path[-1] != os.sep:
        path += os.sep

    return path

if __name__ == '__main__': #pragma: no cover
    import nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
