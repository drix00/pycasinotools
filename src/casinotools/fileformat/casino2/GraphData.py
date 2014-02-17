#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2908 $"
__svnDate__ = "$Date: 2013-03-31 10:32:54 -0400 (Sun, 31 Mar 2013) $"
__svnId__ = "$Id: GraphData.py 2908 2013-03-31 14:32:54Z ppinard $"

# Standard library modules.
import math

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.
class GraphData(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, size=0, borneInf=0.0, borneSup=0.0,
                     isLog=False, isUneven=False,
                     title="", xTitle="",
                     yTitle="", file=None):
        if file != None:
            self.read(file)
        else:
            self._size = size
            self._borneInf = borneInf
            self._borneSup = borneSup
            self._isLog = isLog
            self._isUneven = isUneven
            self._title = title
            self._xTitle = xTitle
            self._yTitle = yTitle
            self._values = []
            self._positions = None

    def add(self, value):
        self._values.append(value)

    def read(self, file):
        assert file.mode == 'rb'
        self._version = self.readLong(file)
        if self._version >= 2040601:
            self._size = self.readLong(file)
            self._borneInf = self.readDouble(file)
            self._borneSup = self.readDouble(file)
            self._isLog = self.readInt(file)
            self._isUneven = self.readInt(file)

            self._title = self.readStr(file)
            self._xTitle = self.readStr(file)
            self._yTitle = self.readStr(file)

            self._values = []
            self._positions = []
            for dummy in xrange(self._size):
                value = self.readDouble(file)
                self._values.append(value)

                if self._isUneven:
                    position = self.readDouble(file)
                    self._positions.append(position)

            if not self._isUneven:
                for i in xrange(self._size):
                    position = self.index2pos(i)
                    self._positions.append(position)

            assert len(self._values) == len(self._positions)

    def index2pos(self, Index):
        XSup = self._borneSup
        XInf = self._borneInf
        nbPoints = self._size
        FLog = self._isLog

        assert(XSup >= XInf)
        assert(nbPoints > 0)

        if nbPoints == 1:
            return XInf

        if Index <= 0:
            return XInf

        if FLog:
            assert(XSup > 0)
            assert(XInf > 0)

            Point = (float(Index)/float(nbPoints-1))
            exp = Point*(math.log10(XSup)-math.log10(XInf)) + math.log10(XInf)
            Point = pow(10.0, exp)
            return Point
        else:
            Point = (float(Index)/float(nbPoints-1))
            Point = Point * (XSup-XInf) + XInf
            return Point

    def getPositions(self):
        if self._positions is None:
            self._positions = [self.index2pos(i) for i in range(self._size)]

        return self._positions

    def getValues(self):
        return self._values

if __name__ == '__main__':    #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
