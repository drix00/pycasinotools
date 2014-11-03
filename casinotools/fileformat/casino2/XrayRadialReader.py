#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.casino2.XrayRadial as XrayRadial

# Globals and constants variables.
K = 'K'
L = 'LIII'
M = 'MV'
HEADER_ELEMENT_LINE = "Radial XRay Distribution"
HEADER_ELEMENT = "Radial Distribution of"
HEADER_ALL = "XRay Radial of"

class XrayRadialReader(object):
    def __init__(self):
        self._data = {}
        self._labels = []
        self._currentElementSymbol = None
        self._currentLine = None

    def readTextFile(self, filepath):
        with open(filepath, 'r') as fp:
            lines = fp.readlines()

        self._setTextFileVersion(lines[0])

        for line in lines:
            if self._isHeaderLine(line):
                self._extractHeaderLineData(line)
            elif self._isDataLabelLine(line):
                self._extractDataLabelLineData(line)
            elif self._isValueLine(line):
                self._extractValueLineData(line)

    def _setTextFileVersion(self, line):
        if line.startswith(HEADER_ELEMENT_LINE):
            self._version = HEADER_ELEMENT_LINE
            self._extractHeaderLineData = self._extractHeaderLineDataElementLine
            self._extractDataLabelLineData = self._extractDataLabelLineDataElementLine
        elif line.startswith(HEADER_ELEMENT):
            self._version = HEADER_ELEMENT
            self._extractHeaderLineData = self._extractHeaderLineDataElement
            self._extractDataLabelLineData = self._extractDataLabelLineDataElement
        elif line.startswith(HEADER_ALL):
            self._version = HEADER_ALL
            self._extractHeaderLineData = self._extractHeaderLineDataElement
            self._extractDataLabelLineData = self._extractDataLabelLineDataElement

    def _isHeaderLine(self, line):
        return line.startswith(self._version)

    def _extractHeaderLineDataElementLine(self, line):
        dummy, line = line.split('Layer')
        items = line.split('of Element')
        self._currentLine = items[0].strip()
        self._currentElementSymbol = items[1].strip()

    def _extractHeaderLineDataElement(self, line):
        dummy, symbol = line.split(self._version)
        self._currentElementSymbol = symbol.strip()

    def _isDataLabelLine(self, line):
        return line.startswith(XrayRadial.DISTANCE_nm[:-5])

    def _extractDataLabelLineDataElementLine(self, line):
        items = line.split('\t')

        self._labels = []
        for item in items:
            self._labels.append(item.strip())

    def _extractDataLabelLineDataElement(self, line):
        items = line.split('\t')

        self._labels = []
        if items[0] == "Distance(nm)":
            self._labels.append(XrayRadial.DISTANCE_nm)

        for item in items[1:]:
            label, xrayline = item.split(':')
            if xrayline.strip().endswith('ABS'):
                label = XrayRadial.INTENSITY_ABSORBED
                xrayline = xrayline[0]

            self._labels.append((xrayline, label))

    def _isValueLine(self, line):
        try:
            dummy = float(line.split('\t')[0])
            return True
        except:
            return False

    def _extractValueLineData(self, line):
        symbol = self._currentElementSymbol
        xrayLine = self._currentLine

        items = line.split('\t')

        for label, item in zip(self.getDataLabels(), items):
            if isinstance(label, tuple):
                self._currentLine = label[0]
                xrayLine = self._currentLine

            self._data.setdefault(symbol, {})
            self._data[symbol].setdefault(xrayLine, XrayRadial.XrayRadial())
            xrayRadialData = self._data[symbol][xrayLine]
            xrayRadialData.setLine(xrayLine)
            xrayRadialData.setElementSymbol(symbol)
            xrayRadialData.setLabels(self.getDataLabels())
            try:
                value = float(item)
            except ValueError:
                value = 0.0

            xrayRadialData.addData(label, value)

    def getDataLabels(self):
        return self._labels

    def getData(self, elementSymbol, line):
        return self._data[elementSymbol][line]
