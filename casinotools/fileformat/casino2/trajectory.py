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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools
import casinotools.fileformat.casino2.scattering_event as ScatteringEvent

# Globals and constants variables.

class Trajectory(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, isSkipReadingData=False):
        self._isSkipReadingData = isSkipReadingData

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'

        self.FRetro = self.read_int(file)
        self.FTrans = self.read_int(file)
        self.FDetec = self.read_int(file)
        self.NbColl = self.read_long(file)
        self.Zmax = self.read_double(file)
        self.LPM = self.read_double(file)
        self.DedsM = self.read_double(file)
        self.PhiM = self.read_double(file)
        self.ThetaM = self.read_double(file)
        self.MoyenX = self.read_double(file)
        self.MoyenY = self.read_double(file)
        self.MoyenZ = self.read_double(file)
        self.Display = self.read_int(file)

        self.NbElec = self.read_long(file)

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

