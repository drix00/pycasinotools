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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
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

        self._version = self.readInt(file)

        tagID = TAG_REGIONS_DATA
        self.findTag(file, tagID)

        if self._version > 30104072:
            self._carrierDiffusionLength = self.readDouble(file)

        if self._version < 30105005:
            self.IDed = self.readInt(file)

        self._numberElements = self.readInt(file)
        self.Rho = self.readDouble(file)

        if self._version < 30105001:
            self.Zmoy = self.readDouble(file)

        self._workFunction = self.readDouble(file)
        self._averagePlasmonEnergy = self.readDouble(file)
        self.ID = self.readInt(file)
        self.Substrate = self.readInt(file)
        self.User_Density = self.readInt(file)
        self.User_Composition = self.readInt(file)
        self._checked = self.readInt(file)

        if self._version < 30105022:
            self._energyIntensity = self.readDouble(file)

        self.Name = self.readStr(file)

        self._numberSampleObjects = self.readInt(file)

        self._sampleObjectIDs = {}
        for dummy in range(self._numberSampleObjects):
            id = self.readInt(file)
            insideOrOutside = self.readInt(file)

            self._sampleObjectIDs[id] = insideOrOutside

        self._mollerInit = self.readDouble(file)
        self._triangleColor_X = self.readDouble(file)
        self._triangleColor_Y = self.readDouble(file)
        self._triangleColor_Z = self.readDouble(file)

        self._elements = []
        for dummy in range(self._numberElements):
            element = Element.Element()
            element.read(file)
            self._elements.append(element)

        self._chemicalName = self.readStr(file)

    def _modify(self, file):
        assert file.mode == 'r+b'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "_write", file.tell())

        tagID = TAG_REGIONS_DATA
        if self.findTag(file, tagID):
            self.writeInt(file, self._version)

            self.writeDouble(file, self._carrierDiffusionLength)

            self.writeInt(file, self._numberElements)
            self.writeDouble(file, self.Rho)

            self.writeDouble(file, self._workFunction)
            self.writeDouble(file, self._averagePlasmonEnergy)
            self.writeInt(file, self.ID)
            self.writeInt(file, self.Substrate)
            self.writeInt(file, self.User_Density)
            self.writeInt(file, self.User_Composition)
            self.writeInt(file, self._checked)

            self.writeStr(file, self.Name)

            self.writeInt(file, self._numberSampleObjects)

            for objectID in sorted(self._sampleObjectIDs.keys()):
                self.writeInt(file, objectID)
                self.writeInt(file, self._sampleObjectIDs[objectID])

            self.writeDouble(file, self._mollerInit)
            self.writeDouble(file, self._triangleColor_X)
            self.writeDouble(file, self._triangleColor_Y)
            self.writeDouble(file, self._triangleColor_Z)

            for element in self._elements:
                element._modify(file)

            self.writeStr(file, self._chemicalName)

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

    def export(self, exportFile):
        # todo: implement the export method.
        logging.error("implement the export method.")
