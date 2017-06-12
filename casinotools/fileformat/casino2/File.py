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
import os.path

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.SimulationData as SimulationData

# Globals and constants variables.

class File(FileReaderWriterTools.FileReaderWriterTools):
    def __init__(self):
        self._filepath = None
        self._optionSimulationData = None
        self._numberSimulations = 0
        self._resultSimulationDataList = []

    def readFromFilepath(self, filepath, isSkipReadingData=False):
        """
        Read the casino either .sim or .cas file.

        :param filepath: complete filepath to read.
        """
        self._filepath = filepath

        file = open(self._filepath, 'rb')
        self.readFromFileObject(file, isSkipReadingData)

    def readFromFileObject(self, file, isSkipReadingData=False):
        assert getattr(file, 'mode', 'rb') == 'rb'

        file.seek(0)
        # Read the first part of the file corresponding to the option of the simulation.
        # Common to the .sim and .cas files.
        self._optionSimulationData = SimulationData.SimulationData(isSkipReadingData)
        self._optionSimulationData.read(file)

        logging.debug("File position after reading option: %i", file.tell())

        # Read the results for each simulations if the file is a .cas.
        if self._optionSimulationData._save_trajectories:
            self._numberSimulations = self.readInt(file)

            for dummy in range(self._numberSimulations):
                simulationData = SimulationData.SimulationData(isSkipReadingData)
                simulationData.read(file)
                self._resultSimulationDataList.append(simulationData)

        file.close()

    def write(self, filepath):
        if self._optionSimulationData != None:
            self._filepath = filepath

            if self._isSimulationFilepath(self._filepath):
                logging.info("Create CASINO file: %s", self._filepath)

                file = open(self._filepath, 'wb')
                assert getattr(file, 'mode', 'wb') == 'wb'
                file.seek(0)
                self._optionSimulationData.write(file)
                file.close()
        else:
            raise AttributeError("No option simulation data specified.")

    def _isSimulationFilepath(self, filepath):
        extension = os.path.splitext(filepath)[1]

        return (extension.lower() == '.sim')

    def setOptionSimulationData(self, optionSimulationData):
        self._optionSimulationData = optionSimulationData

    def getOptionSimulationData(self):
        return self._optionSimulationData

    def getNumberSimulations(self):
        return len(self._resultSimulationDataList)

    def getResultsFirstSimulation(self):
        return self._resultSimulationDataList[0]

    def getResultsSimulation(self, index):
        return self._resultSimulationDataList[index]

def _run():
    from pkg_resources import resource_filename #@UnresolvedImport
    filepathCas = resource_filename(__file__, "../../test_data/wincasino2.45/id475.cas")
    file = File()
    file.readFromFilepath(filepathCas, isSkipReadingData=True)

def runProfile():
    import cProfile
    cProfile.run('_run()', 'Casino2.x_File.prof')

def runProfile2():
    try:
        import hotshot
    except ImportError: # hotshot not supported in Python 3
        return

    prof = hotshot.Profile("Casino2.x_File.prof", lineevents=1)
    prof.runcall(_run)
    prof.close()

if __name__ == '__main__': #pragma: no cover
    runProfile()
