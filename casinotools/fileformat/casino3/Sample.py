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
        if self.findTag(file, tagID):
            self._version = self.readInt(file)

            if self._version >= 3010301:
                return self._read_3131(file)
            else:
                raise "version_not_supported"

    def _read_3131(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_read_3131", file.tell())

        tagID = b"*SUBSTRATE%%%%%"
        if self.findTag(file, tagID):
            self._useSubstrate = self.readInt(file)

            self._substrate = SampleObjectFactory.CreateObjectFromType(SampleObjectFactory.SHAPE_SUBSTRATE)
            self._substrate.read(file)

        tagID = b"*SAMPLEOBJECTS%"
        if self.findTag(file, tagID):
            self._count = self.readInt(file)

            for dummy in range(self._count):
                type = self.readInt(file)

                sampleObject = SampleObjectFactory.CreateObjectFromType(type)

                sampleObject.read(file)

                if self._version >= 30200002:
                    objectId = self.readInt(file)
                    self.addSampleObjectWithId(sampleObject, objectId)
                else:
                    self.addSampleObject(sampleObject)

        if self._version < 30107001:
            tagID = b"*MAC%%%%%%%%%%%"
            if self.findTag(file, tagID):
                #float MAC[100][100][3]
                #file.read((char*)&MAC,sizeof(MAC[0][0][0]*100*100*3));
                numberElements = 100 * 100 * 3
                self._mac = self.readFloatList(file, numberElements)

        tagID = b"*SAMPLEDATA%%%%"
        if self.findTag(file, tagID):
            self._maxSampleTreeLevel = self.readInt(file)

        if self._version >= Version.SIM_OPTIONS_VERSION_3_1_8_2:
            self._offsets[OFFSET_ROTATION_Y] = file.tell()
            self._rotationAngleY_deg = self.readDouble(file)
            self._offsets[OFFSET_ROTATION_Z] = file.tell()
            self._rotationAngleZ_deg = self.readDouble(file)

        self._presence = self.readInt(file)
        if self._presence:
            self._sampleTree = SampleTree.SampleTree()
            self._sampleTree.read(file)

        tagID = b"*REGIONDATA%%%%"
        if self.findTag(file, tagID):
            self._numberRegions = self.readInt(file)

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
        self.writeDouble(self._file, rotationAngle_deg)
        self._rotationAngleY_deg = rotationAngle_deg

    def getRotationZ_deg(self):
        return self._rotationAngleZ_deg

    def setRotationZ_deg(self, rotationAngle_deg):
        self._rotationAngleZ_deg = rotationAngle_deg

    def modifyRotationZ_deg(self, rotationAngle_deg):
        self._file.seek(self._offsets[OFFSET_ROTATION_Z])
        self.writeDouble(self._file, rotationAngle_deg)
        self._rotationAngleZ_deg = rotationAngle_deg

    def write(self, file):
        pass

    def export(self, exportFile):
        # todo: implement the export method.
        self._exportHeader(exportFile)
        self._exportVersion(exportFile)
        self._exportSubstrate(exportFile)
        self._exportSampleObjects(exportFile)
        self._exportSampleData(exportFile)
        self._exportRegionData(exportFile)

    def _exportHeader(self, exportFile):
        line = "-"*80
        self.writeLine(exportFile, line)

        line = "%s" % ("Sample")
        self.writeLine(exportFile, line)

        line = "-"*40
        self.writeLine(exportFile, line)

    def _exportVersion(self, exportFile):
        version = self.getVersion()
        versionString = self._extractVersionString(version)
        line = "File version: %s (%i)" % (versionString, version)
        self.writeLine(exportFile, line)

    def _exportSubstrate(self, exportFile):
        text = self._extractBooleanString(self._useSubstrate)
        line = "Use substract: %s" % (text)
        self.writeLine(exportFile, line)

        self._substrate.export(exportFile)

    def _exportSampleObjects(self, exportFile):
        line = "number of sample objects: %i" % (self._count)
        self.writeLine(exportFile, line)

        sampleObjectID = 0
        for sampleObject in self._sampleObjects:
            sampleObjectID += 1
            line = "Sample object: %i" % (sampleObjectID)
            self.writeLine(exportFile, line)

            sampleObject.export(exportFile)

    def _exportSampleData(self, exportFile):
        line = "Maximum sample tree level: %i" % (self._maxSampleTreeLevel)
        self.writeLine(exportFile, line)

        line = "Sample rotation angle Y (deg): %g" % (self._rotationAngleY_deg)
        self.writeLine(exportFile, line)

        line = "Sample rotation angle Z (deg): %g" % (self._rotationAngleZ_deg)
        self.writeLine(exportFile, line)

        text = self._extractBooleanString(self._presence)
        line = "Presence: %s" % (text)
        self.writeLine(exportFile, line)

        if self._presence:
            self._sampleTree.export(exportFile)

    def _exportRegionData(self, exportFile):
        line = "number of regions: %i" % (self._numberRegions)
        self.writeLine(exportFile, line)

        sampleRegionID = 0
        for region in self._regions:
            sampleRegionID += 1
            line = "Sample region: %i" % (sampleRegionID)
            self.writeLine(exportFile, line)

            region.export(exportFile)
