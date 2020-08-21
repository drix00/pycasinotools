#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.Element

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Element data from CASINO v2.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
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
import math

# Third party modules.

# Local modules.
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools
import casinotools.fileformat.casino2.Composition as Composition
from casinotools.fileformat.casino2.line import NUMBER_ATOM_LINES
from casinotools.fileformat.casino2.Version import VERSION_2050100

# Globals and constants variables.
LINE_K = 'K'
LINE_L = 'LIII'
LINE_M = 'MV'

GENERATED = "Generated"
EMITTED = "Emitted"

TAG_ELEMENT_DATA = b"*ELEMENTDATA%%%"


class Element(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self, number_xray_layers=500):
        self.Z = 0
        self.Nom = ""
        self.Rho = 0.0
        self.A = 0.0
        self.J = 0.0
        self.K = 0.0
        self.ef = 0.0
        self.kf = 0.0
        self.ep = 0.0

        self.Int_PRZ = []
        self.Int_PRZ_ABS = []
        for _dummy in range(3):
            self.Int_PRZ.append(0.0)
            self.Int_PRZ_ABS.append(0.0)

        self.intensity_1_esr = []
        for _dummy in range(NUMBER_ATOM_LINES):
            self.intensity_1_esr.append(0.0)

        self.COUCHE_K = []
        self.COUCHE_LIII = []
        self.COUCHE_MV = []

        self.COUCHE_K_ABS = []
        self.COUCHE_LIII_ABS = []
        self.COUCHE_MV_ABS = []

        self.COUCHE_RADIAL_K = []
        self.COUCHE_RADIAL_LIII = []
        self.COUCHE_RADIAL_MV = []

        self.COUCHE_RADIAL_K_ABS = []
        self.COUCHE_RADIAL_LIII_ABS = []
        self.COUCHE_RADIAL_MV_ABS = []

        for _dummy in range(number_xray_layers):
            self.COUCHE_K.append(0.0)
            self.COUCHE_LIII.append(0.0)
            self.COUCHE_MV.append(0.0)

            self.COUCHE_K_ABS.append(0.0)
            self.COUCHE_LIII_ABS.append(0.0)
            self.COUCHE_MV_ABS.append(0.0)

            self.COUCHE_RADIAL_K.append(0.0)
            self.COUCHE_RADIAL_LIII.append(0.0)
            self.COUCHE_RADIAL_MV.append(0.0)

            self.COUCHE_RADIAL_K_ABS.append(0.0)
            self.COUCHE_RADIAL_LIII_ABS.append(0.0)
            self.COUCHE_RADIAL_MV_ABS.append(0.0)

        self._composition = None

    def read(self, file, number_xray_layers, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = TAG_ELEMENT_DATA
        self.find_tag(file, tag_id)

        self.Z = self.read_int(file)
        self.Nom = self.read_str_length(file, 3)
        self.Rho = self.read_double(file)
        self.A = self.read_double(file)
        self.J = self.read_double(file)
        self.K = self.read_double(file)
        self.ef = self.read_double(file)
        self.kf = self.read_double(file)
        self.ep = self.read_double(file)

        self._composition = Composition.Composition()
        self._composition.read(file)

        # This is the intensities as displayed in the casino program.
        self.Int_PRZ = []
        for dummy in range(3):
            value = self.read_float(file)
            self.Int_PRZ.append(value)

        self.Int_PRZ_ABS = []
        for dummy in range(3):
            value = self.read_float(file)
            self.Int_PRZ_ABS.append(value)

        if version >= VERSION_2050100:
            self.intensity_1_esr = []
            for _dummy in range(NUMBER_ATOM_LINES):
                value = self.read_double(file)
                self.intensity_1_esr.append(value)
        assert len(self.intensity_1_esr) == NUMBER_ATOM_LINES

        if number_xray_layers != 0.0:
            self.COUCHE_K = self.read_double_list(file, number_xray_layers)
            self.COUCHE_LIII = self.read_double_list(file, number_xray_layers)
            self.COUCHE_MV = self.read_double_list(file, number_xray_layers)

            self.COUCHE_K_ABS = self.read_double_list(file, number_xray_layers)
            self.COUCHE_LIII_ABS = self.read_double_list(file, number_xray_layers)
            self.COUCHE_MV_ABS = self.read_double_list(file, number_xray_layers)

            self.COUCHE_RADIAL_K = self.read_double_list(file, number_xray_layers)
            self.COUCHE_RADIAL_LIII = self.read_double_list(file, number_xray_layers)
            self.COUCHE_RADIAL_MV = self.read_double_list(file, number_xray_layers)

            self.COUCHE_RADIAL_K_ABS = self.read_double_list(file, number_xray_layers)
            self.COUCHE_RADIAL_LIII_ABS = self.read_double_list(file, number_xray_layers)
            self.COUCHE_RADIAL_MV_ABS = self.read_double_list(file, number_xray_layers)

    def write(self, file, number_xray_layers):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_ELEMENT_DATA
        self.add_tag_old(file, tag_id)

        self.write_int(file, self.Z)
        self.write_str_length(file, self.Nom, 3)
        self.write_double(file, self.Rho)
        self.write_double(file, self.A)
        self.write_double(file, self.J)
        self.write_double(file, self.K)
        self.write_double(file, self.ef)
        self.write_double(file, self.kf)
        self.write_double(file, self.ep)

        self._composition.write(file)

        # This is the intensities as displayed in the casino program.
        assert len(self.Int_PRZ) == 3
        for index in range(3):
            value = self.Int_PRZ[index]
            self.write_float(file, value)

        assert len(self.Int_PRZ_ABS) == 3
        for index in range(3):
            value = self.Int_PRZ_ABS[index]
            self.write_float(file, value)

        assert len(self.intensity_1_esr) == NUMBER_ATOM_LINES
        for line_index in range(NUMBER_ATOM_LINES):
            value = self.intensity_1_esr[line_index]
            self.write_double(file, value)

        if number_xray_layers != 0.0:
            self.write_double_list(file, self.COUCHE_K, number_xray_layers)
            self.write_double_list(file, self.COUCHE_LIII, number_xray_layers)
            self.write_double_list(file, self.COUCHE_MV, number_xray_layers)

            self.write_double_list(file, self.COUCHE_K_ABS, number_xray_layers)
            self.write_double_list(file, self.COUCHE_LIII_ABS, number_xray_layers)
            self.write_double_list(file, self.COUCHE_MV_ABS, number_xray_layers)

            self.write_double_list(file, self.COUCHE_RADIAL_K, number_xray_layers)
            self.write_double_list(file, self.COUCHE_RADIAL_LIII, number_xray_layers)
            self.write_double_list(file, self.COUCHE_RADIAL_MV, number_xray_layers)

            self.write_double_list(file, self.COUCHE_RADIAL_K_ABS, number_xray_layers)
            self.write_double_list(file, self.COUCHE_RADIAL_LIII_ABS, number_xray_layers)
            self.write_double_list(file, self.COUCHE_RADIAL_MV_ABS, number_xray_layers)

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

    def get_total_xray_intensities_1_esr(self):
        intensities = {}

        assert len(self.intensity_1_esr) == NUMBER_ATOM_LINES
        for line_index in range(NUMBER_ATOM_LINES):
            value = self.intensity_1_esr[line_index]
            if value > 0.0:
                intensities[line_index] = value

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

    def getDepthXrayDistributionLayer(self, z0_nm, z1_nm):
        """
        Return the depth x-ray distributions.

        :note: Remove last value, because it is the accumulator for all out of range values.

        """
        index0 = self._findDepthIndex(z0_nm)
        index1 = self._findDepthIndex(z1_nm)
        distributions = {}

        if max(self.COUCHE_K) > 0.0:
            distributions.setdefault(LINE_K, {})
            distributions[LINE_K][GENERATED] = self.COUCHE_K[index0:index1 + 1]
            distributions[LINE_K][EMITTED] = self.COUCHE_K_ABS[index0:index1 + 1]

        if max(self.COUCHE_LIII) > 0.0:
            distributions.setdefault(LINE_L, {})
            distributions[LINE_L][GENERATED] = self.COUCHE_LIII[index0:index1 + 1]
            distributions[LINE_L][EMITTED] = self.COUCHE_LIII_ABS[index0:index1 + 1]

        if max(self.COUCHE_MV) > 0.0:
            distributions.setdefault(LINE_M, {})
            distributions[LINE_M][GENERATED] = self.COUCHE_MV[index0:index1 + 1]
            distributions[LINE_M][EMITTED] = self.COUCHE_MV_ABS[index0:index1 + 1]

        return distributions

    def getDepthXrayDistributionLayerByLineType(self, z0_nm, z1_nm, line, line_type=EMITTED):
        """
        Return the depth x-ray distributions.

        :note: Remove last value, because it is the accumulator for all out of range values.

        """
        distributions = self._getDepthXrayDistributionLayer()

        return distributions[line][line_type]

    def getDepthXrayDistribution(self):
        """
        Return the depth x-ray distributions.

        :note: Remove last value, because it is the accumulator for all out of range values.

        """
        distributions = {}

        if max(self.COUCHE_K) > 0.0:
            distributions.setdefault(LINE_K, {})
            distributions[LINE_K][GENERATED] = self.COUCHE_K[:-1]
            distributions[LINE_K][EMITTED] = self.COUCHE_K_ABS[:-1]

        if max(self.COUCHE_LIII) > 0.0:
            distributions.setdefault(LINE_L, {})
            distributions[LINE_L][GENERATED] = self.COUCHE_LIII[:-1]
            distributions[LINE_L][EMITTED] = self.COUCHE_LIII_ABS[:-1]

        if max(self.COUCHE_MV) > 0.0:
            distributions.setdefault(LINE_M, {})
            distributions[LINE_M][GENERATED] = self.COUCHE_MV[:-1]
            distributions[LINE_M][EMITTED] = self.COUCHE_MV_ABS[:-1]

        return distributions

    def getDepthXrayDistributionByLineType(self, line, line_type=EMITTED):
        """
        Return the depth x-ray distributions.

        :note: Remove last value, because it is the accumulator for all out of range values.

        """
        distributions = self.getDepthXrayDistribution()

        return distributions[line][line_type]

    def setElement(self, symbol, weight_fraction=1.0, index=0):
        dummy_fnuatom, rho, z, a, ef, kf, ep = NUATOM(symbol)

        self.Z = z
        self.Nom = symbol
        self.Rho = rho
        self.A = a
        self.ef = ef
        self.kf = kf
        self.ep = ep

        self.J = _computeJ(self.Z)
        self.K = _computeK(self.Z)

        self._composition = Composition.Composition()
        self._composition.setIndex(index)
        self._composition.setWeightFraction(weight_fraction)

    def getComposition(self):
        return self._composition

    def getWeightFraction(self):
        return self._composition.FWt

    def setWeightFraction(self, weight_fraction):
        self._composition.setWeightFraction(weight_fraction)

    def getAtomicFraction(self):
        return self._composition.FAt

    def setAtomicFraction(self, atomic_fraction):
        self._composition.setAtomicFraction(atomic_fraction)

    def getMassDensity_g_cm3(self):
        return self.Rho

    def getRepetition(self):
        return self._composition.Rep

    def getAtomicWeight_g_mol(self):
        return self.A


def _computeJ(atomicNumber):
    import casinotools.fileformat.casino2.MeanIonizationPotential as MeanIonizationPotential
    mean_ionization_potential = MeanIonizationPotential.MeanIonizationPotential(MeanIonizationPotential.MODEL_JOY)
    return mean_ionization_potential.computeJ(atomicNumber)


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
        if symbol[1] == 'c':
            z = 89
            rho = 10.07
            a = 227.0278
            ef = 1.0
            kf = 7.0e7
            ep = 25
        elif symbol[1] == 'g':
            z = 47
            rho = 10.50
            a = 107.868
            ef = 5.5
            kf = 1.19e8
            ep = 15
        elif symbol[1] == 'l':
            z = 13
            rho = 2.70
            a = 26.98154
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'm':
            z = 95
            rho = 13.6
            a = 243
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'r':
            z = 18
            rho = 1.784
            a = 39.948
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 's':
            z = 33
            rho = 5.72
            a = 74.9216
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 't':
            z = 85
            rho = 0
            a = 210
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'u':
            z = 79
            rho = 19.3
            a = 196.9665
            ef = 5.5
            kf = 1.19e8
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'B':
        if symbol[1] == 'a':
            z = 56
            rho = 3.5
            a = 137.33
            ef = 1.0
            kf = 7.0e7
            ep = 7.2
        elif symbol[1] == '\0':
            z = 5
            rho = 2.34
            a = 10.81
            ef = 1.0
            kf = 7.0e7
            ep = 22.7
        elif symbol[1] == 'e':
            z = 4
            rho = 1.85
            a = 9.01218
            ef = 1.0
            kf = 7.0e7
            ep = 18.7
        elif symbol[1] == 'i':
            z = 83
            rho = 9.8
            a = 209.0
            ef = 1.0
            kf = 7.0e7
            ep = 14.2
        elif symbol[1] == 'k':
            z = 97
            rho = 0
            a = 247
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'r':
            z = 35
            rho = 3.12
            a = 79.904
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'C':
        if symbol[1] == 'a':
            z = 20
            rho = 1.56
            a = 40.08
            ef = 1.0
            kf = 7.0e7
            ep = 8.8

        elif symbol[1] == '\0':
            z = 6
            rho = 2.62
            a = 12.011
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'd':
            z = 48
            rho = 8.65
            a = 112.41
            ef = 1.0
            kf = 7.0e7
            ep = 19.2

        elif symbol[1] == 'e':
            z = 58
            rho = 6.78
            a = 140.12
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'f':
            z = 98
            rho = 0
            a = 251
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'l':
            z = 17
            rho = 8.96
            a = 35.453
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'm':
            z = 96
            rho = 13.511
            a = 247
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'o':
            z = 27
            rho = 8.9
            a = 58.9332
            ef = 1.0
            kf = 7.0e7
            ep = 20.9

        elif symbol[1] == 'r':
            z = 24
            rho = 7.19
            a = 51.996
            ef = 1.0
            kf = 7.0e7
            ep = 24.9

        elif symbol[1] == 's':
            z = 55
            rho = 1.87
            a = 132.9054
            ef = 1.0
            kf = 7.0e7
            ep = 2.9

        elif symbol[1] == 'u':
            z = 29
            rho = 8.96
            a = 63.546
            ef = 7.0
            kf = 1.35e8
            ep = 19.3

        else:
            fnuatom = 0
    elif symbol[0] == 'D':
        if symbol[1] == 'y':
            z = 66
            rho = 8.54
            a = 160.5
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'E':
        if symbol[1] == 'r':
            z = 68
            rho = 9.05
            a = 167.26
            ef = 1.0
            kf = 7.0e7
            ep = 14

        elif symbol[1] == 's':
            z = 99
            rho = 0
            a = 254
            ep = 15

        elif symbol[1] == 'u':
            z = 63
            rho = 5.26
            a = 151.96
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'F':
        if symbol[1] == 'e':
            z = 26
            rho = 7.86
            a = 55.847
            ef = 1.0
            kf = 7.0e7
            ep = 23

        elif symbol[1] == '\0':
            z = 9
            rho = 1.696
            a = 18.9994
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'm':
            z = 100
            rho = 0
            a = 257
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'r':
            z = 87
            rho = 0
            a = 223
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'G':
        if symbol[1] == 'a':
            z = 31
            rho = 5.91
            a = 69.72
            ef = 1.0
            kf = 7.0e7
            ep = 13.8

        elif symbol[1] == 'd':
            z = 64
            rho = 7.89
            a = 157.25
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'e':
            z = 32
            rho = 5.32
            a = 72.59
            ef = 1.0
            kf = 7.0e7
            ep = 16.2

        else:
            fnuatom = 0
    elif symbol[0] == 'H':
        if symbol[1] == 'e':
            z = 2
            rho = 0.1787
            a = 4.00260
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'f':
            z = 72
            rho = 13.1
            a = 178.49
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'g':
            z = 80
            rho = 13.53
            a = 200.59
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == '\0':
            z = 1
            rho = 0.0899
            a = 1.0079
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'o':
            z = 67
            rho = 10.07
            a = 164.9
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'I':
        if symbol[1] == '\0':
            z = 53
            rho = 4.92
            a = 126.9045
            ef = 1.0
            kf = 7.0e7
            ep = 11.4

        elif symbol[1] == 'n':
            z = 49
            rho = 7.31
            a = 114.82
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'r':
            z = 77
            rho = 22.5
            a = 192.22
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'K':
        if symbol[1] == '\0':
            z = 19
            rho = 0.86
            a = 39.0983
            ef = 1.0
            kf = 7.0e7
            ep = 3.7

        elif symbol[1] == 'r':
            z = 36
            rho = 3.74
            a = 83.8
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'L':
        if symbol[1] == 'a':
            z = 57
            rho = 6.7
            a = 138.9055
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'i':
            z = 3
            rho = 0.53
            a = 6.941
            ef = 4.7
            kf = 1.1e8
            ep = 7.1

        elif symbol[1] == 'r':
            z = 103
            rho = 0
            a = 257
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'u':
            z = 71
            rho = 9.84
            a = 174.967
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'M':
        if symbol[1] == 'd':
            z = 101
            rho = 0
            a = 257
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'g':
            z = 12
            rho = 1.74
            a = 24.305
            ef = 1.0
            kf = 7.0e7
            ep = 10.3

        elif symbol[1] == 'n':
            z = 25
            rho = 7.43
            a = 54.9380
            ef = 1.0
            kf = 7.0e7
            ep = 21.6

        elif symbol[1] == 'o':
            z = 42
            rho = 10.2
            a = 95.94
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'N':
        if symbol[1] == 'a':
            z = 11
            rho = 0.97
            a = 22.98977
            ef = 3.1
            kf = 9.0e7
            ep = 5.7

        elif symbol[1] == 'b':
            z = 41
            rho = 8.56
            a = 92.9064
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'd':
            z = 60
            rho = 7
            a = 144.24
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'e':
            z = 10
            rho = 0.901
            a = 20.179
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'i':
            z = 28
            rho = 8.90
            a = 58.7
            ef = 1.0
            kf = 7.0e7
            ep = 20.7

        elif symbol[1] == '\0':
            z = 7
            rho = 1.251
            a = 14.0067
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'o':
            z = 102
            rho = 0
            a = 254
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'p':
            z = 93
            rho = 20.4
            a = 237.0482
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'O':
        if symbol[1] == '\0':
            z = 8
            rho = 1.429
            a = 15.9994
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 's':
            z = 76
            rho = 22.4
            a = 190.2
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'P':
        if symbol[1] == 'a':
            z = 91
            rho = 15.4
            a = 231.0359
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'b':
            z = 82
            rho = 11.4
            a = 207.2
            ef = 1.0
            kf = 7.0e7
            ep = 13

        elif symbol[1] == 'd':
            z = 46
            rho = 12
            a = 106.4
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'm':
            z = 61
            rho = 6.475
            a = 145
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'o':
            z = 84
            rho = 9.4
            a = 210
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == '\0':
            z = 15
            rho = 1.827
            a = 30.97376
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'r':
            z = 59
            rho = 6.77
            a = 140.9077
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 't':
            z = 78
            rho = 21.4
            a = 195.09
            ef = 1.0
            kf = 7.0e7
            ep = 35

        elif symbol[1] == 'u':
            z = 94
            rho = 19.8
            a = 244
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'R':
        if symbol[1] == 'a':
            z = 88
            rho = 5
            a = 226.0254
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'b':
            z = 37
            rho = 1.53
            a = 85.4678
            ef = 1.0
            kf = 7.0e7
            ep = 3.41

        elif symbol[1] == 'e':
            z = 75
            rho = 21
            a = 186.207
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'h':
            z = 45
            rho = 12.4
            a = 102.9055
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'n':
            z = 86
            rho = 9.91
            a = 222
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'u':
            z = 44
            rho = 12.2
            a = 101.07
            ef = 1.0
            kf = 7.0e7
            ep = 15

        else:
            fnuatom = 0
    elif symbol[0] == 'S':
        if symbol[1] == 'b':
            z = 51
            rho = 6.68
            a = 121.75
            ef = 1.0
            kf = 7.0e7
            ep = 15.2

        elif symbol[1] == 'c':
            z = 21
            rho = 3
            a = 44.9559
            ef = 1.0
            kf = 7.0e7
            ep = 14

        elif symbol[1] == 'e':
            z = 34
            rho = 4.8
            a = 78.96
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'i':
            z = 14
            rho = 2.33
            a = 28.0855
            ef = .555
            kf = 4.0e7
            ep = 16.7

        elif symbol[1] == 'm':
            z = 62
            rho = 7.54
            a = 150.4
            ef = 1.0
            kf = 7.0e7
            ep = 15

        elif symbol[1] == 'n':
            z = 50

            rho = 7.3
            a = 118.69
            ef = 1.0
            kf = 7.0e7
            ep = 13.4

        elif symbol[1] == 'r':
            z = 38
            rho = 2.6
            a = 87.62
            ef = 1.0
            kf = 7.0e7
            ep = 8.
        elif symbol[1] == '\0':
            z = 16
            rho = 2.07
            a = 32.06
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'T':
        if symbol[1] == 'a':
            z = 73
            rho = 16.6
            a = 180.9479
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'b':
            z = 65
            rho = 8.27
            a = 158.9254
            ef = 1.0
            kf = 7.0e7
            ep = 13.3
        elif symbol[1] == 'c':
            z = 43
            rho = 11.5
            a = 98.91
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'e':
            z = 52
            rho = 6.24
            a = 127.6
            ef = 1.0
            kf = 7.0e7
            ep = 17
        elif symbol[1] == 'h':
            z = 90
            rho = 11.7
            a = 232.0381
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'i':
            z = 22
            rho = 4.5
            a = 47.9
            ef = 1.0
            kf = 7.0e7
            ep = 17.9
        elif symbol[1] == 'l':
            z = 81
            rho = 11.85
            a = 204.37
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == 'm':
            z = 69
            rho = 9.33
            a = 168.9342
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'U':
        if symbol[1] == '\0':
            z = 92
            rho = 18.9
            a = 238.029
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'V':
        if symbol[1] == 'a':
            z = 0
            rho = 1
            a = 1
            ef = 0
            kf = 0
            ep = 0
        elif symbol[1] == '\0':
            z = 23
            rho = 5.8
            a = 50.9415
            ef = 1.0
            kf = 7.0e7
            ep = 21.8
        else:
            fnuatom = 0
    elif symbol[0] == 'W':
        if symbol[1] == '\0':
            z = 74
            rho = 19.3
            a = 183.85
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'X':
        if symbol[1] == 'e':
            z = 54
            rho = 5.89
            a = 131.3
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    elif symbol[0] == 'Y':
        if symbol[1] == 'b':
            z = 70
            rho = 6.98
            a = 173.04
            ef = 1.0
            kf = 7.0e7
            ep = 15
        elif symbol[1] == '\0':
            z = 39
            rho = 4.5
            a = 88.9059
            ef = 1.0
            kf = 7.0e7
            ep = 12.5
        else:
            fnuatom = 0
    elif symbol[0] == 'Z':
        if symbol[1] == 'n':
            z = 30
            rho = 7.14
            a = 65.38
            ef = 1.0
            kf = 7.0e7
            ep = 17.2
        elif symbol[1] == 'r':
            z = 40
            rho = 6.49
            a = 91.22
            ef = 1.0
            kf = 7.0e7
            ep = 15
        else:
            fnuatom = 0
    else:
        fnuatom = 0

    return fnuatom, rho, z, a, ef, kf, ep
