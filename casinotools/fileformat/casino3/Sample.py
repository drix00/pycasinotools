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
#import casinotools.fileformat.casino3.SampleSubtrate as SampleSubtrate
import casinotools.fileformat.casino3.SampleObjectFactory as SampleObjectFactory
import casinotools.fileformat.casino3.SampleTree as SampleTree
import casinotools.fileformat.casino3.Region as Region
import casinotools.fileformat.casino3.Version as Version

# Globals and constants variables.
OFFSET_ROTATION_Y = "offset_rotation_y"
OFFSET_ROTATION_Z = "offset_rotation_z"

class ShapeError(Exception): pass

class Sample(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._file = None
        self._startPosition = 0
        self._endPosition = 0
        self._filePathname = ""
        self._fileDescriptor = 0

        self._sampleObjects = []
        self._regions = []

        self._offsets = {}

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()

        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = b"*CASINOSAMPLE%%"
        if self.find_tag(file, tagID):
            self._version = self.read_int(file)

            if self._version >= 3010301:
                return self._read_3131(file)
            else:
                raise "version_not_supported"

    def _read_3131(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_read_3131", file.tell())

        tagID = b"*SUBSTRATE%%%%%"
        if self.find_tag(file, tagID):
            self._useSubstrate = self.read_int(file)

            self._substrate = SampleObjectFactory.CreateObjectFromType(SampleObjectFactory.SHAPE_SUBSTRATE)
            self._substrate.read(file)

        tagID = b"*SAMPLEOBJECTS%"
        if self.find_tag(file, tagID):
            self._count = self.read_int(file)

            for dummy in range(self._count):
                type = self.read_int(file)

                sampleObject = SampleObjectFactory.CreateObjectFromType(type)

                sampleObject.read(file)

                if self._version >= 30200002:
                    objectId = self.read_int(file)
                    self.addSampleObjectWithId(sampleObject, objectId)
                else:
                    self.addSampleObject(sampleObject)

        if self._version < 30107001:
            tagID = b"*MAC%%%%%%%%%%%"
            if self.find_tag(file, tagID):
                #float MAC[100][100][3]
                #file.read((char*)&MAC,sizeof(MAC[0][0][0]*100*100*3));
                numberElements = 100 * 100 * 3
                self._mac = self.read_float_list(file, numberElements)

        tagID = b"*SAMPLEDATA%%%%"
        if self.find_tag(file, tagID):
            self._maxSampleTreeLevel = self.read_int(file)

        if self._version >= Version.SIM_OPTIONS_VERSION_3_1_8_2:
            self._offsets[OFFSET_ROTATION_Y] = file.tell()
            self._rotationAngleY_deg = self.read_double(file)
            self._offsets[OFFSET_ROTATION_Z] = file.tell()
            self._rotationAngleZ_deg = self.read_double(file)

        self._presence = self.read_int(file)
        if self._presence:
            self._sampleTree = SampleTree.SampleTree()
            self._sampleTree.read(file)

        tagID = b"*REGIONDATA%%%%"
        if self.find_tag(file, tagID):
            self._numberRegions = self.read_int(file)

        #return
        for dummy in range(self._numberRegions):
            regionInfo = Region.Region()
            regionInfo.read(file)

            self.addRegion(regionInfo)

        # TODO calculate regions for the sample's triangles.

    def addSampleObject(self, sampleObject):
        self._sampleObjects.append(sampleObject)

    def addSampleObjectWithId(self, sampleObject, objectId):
        self._sampleObjects.append(sampleObject)

    def addRegion(self, region):
        self._regions.append(region)

    def getRegions(self):
        return self._regions

    def getShapes(self):
        return self._sampleObjects

    def getFirstSphereShape(self):
        for shape in self._sampleObjects:
            type = shape.getType()
            if type == SampleObjectFactory.SHAPE_SPHERE:
                return shape

        raise ShapeError("Shape not found.")

    def getPlaneShapes(self):
        shapes = []
        for shape in self._sampleObjects:
            type = shape.getType()
            if type == SampleObjectFactory.SHAPE_PLANE:
                shapes.append(shape)

        return shapes

    def getVersion(self):
        return self._version

    def getRotationY_deg(self):
        return self._rotationAngleY_deg

    def setRotationY_deg(self, rotationAngle_deg):
        self._rotationAngleY_deg = rotationAngle_deg

    def modifyRotationY_deg(self, rotationAngle_deg):
        self._file.seek(self._offsets[OFFSET_ROTATION_Y])
        self.write_double(self._file, rotationAngle_deg)
        self._rotationAngleY_deg = rotationAngle_deg

    def getRotationZ_deg(self):
        return self._rotationAngleZ_deg

    def setRotationZ_deg(self, rotationAngle_deg):
        self._rotationAngleZ_deg = rotationAngle_deg

    def modifyRotationZ_deg(self, rotationAngle_deg):
        self._file.seek(self._offsets[OFFSET_ROTATION_Z])
        self.write_double(self._file, rotationAngle_deg)
        self._rotationAngleZ_deg = rotationAngle_deg

    def write(self, file):
        pass

    def export(self, export_file):
        # todo: implement the export method.
        self._exportHeader(export_file)
        self._exportVersion(export_file)
        self._exportSubstrate(export_file)
        self._exportSampleObjects(export_file)
        self._exportSampleData(export_file)
        self._exportRegionData(export_file)

    def _exportHeader(self, exportFile):
        line = "-"*80
        self.write_line(exportFile, line)

        line = "%s" % ("Sample")
        self.write_line(exportFile, line)

        line = "-"*40
        self.write_line(exportFile, line)

    def _exportVersion(self, exportFile):
        version = self.getVersion()
        versionString = self._extract_version_string(version)
        line = "File version: %s (%i)" % (versionString, version)
        self.write_line(exportFile, line)

    def _exportSubstrate(self, exportFile):
        text = self._extract_boolean_string(self._useSubstrate)
        line = "Use substract: %s" % (text)
        self.write_line(exportFile, line)

        self._substrate.export(exportFile)

    def _exportSampleObjects(self, exportFile):
        line = "number of sample objects: %i" % (self._count)
        self.write_line(exportFile, line)

        sampleObjectID = 0
        for sampleObject in self._sampleObjects:
            sampleObjectID += 1
            line = "Sample object: %i" % (sampleObjectID)
            self.write_line(exportFile, line)

            sampleObject.export(exportFile)

    def _exportSampleData(self, exportFile):
        line = "Maximum sample tree level: %i" % (self._maxSampleTreeLevel)
        self.write_line(exportFile, line)

        line = "Sample rotation angle Y (deg): %g" % (self._rotationAngleY_deg)
        self.write_line(exportFile, line)

        line = "Sample rotation angle Z (deg): %g" % (self._rotationAngleZ_deg)
        self.write_line(exportFile, line)

        text = self._extract_boolean_string(self._presence)
        line = "Presence: %s" % (text)
        self.write_line(exportFile, line)

        if self._presence:
            self._sampleTree.export(exportFile)

    def _exportRegionData(self, exportFile):
        line = "number of regions: %i" % (self._numberRegions)
        self.write_line(exportFile, line)

        sampleRegionID = 0
        for region in self._regions:
            sampleRegionID += 1
            line = "Sample region: %i" % (sampleRegionID)
            self.write_line(exportFile, line)

            region.export(exportFile)
