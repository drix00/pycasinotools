#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2271 $"
__svnDate__ = "$Date: 2011-03-10 16:32:53 -0500 (Thu, 10 Mar 2011) $"
__svnId__ = "$Id: SimulationData.py 2271 2011-03-10 21:32:53Z hdemers $"

# Standard library modules.
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.Sample as Sample
import casinotools.fileformat.casino3.SimulationOptions as SimulationOptions
import casinotools.fileformat.casino3.ScanPointPositions as ScanPointPositions
import casinotools.fileformat.casino3.SimulationResults as SimulationResults

# TODO: Old Reader modules, refactor to use the data module directly.

# Globals and constants variables.

class SimulationData(object):
    def __init__(self):
        self._sample = Sample.Sample()
        self._options = SimulationOptions.SimulationOptions()
        self._scanPointPositions = ScanPointPositions.ScanPointPositions()
        self._results = SimulationResults.SimulationResults()

    def setSample(self, sample):
        self._sample = sample

    def setOptions(self, options):
        self._options = options

    def setScanPointPositions(self, scanPointPositions):
        self._scanPointPositions = scanPointPositions

    def setResults(self, results):
        self._results = results

    def readSample(self, file):
        self._sample.read(file)

    def readOptions(self, file):
        self._options.read(file)

    def readScanPointPositions(self, file):
        self._scanPointPositions.read(file)

    def readResults(self, file):
        self._results.read(file, self._options)

    def writeSample(self, file):
        logging.info("writeSample")
        self._sample.write(file)

    def writeOptions(self, file):
        logging.info("writeOptions")
        self._options.write(file)

    def writeScanPointPositions(self, file):
        logging.info("writeScanPointPositions")
        self._scanPointPositions.write(file)

    def writeResults(self, file):
        logging.info("writeResults")
        self._results.write(file)

    def getScanPointPositions(self):
        return self._scanPointPositions.getPositions()

    def getResultList(self):
        return self._results

    def getFirstScanPointResults(self):
        return self._results.getFirstScanPointResults()

    def getOptions(self):
        return self._options

    def getSample(self):
        return self._sample

    def export(self, exportFile):
        self._sample.export(exportFile)
        self._options.export(exportFile)
        self._scanPointPositions.export(exportFile)
