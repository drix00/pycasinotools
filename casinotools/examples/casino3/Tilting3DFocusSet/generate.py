#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import shutil
import logging

# Third party modules.
import numpy as np

# Local modules.
import _casino
import casinotools.fileformat.casino3.File as CasinoFile

# Project modules

# Globals and constants variables.

def createTiltSimulationFilenames():
    """
    Generate all .sim with the correct titl name.
    """
    analyze = _casino._AnalyzeCasinoSimulation(overwrite=True, basepath="DiscreteTomography")

    sourceFilepath = os.path.join(analyze.getInputPath(), "DataSetBatenburg_GoldinCarbon_Center_X_T500nm_tiltY+0.0deg_woSE.sim")

    #tilts_deg = np.arange(-70.0, 70.0, 0.5)
    tilts_deg = np.arange(-70.0, 70.0, 2.0)
    for tilt_deg in tilts_deg:
        filename = "DataSetBatenburg_GoldinCarbon_Center_X_T500nm_tiltY%+0.1fdeg_woSE.sim" % (tilt_deg)
        destinationFilepath = os.path.join(analyze.getInputPath(), filename)
        if not os.path.isfile(destinationFilepath):
            destinationFilepath = os.path.join(analyze.getInputPath(), 'todo', filename)
            shutil.copy2(sourceFilepath, destinationFilepath)
        else:
            casinoFile = CasinoFile.File(destinationFilepath)
            sample = casinoFile.getFirstSimulation().getSample()
            rotationY_deg = _extractRotationY_deg(filename)
            if rotationY_deg != sample.getRotationY_deg():
                logging.info("%s: %5.1f %5.1f ", filename, rotationY_deg, sample.getRotationY_deg())

def _extractRotationY_deg(filename):
    # DataSetBatenburg_GoldinCarbon_Center_X_T500nm_tiltY0.1deg_woSE.sim
    items = filename.split('_')
    item = items[5]
    value = float(item[5:-3])
    return value

def createTiltSimulationFiles():
    """
    Generate all .sim with the correct titl name.
    """
    analyze = _casino._AnalyzeCasinoSimulation(overwrite=True, basepath="DiscreteTomography")

    sourceFilepath = os.path.join(analyze.getInputPath(), "DataSetBatenburg_GoldinCarbon_Center_X_T500nm_tiltY+0.0deg_woSE.sim")

    #tilts_deg = np.arange(-70.0, 70.0, 0.5)
    tilts_deg = [70.0]
    for tilt_deg in tilts_deg:
        filename = "DataSetBatenburg_GoldinCarbon_Center_X_T500nm_tiltY%+0.1fdeg_woSE.sim" % (tilt_deg)
        destinationFilepath = os.path.join(analyze.getInputPath(), filename)
        casinoFile = CasinoFile.File(sourceFilepath)
        sample = casinoFile.getFirstSimulation().getSample()
        logging.info("%s: %5.1f %5.1f ", filename, sample.getRotationY_deg(), sample.getRotationZ_deg())
        sample.setRotationY_deg(tilt_deg)

        casinoFile.closeFile()
        casinoFile.save(destinationFilepath)

        casinoFile = CasinoFile.File(destinationFilepath)
        sample = casinoFile.getFirstSimulation().getSample()
        logging.info("%s: %5.1f %5.1f ", filename, sample.getRotationY_deg(), sample.getRotationZ_deg())

def run():  #pragma: no cover
    """
    Generate all .sim and script files used in the simulation.
    """
    analyze = _casino.SimulationDiscreteTomographyDarkField(overwrite=True, basepath="DiscreteTomography")
    analyze.generateScripts()

if __name__ == '__main__':  #pragma: no cover
    run()
