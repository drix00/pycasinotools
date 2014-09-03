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
import casinotools.fileformat.casino3.SampleSubtrate as SampleSubtrate
import casinotools.fileformat.casino3.SampleShape.SphereShape as SphereShape
from casinotools.fileformat.casino3.SampleObject import SampleObject
from casinotools.fileformat.casino3.SampleShape.ShapeType import \
    (SHAPE_PLANE, SHAPE_BOX, SHAPE_SPHERE, SHAPE_CONE, SHAPE_CYLINDRE,
     SHAPE_ROUNDREC, SHAPE_TRUNC_PYRAMID, SHAPE_MESHOBJECT, SHAPE_SUBSTRATE)

# Globals and constants variables.

def CreateObjectFromType(type):
    if type == SHAPE_PLANE:
        return PlaneShape(type)
    elif type == SHAPE_BOX:
        return BoxShape(type)
    elif type == SHAPE_SPHERE:
        return SphereShape.SphereShape(type)
    elif type == SHAPE_CONE:
        return ConeShape(type)
    elif type == SHAPE_CYLINDRE:
        return CylindreShape(type)
    elif type == SHAPE_ROUNDREC:
        return RoundedRectangleShape(type)
    elif type == SHAPE_TRUNC_PYRAMID:
        return TruncatedPyramidShape(type)
    elif type == SHAPE_MESHOBJECT:
        return MeshObject(type)
    elif type == SHAPE_SUBSTRATE:
        return SampleSubtrate.SampleSubtrate(type)
    else:
        return SampleObject(type)

class PlaneShape(SampleObject):
    def __init__(self, type):
        super(PlaneShape, self).__init__(type)

    def read(self, file):
        super(PlaneShape, self).read(file)

class BoxShape(SampleObject):
    def __init__(self, type):
        super(BoxShape, self).__init__(type)
        self._type = SHAPE_BOX
        self._scale = [10.0, 10.0, 10.0]
        self._color = [1.0, 1.0, 1.0]

class ConeShape(SampleObject):
    def __init__(self, type):
        super(ConeShape, self).__init__(type)

    def read(self, file):
        logging.error("ConeShape read method not implemented.")

class CylindreShape(SampleObject):
    def __init__(self, type):
        super(CylindreShape, self).__init__(type)

        self._radius = 5.0
        self._divTheta = 12.0

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        super(CylindreShape, self).read(file)

        self._radius = self.readDouble(file)
        self._divTheta = self.readInt(file)

class RoundedRectangleShape(SampleObject):
    def __init__(self, type):
        super(RoundedRectangleShape, self).__init__(type)

    def read(self, file):
        logging.error("RoundedRectangleShape read method not implemented.")

class TruncatedPyramidShape(SampleObject):
    def __init__(self, type):
        super(TruncatedPyramidShape, self).__init__(type)

        self._type = SHAPE_TRUNC_PYRAMID
        self._scale = [1.0, 1.0, 1.0]
        self._color = [0.4, 0.275, 0.5]

        self._angleA_deg = 70.0
        self._angleB_deg = 90.0
        self._angleC_deg = 70.0
        self._angleD_deg = 90.0

        self._x = 10
        self._y = 10
        self._z = 10

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        super(TruncatedPyramidShape, self).read(file)

        if self._version < 30105004:
            for dummyIndex in range(8):
                dummyCorner = self.readDoubleList(file, 3)

        self._x = self.readDouble(file)
        self._y = self.readDouble(file)
        self._z = self.readDouble(file)
        self._angleA_deg = self.readDouble(file)
        self._angleB_deg = self.readDouble(file)
        self._angleC_deg = self.readDouble(file)
        self._angleD_deg = self.readDouble(file)

class MeshObject(SampleObject):
    def __init__(self, type):
        super(MeshObject, self).__init__(type)

    def read(self, file):
        logging.error("MeshObject read method not implemented.")
