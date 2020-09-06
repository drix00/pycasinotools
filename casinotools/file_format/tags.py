#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.tags
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
"""

###############################################################################
# Copyright 2020 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import logging
import struct

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
TAG_LENGTH = 15
BUFFER_LENGTH = 500


def limited_search_tag(file, tag_id, search_length, tag_length=0, filler=b'%'):
    tag = _create_tag_with_filler(tag_id, tag_length, filler)

    is_tag_found = _limited_stream_search(file, tag, search_length)

    return is_tag_found


def _create_tag_with_filler(tag_id, tag_length, filler):
    assert isinstance(tag_id, bytes)
    assert isinstance(filler, bytes)

    tag = tag_id

    number_filler = tag_length - len(tag)
    if number_filler > 0:
        tag += filler * number_filler

    return tag


def _limited_stream_search(file, tag, search_length):
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :param search_length: Search only this length in the file.
    :rtype: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    start_pos = file.tell()

    buffer = file.read(search_length)
    tag_pos = buffer.find(tag)

    if tag_pos == -1:
        file.seek(start_pos)
        return False
    else:
        # Add one for the null character used in the tag.
        file_position = start_pos + tag_pos + len(tag) + 1
        file.seek(file_position)
        return True


def find_tag(file, tag_id):
    return _search_tag(file, tag_id, TAG_LENGTH)


def _search_tag(file, tag_id, tag_length=0, filler=b'%'):
    tag = _create_tag_with_filler(tag_id, tag_length, filler)

    is_tag_found = _stream_search_fast(file, tag)

    return is_tag_found


def find_tag_position(file, tag_id):
    filler = b'%'
    tag = _create_tag_with_filler(tag_id, TAG_LENGTH, filler)
    position = _stream_search_position_fast(file, tag)
    return position


def add_tag(file, tag_id, tag_length=TAG_LENGTH, filler=b'%'):
    start_pos = file.tell()
    tag = _create_tag_with_filler(tag_id, tag_length, filler)
    tag += b"\0"
    size = len(tag)
    buffer = struct.pack("i", size)
    file.write(buffer)
    file.write(tag)
    size_int = struct.calcsize("i")
    assert file.tell() == start_pos + size_int + tag_length + 1


def add_tag_old(file, tag_id, tag_length=TAG_LENGTH, filler=b'%'):
    start_pos = file.tell()
    tag = _create_tag_with_filler(tag_id, tag_length, filler)
    tag += b"\0"
    file.write(tag)
    assert file.tell() == start_pos + tag_length + 1


def _stream_search_slow(file, tag):
    logging.debug("streamSearch looking for tag: %s", tag)
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :rtype: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    start_pos = file.tell()

    buffer = file.read()
    tag_pos = buffer.find(tag)

    if tag_pos != -1:
        # Add one for the null character used in the tag.
        file_position = start_pos + tag_pos + len(tag) + 1
        file.seek(file_position)
        return True
    else:
        file.seek(start_pos)
        return False


def _stream_search_fast(file, tag):
    logging.debug("streamSearch looking for tag: %s", tag)
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :rtype: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    start_pos = file.tell()
    buffer = b""
    temp_buffer = file.read(BUFFER_LENGTH)
    while temp_buffer != b'':
        # logging.debug("File position in streamSearch: %i", file.tell())
        buffer += temp_buffer
        tag_pos = buffer.find(tag)

        if tag_pos != -1:
            # Add one for the null character used in the tag.
            file_position = start_pos + tag_pos + len(tag) + 1
            file.seek(file_position)
            logging.debug("streamSearch find tag %s at %i", tag, file.tell())
            return True
        temp_buffer = file.read(BUFFER_LENGTH)
    else:
        file.seek(start_pos)
        logging.error("streamSearch did not find tag %s at %i", tag, file.tell())
        return False


def _stream_search_position_fast(file, tag):
    logging.debug("streamSearch looking for tag: %s", tag)
    """
    Search a stream for a tag with a limited length search.

    :param file: Already opened file object.
    :param tag: Text tag to search in the file.
    :rtype: bool
    :return: True if the tag is found and the file is at the position after the tag.
    :return: The file position is reset to the origin position if tag is not found.
    """

    start_pos = file.tell()
    buffer = b""
    temp_buffer = file.read(BUFFER_LENGTH)
    while temp_buffer != b'':
        # logging.debug("File position in streamSearch: %i", file.tell())
        buffer += temp_buffer
        tag_pos = buffer.find(tag)

        if tag_pos != -1:
            # Add one for the null character used in the tag.
            file_position = start_pos + tag_pos + len(tag) + 1
            file.seek(file_position)
            logging.debug("streamSearch find tag %s at %i", tag, file.tell())
            return file_position
        temp_buffer = file.read(BUFFER_LENGTH)
    else:
        file.seek(start_pos)
        logging.error("streamSearch did not find tag %s at %i", tag, file.tell())
        return 0
