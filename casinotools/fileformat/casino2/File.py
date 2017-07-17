#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.File

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

CASINO file structure: either sim or .cas.
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
import os.path

# Third party modules.

# Local modules.

# Project modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools
import casinotools.fileformat.casino2.SimulationData as SimulationData
from casinotools.fileformat.casino2.Version import UNKNOWN_VERSION

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

    def extract_version(self, file_path):
        version = UNKNOWN_VERSION

        with open(file_path, 'rb') as casino_file:
            casino_file.seek(0)

            tag_id = SimulationData.TAG_VERSION
            if self.findTag(casino_file, tag_id):
                logging.debug("File pos: %i", casino_file.tell())
                version = self.readInt(casino_file)

        return version


def _run():
    from pkg_resources import resource_filename  # @UnresolvedImport
    file_path_cas = resource_filename(__file__, "../../test_data/wincasino2.45/id475_v2.46.cas")
    file = File()
    file.readFromFilepath(file_path_cas, isSkipReadingData=True)


def run_profile():
    import cProfile
    cProfile.run('_run()', 'Casino2.x_File.prof')


def run_profile2():
    try:
        import hotshot
    except ImportError:  # hotshot not supported in Python 3
        return

    prof = hotshot.Profile("Casino2.x_File.prof", lineevents=1)
    prof.runcall(_run)
    prof.close()


if __name__ == '__main__':  # pragma: no cover
    run_profile()
