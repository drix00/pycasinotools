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
import struct

# Third party modules.

# Local modules.

# Globals and constants variables.
TAG_LENGTH = 15
BUFFER_LENGTH = 500

def limitedSearchTag(file, tagID, searchLength, tagLenght=0, filler=b'%'):
    tag = createTagWithFiller(tagID, tagLenght, filler)

    isTagFound = limitedStreamSearch(file, tag, searchLength)

    return isTagFound

def createTagWithFiller(tagID, tagLenght, filler):
    assert isinstance(tagID, bytes)
    assert isinstance(filler, bytes)

    tag = tagID

    numberFiller = tagLenght - len(tag)
    if numberFiller > 0:
        tag += filler * numberFiller

    return tag

def limitedStreamSearch(file, tag, searchLength):
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :param searchLength: Search only this length in the file.
    :rtpye: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    startPos = file.tell()

    buffer = file.read(searchLength)
    tagPos = buffer.find(tag)

    if tagPos == -1:
        file.seek(startPos)
        return False
    else:
        # Add one for the null character used in the tag.
        filePosition = startPos + tagPos + len(tag) + 1
        file.seek(filePosition)
        return True

def searchTag(file, tagID, tagLenght=0, filler=b'%'):
    tag = createTagWithFiller(tagID, tagLenght, filler)

    isTagFound = _streamSearchFast(file, tag)

    return isTagFound

def addTag(file, tagID, tagLenght=0, filler=b'%'):
    startPos = file.tell()
    tag = createTagWithFiller(tagID, tagLenght, filler)
    tag += "\0"
    size = len(tag)
    buffer = struct.pack("i", size)
    file.write(buffer)
    file.write(tag)
    size = struct.calcsize("i")
    assert file.tell() == startPos + size + tagLenght + 1

def addTagOld(file, tagID, tagLenght=0, filler=b'%'):
    startPos = file.tell()
    tag = createTagWithFiller(tagID, tagLenght, filler)
    tag += b"\0"
    file.write(tag)
    assert file.tell() == startPos + tagLenght + 1

def _streamSearchSlow(file, tag):
    logging.debug("streamSearch looking for tag: %s", tag)
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :rtpye: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    startPos = file.tell()

    buffer = file.read()
    tagPos = buffer.find(tag)

    if tagPos != -1:
        # Add one for the null character used in the tag.
        filePosition = startPos + tagPos + len(tag) + 1
        file.seek(filePosition)
        return True
    else:
        file.seek(startPos)
        return False

def _streamSearchFast(file, tag):
    logging.debug("streamSearch looking for tag: %s", tag)
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :rtpye: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    startPos = file.tell()
    buffer = b""
    tempBuffer = file.read(BUFFER_LENGTH)
    while tempBuffer != b'':
        #logging.debug("File position in streamSearch: %i", file.tell())
        buffer += tempBuffer
        tagPos = buffer.find(tag)

        if tagPos != -1:
            # Add one for the null character used in the tag.
            filePosition = startPos + tagPos + len(tag) + 1
            file.seek(filePosition)
            logging.debug("streamSearch find tag %s at %i", tag, file.tell())
            return True
        tempBuffer = file.read(BUFFER_LENGTH)
    else:
        file.seek(startPos)
        logging.error("streamSearch did not find tag %s at %i", tag, file.tell())
        return False
