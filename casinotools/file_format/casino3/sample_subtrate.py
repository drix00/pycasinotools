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
#import casinotools.file_format.FileReaderWriterTools as FileReaderWriterTools
import casinotools.file_format.casino3.sample_object as SampleObject

# Globals and constants variables.

class Edge(object):
    def read(self, file):
        pass
        #raise NotImplementedError

class SampleSubtrate(SampleObject.SampleObject):
    def __init__(self, type=None):
        super(SampleSubtrate, self).__init__(type)

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        super(SampleSubtrate, self).read(file)

        self._numberEdges = self.read_int(file)

        self._edges = []
        for dummyIndex in range(self._numberEdges):
            edge = Edge()
            edge.read(file)
            self._edges.append(edge)

    def export(self, export_file):
        # todo: implement the export method.
        logging.error("implement the export method.")
