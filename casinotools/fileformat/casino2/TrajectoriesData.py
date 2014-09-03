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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.Trajectory as Trajectory

# Globals and constants variables.

class TrajectoriesData(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, isSkipReadingData=False):
        self._isSkipReadingData = isSkipReadingData

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = b"*TRAJDATA%%%%%%"
        self.findTag(file, tagID)

        self._numberTrajectories = self.readLong(file)

        self._trajectories = []
        for dummy in range(self._numberTrajectories):
            trajectory = Trajectory.Trajectory(self._isSkipReadingData)
            trajectory.read(file)
            self._trajectories.append(trajectory)

    def getTrajectories(self):
        return self._trajectories
