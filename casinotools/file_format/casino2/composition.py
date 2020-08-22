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
import casinotools.file_format.file_reader_writer_tools as FileReaderWriterTools

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

        self.NuEl = self.read_int(file)
        self.FWt = self.read_double(file)
        self.FAt = self.read_double(file)
        self.SigmaT = self.read_double(file)
        self.SigmaTIne = self.read_double(file)
        self.Rep = self.read_int(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        self.write_int(file, self.NuEl)
        self.write_double(file, self.FWt)
        self.write_double(file, self.FAt)
        self.write_double(file, self.SigmaT)
        self.write_double(file, self.SigmaTIne)
        self.write_int(file, self.Rep)

    def setIndex(self, index):
        self.NuEl = index

    def setWeightFraction(self, weightFraction):
        self.FWt = weightFraction

    def setAtomicFraction(self, fraction):
        self.FAt = fraction
