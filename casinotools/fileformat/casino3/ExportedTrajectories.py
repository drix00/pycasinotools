#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.
X_nm = "X (nm)"
Y_nm = "Y (nm)"
Z_nm = "Z (nm)"

KEYWORD_TRAJECTORY = '"Trajectory"'
KEYWORD_NUMBER_COLLISIONS = '"NbCollisions"'
KEYWORD_SCAN_POINT_X = '"X"'
KEYWORD_SCAN_POINT_Y = '"Y"'

class ExportedTrajectories(object):
    def __init__(self, filepath):
        self._filepath = filepath

        self._trajectories = None

    def getPositionsAtZ_nm(self, z_nm):
        if self._trajectories is None:
            self._readDataFile()

        positions = []
        for trajectory in self._trajectories:
            for collision in trajectory:
                if collision[Z_nm] == z_nm:
                    position = (collision[X_nm], collision[Y_nm], collision[Z_nm])
                    positions.append(position)

        return positions

    def getScanPointPosition_nm(self):
        if self._trajectories is None:
            self._readDataFile()

        return self._scanPointX, self._scanPointY

    def _readDataFile(self):
        lines = open(self._filepath, 'rb').readlines()

        trajectories = []
        numberCollisions = None
        collisions = None
        for line in lines:
            if line.startswith(KEYWORD_TRAJECTORY):
                items = line.split()
                if numberCollisions is not None:
                    trajectories.append(collisions)
            elif line.startswith(KEYWORD_SCAN_POINT_X):
                items = line.split()
                if len(items) == 2:
                    try:
                        self._scanPointX = float(items[1])
                    except ValueError:
                        pass
            elif line.startswith(KEYWORD_SCAN_POINT_Y):
                items = line.split()
                if len(items) == 2:
                    try:
                        self._scanPointY = float(items[1])
                    except ValueError:
                        pass
            elif line.startswith(KEYWORD_NUMBER_COLLISIONS):
                if numberCollisions is not None:
                    assert len(collisions) == numberCollisions
                    trajectories.append(collisions)

                items = line.split()
                numberCollisions = int(items[1])
                collisions = []
            elif self._isCollisionDataLine(line):
                collision = self._readCollisionDataLine(line)
                collisions.append(collision)

        self._trajectories = trajectories

    def _isCollisionDataLine(self, line):
        items = line.split()
        if len(items) == 10:
            try:
                float(items[0])
                return True
            except ValueError:
                return False

    def _readCollisionDataLine(self, line):
        items = line.split()

        collision = {}
        collision[X_nm] = float(items[0])
        collision[Y_nm] = float(items[1])
        collision[Z_nm] = float(items[2])

        return collision
