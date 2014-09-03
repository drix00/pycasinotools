#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.ScatteringEvent as ScatteringEvent

# Globals and constants variables.

class Trajectory(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, isSkipReadingData=False):
        self._isSkipReadingData = isSkipReadingData

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self.FRetro = self.readInt(file)
        self.FTrans = self.readInt(file)
        self.FDetec = self.readInt(file)
        self.NbColl = self.readLong(file)
        self.Zmax = self.readDouble(file)
        self.LPM = self.readDouble(file)
        self.DedsM = self.readDouble(file)
        self.PhiM = self.readDouble(file)
        self.ThetaM = self.readDouble(file)
        self.MoyenX = self.readDouble(file)
        self.MoyenY = self.readDouble(file)
        self.MoyenZ = self.readDouble(file)
        self.Display = self.readInt(file)

        self.NbElec = self.readLong(file)

        self._scatteringEvents = []
        if not self._isSkipReadingData:
            for dummy in range(self.NbElec):
                event = ScatteringEvent.ScatteringEvent()
                event.read(file)
                self._scatteringEvents.append(event)
        else:
            offset = ScatteringEvent.ScatteringEvent().getSkipOffset()
            offset *= self.NbElec
            file.seek(offset, os.SEEK_CUR)

    def isBackscattered(self):
        return bool(self.FRetro)

    def isTransmitted(self):
        return bool(self.FTrans)

    def isAbsorbed(self):
        return not self.isBackscattered() and not self.isTransmitted()

    def getScatteringEvents(self):
        return self._scatteringEvents

