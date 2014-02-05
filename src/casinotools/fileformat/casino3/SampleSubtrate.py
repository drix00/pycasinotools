#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import logging

# Third party modules.

# Local modules.
#import casinoTools.FileFormat.casino3.FileReaderWriterTools as FileReaderWriterTools
import casinoTools.FileFormat.casino3.SampleObject as SampleObject

# Globals and constants variables.

class Edge(object):
    def read(self, file):
        pass
        #raise NotImplementedError

class SampleSubtrate(SampleObject.SampleObject):
    def __init__(self, type=None):
        super(SampleSubtrate, self).__init__(type)
    
    def read(self, file):
        assert file.mode == 'rb'
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)
        
        super(SampleSubtrate, self).read(file)
        
        self._numberEdges = self.readInt(file)
        
        self._edges = []
        for dummyIndex in xrange(self._numberEdges):
            edge = Edge()
            edge.read(file)
            self._edges.append(edge)
    
    def export(self, exportFile):
        # todo: implement the export method.
        logging.error("implement the export method.")
    
if __name__ == '__main__':    #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
