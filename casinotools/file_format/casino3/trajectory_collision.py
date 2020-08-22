#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import struct
import math

# Third party modules.

# Local modules.
import casinotools.file_format.file_reader_writer_tools as FileReaderWriterTools

# Globals and constants variables.
COLLISION_TYPE_ATOM = 0
COLLISION_TYPE_REGION = 1
COLLISION_TYPE_NODE = 2
COLLISION_TYPE_RECALC = 3

COLLISION_TYPE_LABELS = {COLLISION_TYPE_ATOM: "Atom",
                         COLLISION_TYPE_REGION: "Region",
                         COLLISION_TYPE_NODE: "Node",
                         COLLISION_TYPE_RECALC:"Recalc"}

def getSizeScatteringEvent():
    size = struct.calcsize("5d2i")
    return size

class TrajectoryCollision(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, items=None):
        if items is not None:
            self._positionX = items[0]
            self._positionY = items[1]
            self._positionZ = items[2]
            self._energy = items[3]
            self._segmentLength = items[4]
            self._collisionType = items[5]
            self._regionID = items[6]

    def read(self, file):
        self._readOptimized(file)

    def _readOriginal(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self._positionX = self.read_double(file)
        self._positionY = self.read_double(file)
        self._positionZ = self.read_double(file)
        self._energy = self.read_double(file)
        self._segmentLength = self.read_double(file)
        self._collisionType = self.read_int(file)

        self._regionID = self.read_int(file)

    def _readOptimized(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        format = "5d2i"
        items = self.read_multiple_values(file, format)

        self.setValues(items)

    def setValues(self, items):
        self._positionX = items[0]
        self._positionY = items[1]
        self._positionZ = items[2]
        self._energy = items[3]
        self._segmentLength = items[4]
        self._collisionType = items[5]
        self._regionID = items[6]

    def getCollisionType(self):
        return self._collisionType

    def getCollisionTypeName(self):
        return COLLISION_TYPE_LABELS[self._collisionType]

    def getX_nm(self):
        return self._positionX

    def getY_nm(self):
        return self._positionY

    def getZ_nm(self):
        return self._positionZ

    def getPosition_nm(self):
        position_nm = (self._positionX, self._positionY, self._positionZ)

        return position_nm

    def getRadiusXY_nm(self):
        return math.sqrt(self._positionX ** 2 + self._positionY ** 2)

    def getEnergy_keV(self):
        return self._energy

    def getRegionID(self):
        return self._regionID
