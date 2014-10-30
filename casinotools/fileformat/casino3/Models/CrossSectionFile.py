#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os
import logging
import math

# Third party modules.
import numpy as np

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
from casinotools.utilities.path import create_path

# Globals and constants variables.
VERSION_30107002 = 30107002
VERSION_LASTEST = VERSION_30107002

def generateRawBinaryFiles(filepath, atomicNumber, energiesGrid_eV, totals_nm2,
                                                     polarAnglesGrid_deg, partialsList_nm2_sr):
    path = os.path.dirname(filepath)
    path = create_path(path)

    logging.info(filepath)

    file = open(filepath, 'wb')

    binaryWriter = FileReaderWriterTools.FileReaderWriterTools()

    for energy_eV, total_nm2 in zip(energiesGrid_eV, totals_nm2):
        binaryWriter.writeInt(file, VERSION_LASTEST)
        binaryWriter.writeDouble(file, atomicNumber)
        energy_keV = energy_eV / 1000.0
        binaryWriter.writeDouble(file, energy_keV)
        binaryWriter.writeDouble(file, total_nm2)

        size = len(polarAnglesGrid_deg)
        binaryWriter.writeLong(file, size)

        partials_nm2_sr = partialsList_nm2_sr[energy_eV]
        partialSinThetas_nm2_sr = []
        polarAngleGrid_rad = []
        for angle_deg, partial_nm2_sr in zip(polarAnglesGrid_deg, partials_nm2_sr):
            angle_rad = math.radians(angle_deg)
            polarAngleGrid_rad.append(angle_rad)
            partialSinThetas_nm2_sr.append(partial_nm2_sr * math.sin(angle_rad) * 2.0 * math.pi)

        ratioList = []
        computedTotal_nm2 = np.trapz(partialSinThetas_nm2_sr, polarAngleGrid_rad)
        for index in range(1, len(partialSinThetas_nm2_sr) + 1):
            x = polarAngleGrid_rad[:index]
            y = partialSinThetas_nm2_sr[:index]
            ratio = np.trapz(y, x) / computedTotal_nm2
            ratioList.append(ratio)

        for ratio, angle_rad in zip(ratioList, polarAngleGrid_rad):
            binaryWriter.writeDouble(file, ratio)
            binaryWriter.writeDouble(file, angle_rad)

    file.close()
