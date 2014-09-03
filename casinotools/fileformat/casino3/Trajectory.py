#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
#import logging
import os
import struct

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino3.TrajectoryCollision as TrajectoryCollision

# Globals and constants variables.
TRAJ_TYPE_NONE = 0x00;
TRAJ_TYPE_BACKSCAT = 0x01;
TRAJ_TYPE_TRANSMIT = 0x02;
TRAJ_TYPE_DETEC = 0x04;
TRAJ_TYPE_SECONDARY = 0x08;
TRAJ_DISPLAY = 0x100;

class Trajectory(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._file = None
        self._startPosition = 0
        self._startPositionCollisions = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

        self._version = None
        self._trajectoryCollisions = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        #logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._startPosition = file.tell()
        #self._readHeaderFast(file)
        self._readHeader(file)

        self._startPositionCollisions = file.tell()
        sizeScatteringEvent = TrajectoryCollision.getSizeScatteringEvent()
        skipOffset = sizeScatteringEvent * self._numberScatteringEvents
        file.seek(skipOffset, os.SEEK_CUR)

        self._endPosition = file.tell()
        #logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

    def _readHeader(self, file):
        self._file.seek(self._startPosition)
        self._version = self.readInt(file)
        # TRAJ_TYPE_BACKSCAT
        self._type = self.readInt(file)
        # TRAJ_TYPE_TRANSMIT
        self._type |= self.readInt(file)
        # TRAJ_TYPE_DETEC
        self._type |= self.readInt(file)
        # TRAJ_TYPE_SECONDARY
        self._type |= self.readInt(file)
        # TRAJ_DISPLAY (0 or 1 for this version)
        if self.readInt(file):
            self._type |= TRAJ_DISPLAY

        self._order = self.readInt(file)
        self._dirX = self.readDouble(file)
        self._dirY = self.readDouble(file)
        self._dirZ = self.readDouble(file)

        self._readNumberScatteringEvents(file)

    def _readHeaderFast(self, file):
        size = struct.calcsize("=7i3d4x16s")
        file.seek(size, os.SEEK_CUR)

        self._readNumberScatteringEventsFast(file)

    def _readNumberScatteringEvents(self, file):
        #logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_readNumberScatteringEvents", file.tell())
        tagID = b"NbElec"
        self.findTag(file, tagID)
        #logging.debug("File position after findtag of %s.%s: %i", self.__class__.__name__, "_readNumberScatteringEvents", file.tell())
        self._numberScatteringEvents = self.readInt(file)
        #logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "_readNumberScatteringEvents", file.tell())

    def _readNumberScatteringEventsFast(self, file):
        #tagID = "NbElec"
        #self.findTag(file, tagID)
        self._numberScatteringEvents = self.readInt(file)

    def _readScatteringEvents(self):
        self._readScatteringEventsOptimized()

    def _readScatteringEventsOriginal(self):
        closeFile = False
        if self._file.closed:
            self._file = open(self._filePathname, 'rb')
            closeFile = True

        self._file.seek(self._startPositionCollisions)
        self._trajectoryCollisions = []
        for dummy in range(self._numberScatteringEvents):
            trajectoryCollision = TrajectoryCollision.TrajectoryCollision()
            trajectoryCollision.read(self._file)
            self._trajectoryCollisions.append(trajectoryCollision)

        if closeFile:
            self._file.close()

    def _readScatteringEventsOptimized(self):
        closeFile = False
        if self._file.closed:
            self._file = open(self._filePathname, 'rb')
            closeFile = True

        self._file.seek(self._startPositionCollisions)

        format = "5d2i"*self._numberScatteringEvents
        items = self.readMultipleValues(self._file, format)

        self._trajectoryCollisions = [TrajectoryCollision.TrajectoryCollision(items[index * 7:(index * 7) + 7]) for index in range(self._numberScatteringEvents)]

        if closeFile:
            self._file.close()

    def getNumberScatteringEvents(self):
        return self._numberScatteringEvents

    def getScatteringEvent(self, index):
        if self._trajectoryCollisions is None:
            self._readScatteringEvents()

        return self._trajectoryCollisions[index]

    def getScatteringEvents(self):
        if self._trajectoryCollisions is None:
            self._readScatteringEvents()

        return self._trajectoryCollisions

    def getScatteringEventsByType(self, type):
        if self._trajectoryCollisions is None:
            self._readScatteringEvents()

        collisions = []
        for collision in self._trajectoryCollisions:
            if collision.getCollisionType() == type:
                collisions.append(collision)

        return collisions

    def deleteAllTrajectoryCollisions(self):
        del self._trajectoryCollisions
        self._trajectoryCollisions = None

    def getVersion(self):
        if self._version is None:
            self._readHeader(self._file)

        return self._version

    def getType(self):
        if self._type is None:
            self._readHeader(self._file)

        return self._type

    def getTypeName(self):
        name = ""
        if self.isTypeNone():
            name += "None "
        elif self.isTypeBackscattered():
            name += "BSE "
        elif self.isTypeTransmitted():
            name += "TE "
        elif self.isTypeDetected():
            name += "Detected "
        elif self.isTypeSecondary():
            name += "SE "
        elif self.isTypeDisplayed():
            name += "Displayed "

        return name

    def isTypeNone(self):
        return self._isType(TRAJ_TYPE_NONE)

    def isTypeBackscattered(self):
        return self._isType(TRAJ_TYPE_BACKSCAT)

    def isTypeTransmitted(self):
        return self._isType(TRAJ_TYPE_TRANSMIT)

    def isTypeDetected(self):
        return self._isType(TRAJ_TYPE_DETEC)

    def isTypeSecondary(self):
        return self._isType(TRAJ_TYPE_SECONDARY)

    def isTypeDisplayed(self):
        return self._isType(TRAJ_DISPLAY)

    def _isType(self, trajectoryType):
        return self.getType() & trajectoryType
