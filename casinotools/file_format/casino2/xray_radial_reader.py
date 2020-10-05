#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.xray_radial_reader
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

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.casino2.xray_radial import XrayRadial, DISTANCE_nm, INTENSITY_ABSORBED

# Globals and constants variables.
K = 'K'
L = 'LIII'
M = 'MV'
HEADER_ELEMENT_LINE = "Radial XRay Distribution"
HEADER_ELEMENT = "Radial Distribution of"
HEADER_ALL = "XRay Radial of"

class XrayRadialReader:
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
        return line.startswith(DISTANCE_nm[:-5])

    def _extractDataLabelLineDataElementLine(self, line):
        items = line.split('\t')

        self._labels = []
        for item in items:
            self._labels.append(item.strip())

    def _extractDataLabelLineDataElement(self, line):
        items = line.split('\t')

        self._labels = []
        if items[0] == "Distance(nm)":
            self._labels.append(DISTANCE_nm)

        for item in items[1:]:
            label, xrayline = item.split(':')
            if xrayline.strip().endswith('ABS'):
                label = INTENSITY_ABSORBED
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
            self._data[symbol].setdefault(xrayLine, XrayRadial())
            xrayRadialData = self._data[symbol][xrayLine]
            xrayRadialData.set_line(xrayLine)
            xrayRadialData.set_element_symbol(symbol)
            xrayRadialData.set_labels(self.getDataLabels())
            try:
                value = float(item)
            except ValueError:
                value = 0.0

            xrayRadialData.add_data(label, value)

    def getDataLabels(self):
        return self._labels

    def getData(self, elementSymbol, line):
        return self._data[elementSymbol][line]
