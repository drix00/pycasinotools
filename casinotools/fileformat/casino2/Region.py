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
import casinotools.fileformat.casino2.Element as Element

# Globals and constants variables.
decimal.getcontext().prec = 28
EPSILON = 1.0e-4

NB_PAR_MAX = 4

TAG_REGIONS_DATA = b"*REGIONSDATA%%%"


class Region(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, numberXRayLayers):
        self._numberXRayLayers = numberXRayLayers

    def read(self, file):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = TAG_REGIONS_DATA
        self.findTag(file, tagID)

        self.ID = self.readInt(file)
        self.IDed = self.readInt(file)
        self.NbEl = self.readInt(file)
        self.Rho = self.readDouble(file)
        self.Zmoy = self.readDouble(file)

        self.Parametre = []
        for dummy in range(NB_PAR_MAX):
            value = self.readDouble(file)
            self.Parametre.append(value)

        self.Forme = self.readInt(file)
        self.Substrate = self.readInt(file)
        self.color = self.readLong(file)
        self.cindex = self.readInt(file)
        self.User_Density = self.readInt(file)
        self.User_Composition = self.readInt(file)

        self.Name = self.readStr(file)

        self._elements = []
        for dummy in range(self.NbEl):
            element = Element.Element()
            element.read(file, self._numberXRayLayers)
            self._elements.append(element)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tagID = TAG_REGIONS_DATA
        self.addTagOld(file, tagID)
        self.writeInt(file, self.ID)
        self.writeInt(file, self.IDed)
        self.writeInt(file, self.NbEl)
        self.writeDouble(file, self.Rho)
        self.writeDouble(file, self.Zmoy)

        assert len(self.Parametre) == NB_PAR_MAX
        for index in range(NB_PAR_MAX):
            value = self.Parametre[index]
            self.writeDouble(file, value)

        self.writeInt(file, self.Forme)
        self.writeInt(file, self.Substrate)
        self.writeLong(file, self.color)
        self.writeInt(file, self.cindex)
        self.writeInt(file, self.User_Density)
        self.writeInt(file, self.User_Composition)

        self.writeStr(file, self.Name)

        assert len(self._elements) == self.NbEl
        for index in range(self.NbEl):
            element = self._elements[index]
            element.write(file, self._numberXRayLayers)

    def getNumberElements(self):
        assert len(self._elements) == self.NbEl
        return self.NbEl

    def removeAllElements(self):
        self.NbEl = 0
        self._elements = []
        assert len(self._elements) == self.NbEl

    def addElement(self, symbol, weightFraction=1.0, numberXRayLayers=500):
        self.NbEl += 1
        element = Element.Element(numberXRayLayers)
        element.setElement(symbol, weightFraction)
        self._elements.append(element)
        assert len(self._elements) == self.NbEl

    def getElement(self, index):
        return self._elements[index]

    def getElements(self):
        return self._elements

    def setElement(self, elementSymbol, weightFraction=1.0, numberXRayLayers=500, indexElement=0):
        element = Element.Element(numberXRayLayers)
        element.setElement(elementSymbol, weightFraction)
        self._elements[indexElement] = element
        assert len(self._elements) == self.NbEl
        self.update()

    def getElementBySymbol(self, symbol):
        for element in self._elements:
            if element.getSymbol() == symbol:
                return element

    def update(self):
        self.NbEl = self._computeNumberElements()
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

    def isUserMassDensity(self):
        return bool(self.User_Density)

    def getParameters(self):
        return self.Parametre

    def setParameters(self, parameters):
        self.Parametre = parameters

