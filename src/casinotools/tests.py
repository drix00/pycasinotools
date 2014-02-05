#!/usr/bin/env python
"""
.. py:currentmodule:: tests
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Regression testing for the project.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import DrixUtilities.Testings as Testings

# Project modules

# Globals and constants variables.

if __name__ == "__main__": #pragma: no cover
    Testings.runTestSuiteWithCoverage(packageName=__file__)
