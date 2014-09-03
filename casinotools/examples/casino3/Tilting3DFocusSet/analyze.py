#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Project modules
import _casino

# Globals and constants variables.

def run():  #pragma: no cover
    """
    Generate all .sim and script files used in the simulation.
    """
    analyze = _casino.SimulationDiscreteTomographyDarkField(overwrite=True, basepath="DiscreteTomography")
    analyze._resetCache = False
    analyze.doAnalyze()

    #analyze.computeNewPositions()

    #analyze = _casino.SimulationDiscreteTomographyBrightField(overwrite=True, basepath="DiscreteTomography")
    #analyze._resetCache = False
    #analyze.doAnalyze(output)

if __name__ == '__main__':  #pragma: no cover
    run()
