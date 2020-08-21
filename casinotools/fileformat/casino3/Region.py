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
import decimal

# Third party modules.

# Local modules.
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools
import casinotools.fileformat.casino3.Element as Element

# Globals and constants variables.
decimal.getcontext().prec = 28
EPSILON = 1.0e-4

NB_PAR_MAX = 4

TAG_REGIONS_DATA = b"*regionSDATA%%%"


class Region(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        pass

    def read(self, file):
        self._file = file
        self._startPosition = file.tell()
        self._filePathname = file.name
        self._fileDescriptor = file.fileno()
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", self._startPosition)

        self._version = self.read_int(file)

        tagID = TAG_REGIONS_DATA
        self.find_tag(file, tagID)

        if self._version > 30104072:
            self._carrierDiffusionLength = self.read_double(file)

        if self._version < 30105005:
            self.IDed = self.read_int(file)

        self._numberElements = self.read_int(file)
        self.Rho = self.read_double(file)

        if self._version < 30105001:
            self.Zmoy = self.read_double(file)

        self._workFunction = self.read_double(file)
        self._averagePlasmonEnergy = self.read_double(file)
        self.ID = self.read_int(file)
        self.Substrate = self.read_int(file)
        self.User_Density = self.read_int(file)
        self.User_Composition = self.read_int(file)
        self._checked = self.read_int(file)

        if self._version < 30105022:
            self._energyIntensity = self.read_double(file)

        self.Name = self.read_str(file)

        self._numberSampleObjects = self.read_int(file)

        self._sampleObjectIDs = {}
        for dummy in range(self._numberSampleObjects):
            id = self.read_int(file)
            insideOrOutside = self.read_int(file)

            self._sampleObjectIDs[id] = insideOrOutside

        self._mollerInit = self.read_double(file)
        self._triangleColor_X = self.read_double(file)
        self._triangleColor_Y = self.read_double(file)
        self._triangleColor_Z = self.read_double(file)

        self._elements = []
        for dummy in range(self._numberElements):
            element = Element.Element()
            element.read(file)
            self._elements.append(element)

        self._chemicalName = self.read_str(file)

    def _modify(self, file):
        assert file.mode == 'r+b'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write", file.tell())

        tagID = TAG_REGIONS_DATA
        if self.find_tag(file, tagID):
            self.write_int(file, self._version)

            self.write_double(file, self._carrierDiffusionLength)

            self.write_int(file, self._numberElements)
            self.write_double(file, self.Rho)

            self.write_double(file, self._workFunction)
            self.write_double(file, self._averagePlasmonEnergy)
            self.write_int(file, self.ID)
            self.write_int(file, self.Substrate)
            self.write_int(file, self.User_Density)
            self.write_int(file, self.User_Composition)
            self.write_int(file, self._checked)

            self.write_str(file, self.Name)

            self.write_int(file, self._numberSampleObjects)

            for objectID in sorted(self._sampleObjectIDs.keys()):
                self.write_int(file, objectID)
                self.write_int(file, self._sampleObjectIDs[objectID])

            self.write_double(file, self._mollerInit)
            self.write_double(file, self._triangleColor_X)
            self.write_double(file, self._triangleColor_Y)
            self.write_double(file, self._triangleColor_Z)

            for element in self._elements:
                element._modify(file)

            self.write_str(file, self._chemicalName)

    def write(self, file):
        raise NotImplementedError

    def modifyName(self, name):
        self.Name = name
        if not self._file.closed:
            currentPosition = self._file.tell()
            self._file.close()
        else:
            currentPosition = 0

        self._file = open(self._filePathname, 'r+b')

        self._file.seek(self._startPosition)

        self._modify(self._file)

        self._file.close()
        self._file = open(self._filePathname, 'rb')
        self._file.seek(currentPosition)

    def getNumberElements(self):
        assert len(self._elements) == self._numberElements
        return self._numberElements

    def removeAllElements(self):
        self._numberElements = 0
        self._elements = []
        assert len(self._elements) == self._numberElements

    def addElement(self, symbol, weightFraction=1.0, numberXRayLayers=500):
        self._numberElements += 1
        element = Element.Element(numberXRayLayers)
        element.setElement(symbol, weightFraction)
        self._elements.append(element)
        assert len(self._elements) == self._numberElements

    def getElement(self, index):
        return self._elements[index]

    def getElementBySymbol(self, symbol):
        for element in self._elements:
            if element.getSymbol() == symbol:
                return element

    def update(self):
        self._numberElements = self._computeNumberElements()
        self.Rho = self._computeMeanMassDensity_g_cm3()
        self.Zmoy = self._computeMeanAtomicNumber()
        self.Name = self._generateName()

        self._computeAtomicFractionElements()
        self._checkWeightFraction()
        self._checkAtomicFraction()

    def _computeNumberElements(self):
        return len(self._elements)

    def _computeMeanMassDensity_g_cm3(self):
        inverseTotal = 0.0
        for element in self._elements:
            weightFraction = element.getWeightFraction()
            massDensity_g_cm3 = element.getMassDensity_g_cm3()

            inverseTotal += weightFraction / massDensity_g_cm3

        meanMassDensity = 1.0 / inverseTotal
        return meanMassDensity

    def _computeMeanAtomicNumber(self):
        Total_Z = 0.0
        Total_Elements = 0.0

        for element in self._elements:
            repetition = element.getRepetition()
            Total_Elements += repetition
            Total_Z += element.getAtomicNumber() * repetition

        meanAtomicNumber = Total_Z / Total_Elements
        return meanAtomicNumber

    def _generateName(self):
        name = ""
        for element in self._elements:
            name += element.getSymbol().strip()

        return name

    def _computeAtomicFractionElements(self):
        total = 0.0
        for element in self._elements:
            weightFraction = element.getWeightFraction()
            atomicWeight = element.getAtomicWeight_g_mol()

            total += weightFraction / atomicWeight

        for element in self._elements:
            weightFraction = element.getWeightFraction()
            atomicWeight = element.getAtomicWeight_g_mol()

            atomicFraction = (weightFraction / atomicWeight) / total
            element.setAtomicFraction(atomicFraction)

    def _checkWeightFraction(self):
        weightFractions = [element.getWeightFraction() for element in self._elements]
        total = sum(weightFractions)
        assert abs(total - 1.0) < EPSILON

        for element in self._elements:
            newWeightFraction = decimal.Decimal(str(element.getWeightFraction())) / decimal.Decimal(str(total))
            element.setWeightFraction(float(newWeightFraction))

        weightFractions = [element.getWeightFraction() for element in self._elements]
        total = sum(weightFractions)
        assert abs(total - 1.0) < EPSILON * EPSILON

    def _checkAtomicFraction(self):
        atomicFractions = [element.getAtomicFraction() for element in self._elements]
        total = sum(atomicFractions)
        assert abs(total - 1.0) < EPSILON

        for element in self._elements:
            newAtomicFraction = decimal.Decimal(str(element.getAtomicFraction())) / decimal.Decimal(str(total))
            element.setAtomicFraction(float(newAtomicFraction))

        atomicFractions = [element.getAtomicFraction() for element in self._elements]
        total = sum(atomicFractions)
        assert abs(total - 1.0) < EPSILON * EPSILON

    def getMeanMassDensity_g_cm3(self):
        return self.Rho

    def getMeanAtomicNumber(self):
        return self.Zmoy

    def getName(self):
        return self.Name

    def getComposition(self):
        return self._chemicalName

    def getId(self):
        return self.ID

    def export(self, export_file):
        # todo: implement the export method.
        logging.error("implement the export method.")
