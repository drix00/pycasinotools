#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2914 $"
__svnDate__ = "$Date: 2013-09-16 10:55:22 -0400 (Mon, 16 Sep 2013) $"
__svnId__ = "$Id: AnalyzeTransmittedElectrons.py 2914 2013-09-16 14:55:22Z hdemers $"

# Standard library modules.
import math

# Third party modules.
from scipy.stats import histogram2

# Local modules.
from casinotools.analysis.casino3 import statistic

# Globals and constants variables.
class Result(object):
    def __init__(self):
        self._simulations = []

    def setSimulations(self, simulations):
        self._simulations = simulations

    def getNumberSimulations(self):
        return len(self._simulations)

    def getDistancesFromFirstOne(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()
        positions = []
        for scanPointResults in scanPointsResults:
            positions.append(scanPointResults.getPosition())

        distances = []
        firstPosition = positions[0]
        for position in positions:
            distance = self._computeDistanceBetweenTwoPositions(firstPosition, position)
            distances.append(distance)

        return distances

    def getDistancesFromOrigine(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()
        positions = []
        for scanPointResults in scanPointsResults:
            positions.append(scanPointResults.getPosition())

        distances = []
        origine = (0.0, 0.0, 0.0)
        for position in positions:
            distance = self._computeDistanceBetweenTwoPositions(origine, position)
            angle = math.fabs(math.atan2(position[1], position[0]))
            if 0.0 <=    angle < math.pi/2.0:
                distance *= -1.0
            distances.append(distance)

        return distances

    def getPositions(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()
        positions = []
        for scanPointResults in scanPointsResults:
            positions.append(scanPointResults.getPosition())

        return positions

    def getYList(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()
        positions = []
        for scanPointResults in scanPointsResults:
            positions.append(scanPointResults.getPosition())

        yList = []
        for position in positions:
            yList.append(position[1])

        return yList

    def getXList(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()
        positions = []
        for scanPointResults in scanPointsResults:
            positions.append(scanPointResults.getPosition())

        xList = []
        for position in positions:
            xList.append(position[0])

        return xList

    def getZList(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()
        positions = []
        for scanPointResults in scanPointsResults:
            positions.append(scanPointResults.getPosition())

        zList = []
        for position in positions:
            zList.append(position[2])

        return zList

    def _computeDistanceBetweenTwoPositions(self, positionA, positionB):
        argSqrt = 0
        for uA, uB in zip(positionA, positionB):
            argSqrt += (uA - uB)**2

        distance = math.sqrt(argSqrt)
        return distance

    def getBseCoefficient(self, index=0):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        bse = scanPointsResults[index].getBackscatteredCoefficient()
        return bse

    def getBseCoefficients(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        bseList = []
        for scanPointResults in scanPointsResults:
            bse = scanPointResults.getBackscatteredCoefficient()
            bseList.append(bse)
        return bseList

    def getSeCoefficient(self, index=0):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        value = scanPointsResults[index].getSecondaryElectronCoefficient()
        return value

    def getSeCoefficients(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        seList = []
        for scanPointResults in scanPointsResults:
            se = scanPointResults.getSecondaryElectronCoefficient()
            seList.append(se)
        return seList

    def getDepositedEnergies_keV(self, regionInfoIndices):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        values = []
        for scanPointResults in scanPointsResults:
            value = 0.0
            for regionInfoIndex in regionInfoIndices:
                value += scanPointResults.getDepositedEnergies_keV(regionInfoIndex)
            values.append(value)

        return values

    def getTransmittedElectronsCoefficient(self, index=0):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        te = scanPointsResults[index].getTransmittedCoefficient()
        return te

    def getDetectedTransmittedElectrons(self, betaMin_mrad=None, betaMax_mrad=None):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        numberElectronsList = []
        for scanPointResults in scanPointsResults:
            transmittedDetectedCoefficient = scanPointResults.getTransmittedDetectedElectrons(betaMin_mrad, betaMax_mrad)
            numberElectronsList.append(transmittedDetectedCoefficient)

        return numberElectronsList

    def getDetectedTransmittedElectronsCoefficient(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        numberElectronsList = []
        for scanPointResults in scanPointsResults:
            transmittedDetectedCoefficient = scanPointResults.getTransmittedDetectedCoefficient()
            numberElectronsList.append(transmittedDetectedCoefficient)

        return numberElectronsList

    def getDetectedTransmittedElectronsCoefficientError(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        numberElectronsList = []
        for scanPointResults in scanPointsResults:
            numberSimulatedElectrons = scanPointResults.getNumberSimulatedTrajectories()
            transmittedDetectedCoefficient = scanPointResults.getTransmittedDetectedCoefficient()

            error = 3.0*self._computeBinaryVariance(numberSimulatedElectrons, transmittedDetectedCoefficient)
            numberElectronsList.append(error)

        return numberElectronsList

    def _computeBinaryVariance(self, numberSimulatedElectrons, meanValue):
        argSqrt = meanValue*(1.0 - meanValue)/numberSimulatedElectrons
        variance = math.sqrt(argSqrt)
        return variance

    def getTransmittedElectronsByAngles(self, angleBins):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        transmittedElectronsList = []
        for scanPointResults in scanPointsResults:
            angles = scanPointResults.getTransmittedAngles()

            hist = histogram2(angles, angleBins)
            transmittedElectronsList.append(hist)

        return transmittedElectronsList

    def getTransmittedElectronsAngles(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        transmittedElectronsAnglesList = []
        for scanPointResults in scanPointsResults:
            angles = scanPointResults.getTransmittedAngles()

            transmittedElectronsAnglesList.append(angles)

        return transmittedElectronsAnglesList

    def getTransmittedElectronsBinnedAngles(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        transmittedElectronsAnglesList = []
        for scanPointResults in scanPointsResults:
            angles = scanPointResults.getTransmittedBinnedAngles()

            transmittedElectronsAnglesList.append(angles)

        return transmittedElectronsAnglesList

    def getNumberTrajectories(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        numberTrajectoriesList = []
        for scanPointResults in scanPointsResults:
            numberTrajectories = scanPointResults.getNumberSimulatedTrajectories()

            numberTrajectoriesList.append(numberTrajectories)

        return numberTrajectoriesList

    def getTransmittedElectronsByAngleStatistic(self):
        simulationResults = self._simulations[0].getResultList()
        scanPointsResults = simulationResults.getScanPointsResults()

        angleStatisticList = []
        for scanPointResults in scanPointsResults:
            angles = scanPointResults.getTransmittedAngles()
            statistic = statistic.Statistic(angles)
            angleStatisticList.append(statistic)

        return angleStatisticList

    def getTotalDepositedEnergies_keV(self):
        simulationResults = self._simulations[0].getResultList()

        return simulationResults.getTotalDepositedEnergies_keV()


