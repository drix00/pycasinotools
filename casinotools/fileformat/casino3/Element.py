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
import math

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.
LINE_K = 'K'
LINE_L = 'LIII'
LINE_M = 'MV'

GENERATED = "Generated"
EMITTED = "Emitted"

TAG_ELEMENT_DATA = b"*ELEMENTDATA_XX"

class Element(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._version = None
        self._elementID = 0
        self._weightFraction = 1.0
        self._atomicFraction = 1.0
        self._sigmaTElastic = 0.0
        self._repetition = 1
        self.Z = 0
        self._virtualElementInteger = 0

        self.Nom = ""
        self.Rho = 0.0
        self.A = 0.0
        self.J = 0.0
        self.K_Gauvin = 0.0
        self.K_Monsel = 0.0
        self.ef = 0.0
        self.kf = 0.0
        self.ep = 0.0

        self.Int_PRZ = []
        self.Int_PRZ_ABS = []
        for dummy in range(3):
            self.Int_PRZ.append(0.0)
            self.Int_PRZ_ABS.append(0.0)

    def read(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = TAG_ELEMENT_DATA
        self.findTag(file, tagID)
        self._version = self.readInt(file)

        self._elementID = self.readInt(file)
        self._weightFraction = self.readDouble(file)
        self._atomicFraction = self.readDouble(file)
        self._sigmaTElastic = self.readDouble(file)
        self._repetition = self.readInt(file)
        self.Z = self.readDouble(file)
        self._virtualElementInteger = self.readInt(file)

        self.Nom = self.readStrLength(file, 3)
        self.Rho = self.readDouble(file)
        self.A = self.readDouble(file)
        self.J = self.readDouble(file)
        self.K_Gauvin = self.readDouble(file)
        self.K_Monsel = self.readDouble(file)
        self.ef = self.readDouble(file)
        self.kf = self.readDouble(file)
        self.ep = self.readDouble(file)

        # This is the intensities as displayed in the casino program.
        self.Int_PRZ = []
        for dummy in range(3):
            value = self.readDouble(file)
            self.Int_PRZ.append(value)

        self.Int_PRZ_ABS = []
        for dummy in range(3):
            value = self.readDouble(file)
            self.Int_PRZ_ABS.append(value)

    def write(self, file):
        raise NotImplementedError
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

    def _modify(self, file):
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tagID = TAG_ELEMENT_DATA
        self.findTag(file, tagID)

        self.writeInt(file, self._version)

        self.writeInt(file, self._elementID)
        self.writeDouble(file, self._weightFraction)
        self.writeDouble(file, self._atomicFraction)
        self.writeDouble(file, self._sigmaTElastic)
        self.writeInt(file, self._repetition)
        self.writeDouble(file, self.Z)
        self.writeInt(file, self._virtualElementInteger)

        self.writeStrLength(file, self.Nom, 3)
        self.writeDouble(file, self.Rho)
        self.writeDouble(file, self.A)
        self.writeDouble(file, self.J)
        self.writeDouble(file, self.K_Gauvin)
        self.writeDouble(file, self.K_Monsel)
        self.writeDouble(file, self.ef)
        self.writeDouble(file, self.kf)
        self.writeDouble(file, self.ep)

        # This is the intensities as displayed in the casino program.
        assert len(self.Int_PRZ) == 3
        for index in range(3):
            value = self.Int_PRZ[index]
            self.writeDouble(file, value)

        assert len(self.Int_PRZ_ABS) == 3
        for index in range(3):
            value = self.Int_PRZ_ABS[index]
            self.writeDouble(file, value)

    def getAtomicNumber(self):
        return self.Z

    def getSymbol(self):
        return self.Nom

    def getTotalXrayIntensities(self):
        intensities = {}

        if self.Int_PRZ[0] > 0.0:
            intensities.setdefault(LINE_K, {})
            intensities[LINE_K][GENERATED] = self.Int_PRZ[0]
            intensities[LINE_K][EMITTED] = self.Int_PRZ_ABS[0]

        if self.Int_PRZ[1] > 0.0:
            intensities.setdefault(LINE_L, {})
            intensities[LINE_L][GENERATED] = self.Int_PRZ[1]
            intensities[LINE_L][EMITTED] = self.Int_PRZ_ABS[1]

        if self.Int_PRZ[2] > 0.0:
            intensities.setdefault(LINE_M, {})
            intensities[LINE_M][GENERATED] = self.Int_PRZ[2]
            intensities[LINE_M][EMITTED] = self.Int_PRZ_ABS[2]

        return intensities

    def getTotalXrayIntensityByLineType(self, line, type=EMITTED):
        if LINE_K.startswith(line[0]):
            line = LINE_K
        elif LINE_L.startswith(line[0]):
            line = LINE_L
        elif LINE_M.startswith(line[0]):
            line = LINE_M

        intensities = self.getTotalXrayIntensities()
        return intensities[line][type]

    def getRadialXrayDistribution(self):
        """
        Return the radial x-ray distributions.

        :note: Remove last value, because it is the accumulator for all out of range values.

        """
        distributions = {}

        if max(self.COUCHE_RADIAL_K) > 0.0:
            distributions.setdefault(LINE_K, {})
            distributions[LINE_K][GENERATED] = self.COUCHE_RADIAL_K[:-1]
            distributions[LINE_K][EMITTED] = self.COUCHE_RADIAL_K_ABS[:-1]

        if max(self.COUCHE_RADIAL_LIII) > 0.0:
            distributions.setdefault(LINE_L, {})
            distributions[LINE_L][GENERATED] = self.COUCHE_RADIAL_LIII[:-1]
            distributions[LINE_L][EMITTED] = self.COUCHE_RADIAL_LIII_ABS[:-1]

        if max(self.COUCHE_RADIAL_MV) > 0.0:
            distributions.setdefault(LINE_M, {})
            distributions[LINE_M][GENERATED] = self.COUCHE_RADIAL_MV[:-1]
            distributions[LINE_M][EMITTED] = self.COUCHE_RADIAL_MV_ABS[:-1]

        return distributions

    def setElement(self, symbol, weightFraction=1.0, index=0):
        _, rho, z, a, ef, kf, ep = NUATOM(symbol)

        self.Z = z
        self.Nom = symbol
        self.Rho = rho
        self.A = a
        self.ef = ef
        self.kf = kf
        self.ep = ep

        self.J = _computeJ(self.Z)
        self.K = _computeK(self.Z)

    def getComposition(self):
        return self._composition

    def getWeightFraction(self):
        return self._composition.FWt

    def setWeightFraction(self, weightFraction):
        self._composition.setWeightFraction(weightFraction)

    def getAtomicFraction(self):
        return self._composition.FAt

    def setAtomicFraction(self, atomicFraction):
        self._composition.setAtomicFraction(atomicFraction)
        self._composition.FAt = atomicFraction

    def getMassDensity_g_cm3(self):
        return self.Rho

    def getRepetition(self):
        return self._composition.Rep

    def getAtomicWeight_g_mol(self):
        return self.A

def _computeJ(atomicNumber):
    import casinotools.fileformat.casino2.MeanIonizationPotential as MeanIonizationPotential
    meanIonizationPotential = MeanIonizationPotential.MeanIonizationPotential(MeanIonizationPotential.MODEL_JOY)
    return meanIonizationPotential.computeJ(atomicNumber)

def _computeK(atomicNumber):
    k = 0.734 * math.pow(atomicNumber, 0.037)
    return k

def NUATOM(symbol):
    """
    Transcription du symbole atomique.
    """
    rho = 0.0
    z = 0
    a = 0.0
    ef = 0.0
    kf = 0.0
    ep = 0.0

    fnuatom = 1

    if len(symbol) == 1:
        symbol += '\0'
    assert len(symbol) == 2

    if symbol[0] == 'A':
        if symbol[1] == 'c' : z = 89;rho = 10.07;a = 227.0278;ef = 1.0;kf = 7.0e7;ep = 25;
        elif symbol[1] == 'g' :    z = 47; rho = 10.50; a = 107.868; ef = 5.5; kf = 1.19e8; ep = 15;
        elif symbol[1] == 'l' :    z = 13; rho = 2.70; a = 26.98154; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'm' :    z = 95; rho = 13.6; a = 243; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'r' :    z = 18; rho = 1.784; a = 39.948; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 's' :    z = 33; rho = 5.72; a = 74.9216; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 't' :    z = 85; rho = 0; a = 210; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'u' :    z = 79; rho = 19.3; a = 196.9665; ef = 5.5; kf = 1.19e8; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'B' :
        if symbol[1] == 'a' :    z = 56; rho = 3.5; a = 137.33; ef = 1.0; kf = 7.0e7; ep = 7.2;
        elif symbol[1] == '\0' :    z = 5; rho = 2.34; a = 10.81; ef = 1.0; kf = 7.0e7; ep = 22.7;
        elif symbol[1] == 'e' :    z = 4; rho = 1.85; a = 9.01218; ef = 1.0; kf = 7.0e7; ep = 18.7;
        elif symbol[1] == 'i' :    z = 83; rho = 9.8; a = 209.0; ef = 1.0; kf = 7.0e7; ep = 14.2;
        elif symbol[1] == 'k' :    z = 97; rho = 0; a = 247; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'r' :    z = 35; rho = 3.12; a = 79.904; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'C' :
        if symbol[1] == 'a' :    z = 20; rho = 1.56; a = 40.08; ef = 1.0; kf = 7.0e7; ep = 8.8;
        elif symbol[1] == '\0' :    z = 6; rho = 2.62; a = 12.011; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'd' :    z = 48; rho = 8.65; a = 112.41; ef = 1.0; kf = 7.0e7; ep = 19.2;
        elif symbol[1] == 'e' :    z = 58; rho = 6.78; a = 140.12; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'f' :    z = 98; rho = 0; a = 251; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'l' :    z = 17; rho = 8.96; a = 35.453; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'm' :    z = 96; rho = 13.511; a = 247; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'o' :    z = 27; rho = 8.9; a = 58.9332; ef = 1.0; kf = 7.0e7; ep = 20.9;
        elif symbol[1] == 'r' :    z = 24; rho = 7.19; a = 51.996; ef = 1.0; kf = 7.0e7; ep = 24.9;
        elif symbol[1] == 's' :    z = 55; rho = 1.87; a = 132.9054; ef = 1.0; kf = 7.0e7; ep = 2.9;
        elif symbol[1] == 'u' :    z = 29; rho = 8.96; a = 63.546; ef = 7.0; kf = 1.35e8; ep = 19.3;
        else: fnuatom = 0
    elif symbol[0] == 'D' :
        if symbol[1] == 'y' :    z = 66; rho = 8.54; a = 160.5; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'E' :
        if symbol[1] == 'r' :    z = 68; rho = 9.05; a = 167.26; ef = 1.0; kf = 7.0e7; ep = 14;
        elif symbol[1] == 's' :    z = 99; rho = 0; a = 254; ep = 15;
        elif symbol[1] == 'u' :    z = 63; rho = 5.26; a = 151.96; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'F' :
        if symbol[1] == 'e' :    z = 26; rho = 7.86; a = 55.847; ef = 1.0; kf = 7.0e7; ep = 23;
        elif symbol[1] == '\0' :    z = 9; rho = 1.696; a = 18.9994; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'm' :    z = 100; rho = 0; a = 257; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'r' :    z = 87; rho = 0; a = 223; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'G' :
        if symbol[1] == 'a' :    z = 31; rho = 5.91; a = 69.72; ef = 1.0; kf = 7.0e7; ep = 13.8;
        elif symbol[1] == 'd' :    z = 64; rho = 7.89; a = 157.25; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'e' :    z = 32; rho = 5.32; a = 72.59; ef = 1.0; kf = 7.0e7; ep = 16.2;
        else: fnuatom = 0
    elif symbol[0] == 'H' :
        if symbol[1] == 'e' :    z = 2; rho = 0.1787; a = 4.00260; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'f' :    z = 72; rho = 13.1; a = 178.49; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'g' :    z = 80; rho = 13.53; a = 200.59; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == '\0' :    z = 1; rho = 0.0899; a = 1.0079; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'o' :    z = 67; rho = 10.07; a = 164.9; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'I' :
        if symbol[1] == '\0' :    z = 53; rho = 4.92; a = 126.9045; ef = 1.0; kf = 7.0e7; ep = 11.4;
        elif symbol[1] == 'n' :    z = 49; rho = 7.31; a = 114.82; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'r' :    z = 77; rho = 22.5; a = 192.22; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'K' :
        if symbol[1] == '\0' :    z = 19; rho = 0.86; a = 39.0983; ef = 1.0; kf = 7.0e7; ep = 3.7;
        elif symbol[1] == 'r' :    z = 36; rho = 3.74; a = 83.8; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'L' :
        if symbol[1] == 'a' :    z = 57; rho = 6.7; a = 138.9055; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'i' :    z = 3; rho = 0.53; a = 6.941; ef = 4.7; kf = 1.1e8; ep = 7.1;
        elif symbol[1] == 'r' :    z = 103; rho = 0; a = 257; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'u' :    z = 71; rho = 9.84; a = 174.967; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'M' :
        if symbol[1] == 'd' :    z = 101; rho = 0; a = 257; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'g' :    z = 12; rho = 1.74; a = 24.305; ef = 1.0; kf = 7.0e7; ep = 10.3;
        elif symbol[1] == 'n' :    z = 25; rho = 7.43; a = 54.9380; ef = 1.0; kf = 7.0e7; ep = 21.6;
        elif symbol[1] == 'o' :    z = 42; rho = 10.2; a = 95.94; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'N' :
        if symbol[1] == 'a' :    z = 11; rho = 0.97; a = 22.98977; ef = 3.1; kf = 9.0e7; ep = 5.7;
        elif symbol[1] == 'b' :    z = 41; rho = 8.56; a = 92.9064; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'd' :    z = 60; rho = 7; a = 144.24; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'e' :    z = 10; rho = 0.901; a = 20.179; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'i' :    z = 28; rho = 8.90; a = 58.7; ef = 1.0; kf = 7.0e7; ep = 20.7;
        elif symbol[1] == '\0' :    z = 7; rho = 1.251; a = 14.0067; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'o' :    z = 102; rho = 0; a = 254; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'p' :    z = 93; rho = 20.4; a = 237.0482; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'O' :
        if symbol[1] == '\0' :    z = 8; rho = 1.429; a = 15.9994; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 's' :    z = 76; rho = 22.4; a = 190.2; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'P' :
        if symbol[1] == 'a' :    z = 91; rho = 15.4; a = 231.0359; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'b' :    z = 82; rho = 11.4; a = 207.2; ef = 1.0; kf = 7.0e7; ep = 13;
        elif symbol[1] == 'd' :    z = 46; rho = 12; a = 106.4; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'm' :    z = 61; rho = 6.475; a = 145; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'o' :    z = 84; rho = 9.4; a = 210; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == '\0' :    z = 15; rho = 1.827; a = 30.97376; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'r' :    z = 59; rho = 6.77; a = 140.9077; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 't' :    z = 78; rho = 21.4; a = 195.09; ef = 1.0; kf = 7.0e7; ep = 35;
        elif symbol[1] == 'u' :    z = 94; rho = 19.8; a = 244; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'R' :
        if symbol[1] == 'a' :    z = 88; rho = 5; a = 226.0254; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'b' :    z = 37; rho = 1.53; a = 85.4678; ef = 1.0; kf = 7.0e7; ep = 3.41;
        elif symbol[1] == 'e' :    z = 75; rho = 21; a = 186.207; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'h' :    z = 45; rho = 12.4; a = 102.9055; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'n' :    z = 86; rho = 9.91; a = 222; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'u' :    z = 44; rho = 12.2; a = 101.07; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'S' :
        if symbol[1] == 'b' :    z = 51; rho = 6.68; a = 121.75; ef = 1.0; kf = 7.0e7; ep = 15.2;
        elif symbol[1] == 'c' :    z = 21; rho = 3; a = 44.9559; ef = 1.0; kf = 7.0e7; ep = 14;
        elif symbol[1] == 'e' :    z = 34; rho = 4.8; a = 78.96; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'i' :    z = 14; rho = 2.33; a = 28.0855; ef = .555; kf = 4.0e7; ep = 16.7;
        elif symbol[1] == 'm' :    z = 62; rho = 7.54; a = 150.4; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'n' :    z = 50; rho = 7.3; a = 118.69; ef = 1.0; kf = 7.0e7; ep = 13.4;
        elif symbol[1] == 'r' :    z = 38; rho = 2.6; a = 87.62; ef = 1.0; kf = 7.0e7; ep = 8.;
        elif symbol[1] == '\0' :    z = 16; rho = 2.07; a = 32.06; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'T' :
        if symbol[1] == 'a' :    z = 73; rho = 16.6; a = 180.9479; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'b' :    z = 65; rho = 8.27; a = 158.9254; ef = 1.0; kf = 7.0e7; ep = 13.3;
        elif symbol[1] == 'c' :    z = 43; rho = 11.5; a = 98.91; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'e' :    z = 52; rho = 6.24; a = 127.6; ef = 1.0; kf = 7.0e7; ep = 17;
        elif symbol[1] == 'h' :    z = 90; rho = 11.7; a = 232.0381; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'i' :    z = 22; rho = 4.5; a = 47.9; ef = 1.0; kf = 7.0e7; ep = 17.9;
        elif symbol[1] == 'l' :    z = 81; rho = 11.85; a = 204.37; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == 'm' :    z = 69; rho = 9.33; a = 168.9342; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'U' :
        if symbol[1] == '\0' :    z = 92; rho = 18.9; a = 238.029; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'V' :
        if symbol[1] == 'a':    z = 0; rho = 1; a = 1; ef = 0; kf = 0; ep = 0;
        elif symbol[1] == '\0' :    z = 23; rho = 5.8; a = 50.9415; ef = 1.0; kf = 7.0e7; ep = 21.8;
        else: fnuatom = 0
    elif symbol[0] == 'W' :
        if symbol[1] == '\0' :    z = 74; rho = 19.3; a = 183.85; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'X' :
        if symbol[1] == 'e' :    z = 54; rho = 5.89; a = 131.3; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    elif symbol[0] == 'Y' :
        if symbol[1] == 'b' :    z = 70; rho = 6.98; a = 173.04; ef = 1.0; kf = 7.0e7; ep = 15;
        elif symbol[1] == '\0' :    z = 39; rho = 4.5; a = 88.9059; ef = 1.0; kf = 7.0e7; ep = 12.5;
        else: fnuatom = 0
    elif symbol[0] == 'Z' :
        if symbol[1] == 'n' :    z = 30; rho = 7.14; a = 65.38; ef = 1.0; kf = 7.0e7; ep = 17.2;
        elif symbol[1] == 'r' :    z = 40; rho = 6.49; a = 91.22; ef = 1.0; kf = 7.0e7; ep = 15;
        else: fnuatom = 0
    else:
        fnuatom = 0;

    return fnuatom, rho, z, a, ef, kf, ep
