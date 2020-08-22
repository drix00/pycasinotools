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
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools
import casinotools.fileformat.casino3.SampleShape.shape_type as ShapeType

# Globals and constants variables.

class SampleObject(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, type):
        self._version = None
        self._name = "Empty"
        self._regionName = "Undefined"

        self._translation = []
        self._rotation = []
        self._scale = [1.0, 1.0, 1.0]
        self._color = [0.0, 0.0, 1.0]

        self._type = type

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        tagID = b"%SMPLOBJ"
        if self.find_tag(file, tagID):
            self._version = self.read_int(file)

            self._name = self.read_str(file)
            self._regionName = self.read_str(file)

            self._translation = self.read_double_list(file, 3)
            self._rotation = self.read_double_list(file, 3)
            self._scale = self.read_double_list(file, 3)
            self._color = self.read_double_list(file, 3)

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def getVersion(self):
        return self._version

    def getTranslation_nm(self):
        return self._translation

    def getScale_nm(self):
        return self._scale

    def export(self, export_file):
        self._exportVersion(export_file)
        self._exportType(export_file)
        self._exportName(export_file)
        self._exportRegionName(export_file)
        self._exportTranslation(export_file)
        self._exportRotation(export_file)
        self._exportScale(export_file)
        self._exportColor(export_file)

    def _exportVersion(self, exportFile):
        version = self.getVersion()
        versionString = self._extract_version_string(version)
        line = "Sample object version: %s (%i)" % (versionString, version)
        self.write_line(exportFile, line)

    def _exportType(self, exportFile):
        typeStr = ShapeType.getString(self._type)
        line = "Type: %s" % (typeStr)
        self.write_line(exportFile, line)

    def _exportName(self, exportFile):
        line = "Name: %s" % (self._name)
        self.write_line(exportFile, line)

    def _exportRegionName(self, exportFile):
        line = "Region name: %s" % (self._regionName)
        self.write_line(exportFile, line)

    def _exportTranslation(self, exportFile):
        line = "Translation:"
        self.write_line(exportFile, line)

        for label, value in zip(["X", 'Y', 'Z'], self._translation):
            line = "\t%s: %g" % (label, value)
            self.write_line(exportFile, line)

    def _exportRotation(self, exportFile):
        line = "Rotation:"
        self.write_line(exportFile, line)

        for label, value in zip(["X", 'Y', 'Z'], self._rotation):
            line = "\t%s: %g" % (label, value)
            self.write_line(exportFile, line)

    def _exportScale(self, exportFile):
        line = "Scale:"
        self.write_line(exportFile, line)

        for label, value in zip(["X", 'Y', 'Z'], self._scale):
            line = "\t%s: %g" % (label, value)
            self.write_line(exportFile, line)

    def _exportColor(self, exportFile):
        line = "Color:"
        self.write_line(exportFile, line)

        for label, value in zip(["R", 'G', 'B'], self._color):
            line = "\t%s: %g" % (label, value)
            self.write_line(exportFile, line)

    def modifyPositionZ(self, newPositionZ_nm):
        if not self._file.closed:
            currentPosition = self._file.tell()
            self._file.close()
        else:
            currentPosition = 0

        self._file = open(self._filePathname, 'r+b')

        self._file.seek(self._startPosition)
        self._translation = (self._translation[0], self._translation[1], newPositionZ_nm)

        self._modify(self._file)

        self._file.close()
        self._file = open(self._filePathname, 'rb')
        self._file.seek(currentPosition)

    def _modify(self, file):
        assert file.mode == 'r+b'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write", file.tell())

        tagID = "%SMPLOBJ"
        if self.find_tag(file, tagID):
            self.write_int(file, self._version)

            self.write_str(file, self._name)
            self.write_str(file, self._regionName)

            self.write_double_list(file, self._translation, 3)
            self.write_double_list(file, self._rotation, 3)
            self.write_double_list(file, self._scale, 3)
            self.write_double_list(file, self._color, 3)
