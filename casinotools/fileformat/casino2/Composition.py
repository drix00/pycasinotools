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

# Globals and constants variables.

class Composition(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self.NuEl = 0
        self.FWt = 1.0
        self.FAt = 1.0
        self.SigmaT = 0.0
        self.SigmaTIne = 0.0
        self.Rep = 1

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        self.NuEl = self.readInt(file)
        self.FWt = self.readDouble(file)
        self.FAt = self.readDouble(file)
        self.SigmaT = self.readDouble(file)
        self.SigmaTIne = self.readDouble(file)
        self.Rep = self.readInt(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        self.writeInt(file, self.NuEl)
        self.writeDouble(file, self.FWt)
        self.writeDouble(file, self.FAt)
        self.writeDouble(file, self.SigmaT)
        self.writeDouble(file, self.SigmaTIne)
        self.writeInt(file, self.Rep)

    def setIndex(self, index):
        self.NuEl = index

    def setWeightFraction(self, weightFraction):
        self.FWt = weightFraction

    def setAtomicFraction(self, fraction):
        self.FAt = fraction
