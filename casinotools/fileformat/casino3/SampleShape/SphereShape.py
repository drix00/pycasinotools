#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import logging

# Third party modules.

# Local modules.
from casinotools.fileformat.casino3.SampleObject import SampleObject
from casinotools.fileformat.casino3.SampleShape.ShapeType import SHAPE_SPHERE

# Globals and constants variables.

class SphereShape(SampleObject):
    def __init__(self, type):
        super(SphereShape, self).__init__(type)
        self._type = SHAPE_SPHERE

        self._radius_nm = 5.0
        self._divisionPhi = 4
        self._divisionTheta = 4
        self._color = [0.0, 1.0, 0.0]

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        super(SphereShape, self).read(file)

        self._radius_nm = self.readDouble(file)
        self._divisionPhi = self.readInt(file)
        self._divisionTheta = self.readInt(file)

    def setRadius_nm(self, radius_nm):
        self._radius_nm = radius_nm

    def setDivision(self, division):
        self._divisionPhi = division
        self._divisionTheta = division

    #def export(self, exportdFile):

