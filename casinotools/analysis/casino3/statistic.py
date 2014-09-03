#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.

# Globals and constants variables.

class Statistic(object):
    def __init__(self, array):
        self._minimum = np.amin(array)
        self._maximum = np.amax(array)
        self._range = np.ptp(array)
        self._mean = np.mean(array)
        self._median = np.median(array)
        self._standardDeviation = np.std(array)
        self._variance = np.var(array)

    def getMean(self):
        return self._mean

    def getStandardDeviation(self):
        return self._standardDeviation

    def getMaximum(self):
        return self._maximum

    def getMedian(self):
        return self._median
