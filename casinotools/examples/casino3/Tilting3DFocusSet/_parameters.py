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
from casinotools.analysis.casino3.parameters import _Parameters

# Globals and constants variables.

class Parameters(_Parameters):
    def _initKeywords(self):
        self._keywords = [self.KEY_SIMULATION_NAME,
                          self.KEY_SAMPLE_NAME,
                          self.KEY_SAMPLE_POSITION,
                          self.KEY_SAMPLE_ORIENTATION,
                          self.KEY_SAMPLE_THICKNESS,
                          self.KEY_TILT_Y,
                          self.KEY_SECONDARY_ELECTRON,
                          self.KEY_LINESCAN_DIRECTION,
                          self.KEY_LINESCAN_WIDTH,
                          self.KEY_LINESCAN_HEIGHT,
                          self.KEY_LINESCAN_NUMBER_POINTS,
                          self.KEY_ENERGY,
                          self.KEY_BEAM_RADIUS,
                          self.KEY_BEAM_SEMI_ANGLE,
                          self.KEY_NUMBER_ELECTRONS]
