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
import scitools.multipleloop

# Local modules.
from casinotools.scripting.casino3 import CasinoSimulationExperiment
import SimulationParameters

# Globals and constants variables.

class CasinoSimulationExperimentSet(object):
    def __init__(self, parameters=None):
        if parameters != None:
            self.setParameters(parameters)

    def setParameters(self, parameters):
        self._parameters = parameters

    def createAllExperiments(self):
        all, names, dummyVaried = scitools.multipleloop.combine(self._parameters)

        experiments = []

        if SimulationParameters.SCAN_POINT_FILES in names:
            index = names.index(SimulationParameters.SCAN_POINT_FILES)
            names.insert(index, SimulationParameters.ERASE_ALL_SCANPOINTS)
        if SimulationParameters.SCAN_POINT in names:
            index = names.index(SimulationParameters.SCAN_POINT)
            names.insert(index, SimulationParameters.ERASE_ALL_SCANPOINTS)
        for values in all:
            if SimulationParameters.SCAN_POINT_FILES in names:
                values.insert(index, "")
            if SimulationParameters.SCAN_POINT in names:
                values.insert(index, "")

            if SimulationParameters.TOTAL_CROSS_SECTION in names and SimulationParameters.PARTIAL_CROSS_SECTION in names:
                indexTotal = names.index(SimulationParameters.TOTAL_CROSS_SECTION)
                indexPartial = names.index(SimulationParameters.PARTIAL_CROSS_SECTION)
                if values[indexTotal] == values[indexPartial]:
                    experiment = CasinoSimulationExperiment.CasinoSimulationExperiment(names, values)
                    experiments.append(experiment)
            else:
                experiment = CasinoSimulationExperiment.CasinoSimulationExperiment(names, values)
                experiments.append(experiment)

        self._experiments = experiments

    def nextExperiment(self):
        for experiment in self._experiments:
            yield experiment
