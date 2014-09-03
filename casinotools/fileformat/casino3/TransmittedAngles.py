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
import os

# Third party modules.
import numpy as np

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.

class TransmittedAngles(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._file = None
        self._startPosition = 0
        self._startPositionCollisions = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

        self._angles = None
        self._binnedAngles = None

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._numberTransmittedElectrons = self.readInt(file)
        self._numberTransmittedDetectedElectrons = self.readInt(file)

        self._numberAngles = self.readInt(file)
        self._startPosition = file.tell()
        skipOffset = self.getSizeOfDoubleList(self._numberAngles)
        file.seek(skipOffset, os.SEEK_CUR)

        self._numberBinnedAngles = self.readInt(file)
        skipOffset = self.getSizeOfIntList(self._numberBinnedAngles)
        file.seek(skipOffset, os.SEEK_CUR)

        self._endPosition = file.tell()
        logging.debug("File position at the end of %s.%s: %i", self.__class__.__name__, "read", self._endPosition)

    def _readAngleValues(self):
        self._file.seek(self._startPosition)
        self._angles = self.readDoubleList(self._file, self._numberAngles)

        self._numberBinnedAngles = self.readInt(self._file)
        self._binnedAngles = self.readIntList(self._file, self._numberBinnedAngles)

    def getAngles(self):
        if self._angles is None:
            self._readAngleValues()

        return self._angles

    def getBinnedAngles(self):
        if self._binnedAngles is None:
            self._readAngleValues()

        return self._binnedAngles

    def getTransmittedDetectedElectrons(self, betaMin, betaMax):
        if self._numberAngles > 0:
            return self.getTransmittedDetectedElectronsByAngles(betaMin, betaMax)
        elif self._numberBinnedAngles > 0:
            return self.getTransmittedDetectedElectronsByBinnedAngles(betaMin, betaMax)

    def getTransmittedDetectedElectronsByAngles(self, betaMin_mrad, betaMax_mrad):
        if self._angles is None:
            self._readAngleValues()

        if betaMin_mrad == None:
            betaMin_rad = min(self._angles)
        else:
            betaMin_rad = betaMin_mrad * 1.0e-3

        if betaMax_mrad == None:
            betaMax_rad = max(self._angles)
        else:
            betaMax_rad = betaMax_mrad * 1.0e-3

        angles = np.array(self._angles)
        numberDetectedElectrons = np.ma.masked_outside(angles, betaMin_rad, betaMax_rad).count()

        return numberDetectedElectrons

    def getTransmittedDetectedElectronsByBinnedAngles(self, betaMin, betaMax):
        if self._binnedAngles is None:
            self._readAngleValues()

        startAngle_mrad = 0.0
        stopAngle_mrad = (np.pi / 2.0) * 1.0e3
        numberAngles = self._numberBinnedAngles
        angles = np.linspace(startAngle_mrad, stopAngle_mrad, numberAngles)
        assert len(angles) == len(self._binnedAngles)

        for index, angle in enumerate(angles):
            if angle >= betaMin:
                indexMin = index
                break

        for index, angle in enumerate(angles):
            if angle <= betaMax:
                indexMax = index

        numberElectrons = sum(self._binnedAngles[indexMin:indexMax + 1])
        return numberElectrons
