#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import struct

# Third party modules.

# Local modules.
import casinotools.fileformat.Tags as Tags

# Globals and constants variables.

class FileReaderWriterTools(object):
    def findTag(self, file, tagID):
        return Tags.searchTag(file, tagID, Tags.TAG_LENGTH)

    def addTagOld(self, file, tagID):
        return Tags.addTagOld(file, tagID, Tags.TAG_LENGTH)

    def addTag(self, file, tagID):
        return Tags.addTag(file, tagID, Tags.TAG_LENGTH)

    def readInt(self, file):
        format = "i"
        value = self._read(file, format, int)
        return value

    def readLong(self, file):
        # TODO: Check if using i in the format is not a bug.
        format = "i"
        value = self._read(file, format, int)
        return value

    def readDouble(self, file):
        format = "d"
        value = self._read(file, format, float)
        return value

    def readFloat(self, file):
        format = "f"
        value = self._read(file, format, float)
        return value

    def readBool(self, file):
        format = "?"
        value = self._read(file, format, bool)
        return value

    def readStr(self, file):
        size = self.readInt(file)
        #self.readInt(file)
        return self.readStrLength(file, size)

    def readStrLength(self, file, size):
        format = "%is" % (size)
        value = self._read(file, format, bytes)
        value = value.decode('ascii', 'replace')
        value = value.replace('\x00', '')
        return value

    def readFloatList(self, file, numberElements):
        return self._readFloatListWithoutLoopFast(file, numberElements)

    def _readFloatListWithoutLoopFast(self, file, numberElements):
        format = "%if" % (numberElements)
        size = struct.calcsize(format)
        buffer = file.read(size)
        items = struct.unpack_from(format, buffer)

        return items

    def readDoubleList(self, file, numberElements=None):
        if numberElements is None:
            #numberElements = self.readLong(file)
            numberElements = self.readInt(file)

        return self._readDoubleListWithoutLoopFast(file, numberElements)

    def _readDoubleListWithLoop(self, file, numberElements):
        array = []
        for dummy in range(numberElements):
            value = self.readDouble(file)
            array.append(value)

        return array

    def _readDoubleListWithoutLoop(self, file, numberElements):
        format = "%id" % (numberElements)
        size = struct.calcsize(format)
        buffer = file.read(size)
        items = struct.unpack_from(format, buffer)
        array = [float(item) for item in items]

        return array

    def _readDoubleListWithoutLoopFast(self, file, numberElements):
        if numberElements > 0:
            format = "%id" % (numberElements)
            size = struct.calcsize(format)
            buffer = file.read(size)
            items = struct.unpack_from(format, buffer)

            return items
        else:
            return []

    def readIntList(self, file, numberElements):
        return self._readIntListWithoutLoopFast(file, numberElements)

    def _readIntListWithoutLoopFast(self, file, numberElements):
        format = "%ii" % (numberElements)
        size = struct.calcsize(format)
        buffer = file.read(size)
        items = struct.unpack_from(format, buffer)

        return items

    def getSizeOfDoubleList(self, numberElements):
        format = "%id" % (numberElements)
        size = struct.calcsize(format)
        return size

    def getSizeOfIntList(self, numberElements):
        format = "%ii" % (numberElements)
        size = struct.calcsize(format)
        return size

    def _read(self, file, format, type):
        size = struct.calcsize(format)
        buffer = file.read(size)
        items = struct.unpack_from(format, buffer)
        return type(items[0])

    def readMultipleValues(self, file, format):
        size = struct.calcsize(format)
        buffer = file.read(size)
        items = struct.unpack_from(format, buffer)
        return items

    def writeStrLength(self, file, value, size):
        value = self._checkAndCorrectValueSize(value, size)
        format = "%is" % (size,)
        value = value.encode('ascii', 'replace')
        self._write(file, format, value, bytes)

    def _checkAndCorrectValueSize(self, value, size):
        if len(value) > size:
            value = value[:size]
        assert len(value) <= size
        return value

    def writeInt(self, file, value):
        format = "i"
        self._write(file, format, value, int)

    def writeDouble(self, file, value):
        format = "d"
        self._write(file, format, value, float)

    def writeLong(self, file, value):
        format = "=l"
        self._write(file, format, value, int)

    def writeBool(self, file, value):
        format = "?"
        self._write(file, format, value, bool)

    def writeFloat(self, file, value):
        format = "f"
        self._write(file, format, value, float)

    def writeStr(self, file, value):
        size = len(value)
        self.writeInt(file, size)
        self.writeStrLength(file, value, size)

    def writeDoubleList(self, file, valueList, numberElements):
        assert len(valueList) == numberElements
        self._writeDoubleListWithoutLoop(file, valueList, numberElements)

    def _writeDoubleListWithLoop(self, file, valueList, numberElements):
        for index in range(numberElements):
            self.writeDouble(file, valueList[index])

    def _writeDoubleListWithoutLoop(self, file, valueList, numberElements):
        format = "%id" % (numberElements)
        buffer = struct.pack(format, *valueList)
        file.write(buffer)

    def _write(self, file, format, value, type):
        value = type(value)
        buffer = struct.pack(format, value)
        file.write(buffer)
        file.flush()

    def export(self, exportFile):
            raise NotImplementedError

    def writeLine(self, file, line):
            if not line.endswith('\n'):
                    line += '\n'
            file.write(line)

    def _extractVersionString(self, version):
        """
        30103040
        """
        text = str(version)

        major = int(text[0])
        minor = int(text[1:3])
        revision = int(text[3:5])
        build = int(text[5:])

        versionStr = "%s.%s.%s.%s" % (major, minor, revision, build)
        return versionStr

    def _extractBooleanString(self, booleanValue):
        booleanValue = bool(booleanValue)

        if booleanValue:
            return "true"
        else:
            return "false"
