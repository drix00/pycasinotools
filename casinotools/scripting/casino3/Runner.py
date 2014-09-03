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

# Globals and constants variables.

class Runner(object):
    def __init__(self):
        self._simulationFiles = []
        self._energies_keV = []
        self._numberTrajectoriesList = []
        self._beamRadiusList_nm = []
        self._focalPlaneZList_nm = []
        self._particleRadiusList = []
        self._filmThicknessList = []

    def setSimulationFiles(self, simulationFiles):
        self._simulationFiles = simulationFiles

    def setEnergies_keV(self, energies_keV):
        self._energies_keV = energies_keV

    def setNumberTrajectoriesList(self, numberTrajectoriesList):
        self._numberTrajectoriesList = numberTrajectoriesList

    def setBeamRadiusList_nm(self, beamRadiusList_nm):
        self._beamRadiusList_nm = beamRadiusList_nm

    def setFocalPlaneZList_nm(self, focalPlaneZList_nm):
        self._focalPlaneZList_nm = focalPlaneZList_nm

    def setParticleRadiusList_nm(self, particleRadiusList):
        self._particleRadiusList = particleRadiusList

    def setFilmThicknessList_nm(self, filmThicknessList):
        self._filmThicknessList = filmThicknessList
