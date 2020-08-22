#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
from math import pow

# Third party modules.

# Local modules.

# Globals and constants variables.
MODEL_JOY = 0
MODEL_BERGER = 1
MODEL_PH = 2

class MeanIonizationPotential(object):
    def __init__(self, model=MODEL_JOY):
        if model == MODEL_JOY:
            self._compute = self._computeJoy
        elif model == MODEL_BERGER:
            self._compute = self._computeBerger
        elif model == MODEL_PH:
            self._compute = self._computePH

    def computeJ(self, atomicNumber):
        return self._compute(atomicNumber)

    def _computeJoy(self, atomicNumber):
        z = float(atomicNumber)
        if atomicNumber < 13:
            J = 11.5 * z * 1e-3
        else:
            J = 0.00976 * z + 0.0588 / pow(z, 0.19)

        return J

    def _computeBerger(self, atomicNumber):
        z = float(atomicNumber)
        J = 0.00976 * z + 0.0588 / pow(z, 0.19)
        return J

    def _computePH(self, atomicNumber):
        z = float(atomicNumber)
        if atomicNumber <= 20:
            J = 14.858 + 15.4 * z - 2.9276 * pow(z, 2) + 0.5348 * pow(z, 3) - 0.03563 * pow(z, 4) + 7.7733e-4 * pow(z, 5)
        else:
            J = -2034.18 + 35.576 * z - 0.1142 * pow(z, 2) + 63824.348 / z - 658308.68 / (z * z)

        return (J * 1e-3)

