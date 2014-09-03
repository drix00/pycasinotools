#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2011 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import os.path
import logging

# Third party modules.

# Local modules.

# Project modules

# Globals and constants variables.

class _Parameters(dict):
    """
    .. py:currentclass:: _Parameters
       :exclude-members: update

    """
    KEY_PROJECT_NAME = "projectName"
    KEY_SIMULATION_NAME = "simulationName"
    KEY_SAMPLE_NAME = "sampleName"
    KEY_PARTICLE_POSITION = "particlePosition"
    KEY_PARTICLE_POSITION_STRING = "particlePositionString"
    KEY_PARTICLE_DIAMETER = "particleDiameter"
    KEY_PARTICLE_RADIUS = "particleRadius"
    KEY_SAMPLE_POSITION = "samplePosition"
    KEY_SAMPLE_ORIENTATION = "sampleOrientation"
    KEY_SAMPLE_THICKNESS = "sampleThickness"
    KEY_TILT_Y = "tiltY"
    KEY_SECONDARY_ELECTRON = "secondaryElectron"
    KEY_SCAN_TYPE = "scanType"
    KEY_LINESCAN_DIRECTION = "linescanDirection"
    KEY_LINESCAN_WIDTH = "linescanWidth"
    KEY_LINESCAN_HEIGHT = "linescanHeight"
    KEY_LINESCAN_POSITION_X = "linescanPositionX"
    KEY_LINESCAN_POSITION_Y = "linescanPositionY"
    KEY_LINESCAN_POSITION_Z = "linescanPositionZ"
    KEY_LINESCAN_STEP_SIZE = "linescanStepSize"
    KEY_LINESCAN_NUMBER_POINTS = "linescanNumberPoints"
    KEY_LINESCAN_NUMBER_LINES = "linescanNumberLines"
    KEY_SCAN_POINT_X = "scanPointX"
    KEY_SCAN_POINT_Y = "scanPointY"
    KEY_SCAN_POINT_Z = "scanPointZ"
    KEY_ENERGY = "energy"
    KEY_BEAM_RADIUS = "beamRadius"
    KEY_BEAM_SEMI_ANGLE = "beamSemiAngle"
    KEY_BEAM_DISTRIBUTION = "beamDistribution"
    KEY_NUMBER_ELECTRONS = "numberElectrons"
    KEY_REPETITION_ID = "repetitionId"

    def __init__(self, filepath):
        self.clear()
        self._initKeywords()
        self._createFormatList()
        self._extractFromFilepath(filepath)

    def _initKeywords(self):
        raise NotImplementedError

    def _createFormatList(self):
        self._formatList = {}
        self._formatList[self.KEY_PROJECT_NAME] = ("", "%s", str, "")
        self._formatList[self.KEY_SIMULATION_NAME] = ("", "%s", str, "")
        self._formatList[self.KEY_SAMPLE_NAME] = ("", "%s", str, "")
        self._formatList[self.KEY_PARTICLE_POSITION] = ("pz", "%s", str, "nm")
        self._formatList[self.KEY_PARTICLE_POSITION_STRING] = ("", "%s", str, "")
        self._formatList[self.KEY_PARTICLE_DIAMETER] = ("d", "%s", str, "nm")
        self._formatList[self.KEY_PARTICLE_RADIUS] = ("sr", "%s", str, "nm")
        self._formatList[self.KEY_SAMPLE_POSITION] = ("", "%s", str, "")
        self._formatList[self.KEY_SAMPLE_ORIENTATION] = ("", "%s", str, "")
        self._formatList[self.KEY_SAMPLE_THICKNESS] = ("T", "%s", str, "nm")
        self._formatList[self.KEY_TILT_Y] = ("sr", "%s", str, "nm")
        self._formatList[self.KEY_SECONDARY_ELECTRON] = ("", "%s", str, "")
        self._formatList[self.KEY_SCAN_TYPE] = ("", "%s", str, "")
        self._formatList[self.KEY_LINESCAN_DIRECTION] = ("pz", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_WIDTH] = ("w", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_HEIGHT] = ("h", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_POSITION_X] = ("LX", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_POSITION_Y] = ("LY", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_POSITION_Z] = ("LZ", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_STEP_SIZE] = ("ps", "%s", str, "nm")
        self._formatList[self.KEY_LINESCAN_NUMBER_POINTS] = ("", "%s", str, "pts")
        self._formatList[self.KEY_LINESCAN_NUMBER_LINES] = ("NL", "%s", str, "")
        self._formatList[self.KEY_SCAN_POINT_X] = ("fx", "%s", str, "nm")
        self._formatList[self.KEY_SCAN_POINT_Y] = ("fy", "%s", str, "nm")
        self._formatList[self.KEY_SCAN_POINT_Z] = ("fz", "%s", str, "nm")
        self._formatList[self.KEY_ENERGY] = ("E", "%s", str, "keV")
        self._formatList[self.KEY_BEAM_RADIUS] = ("br", "%s", str, "nm")
        self._formatList[self.KEY_BEAM_SEMI_ANGLE] = ("a", "%s", str, "mrad")
        self._formatList[self.KEY_BEAM_DISTRIBUTION] = ("", "%s", str, "")
        self._formatList[self.KEY_NUMBER_ELECTRONS] = ("N", "%s", str, "e")
        self._formatList[self.KEY_REPETITION_ID] = ("Id", "%s", str, "X")

    def __hash__(self):
        keys = sorted(self.keys())

        values = tuple([self[key] for key in keys])

        return values.__hash__()

    def __str__(self):
        self._createFormatList()

        keyword = self._keywords[0]
        item = self[keyword]
        text = self._generateTextFromValue(keyword, item)[1:]
        for keyword in self._keywords[1:]:
            try:
                item = self[keyword]
                text += self._generateTextFromValue(keyword, item)
            except KeyError, message:
                logging.error(message)

        return text

    def _extractFromFilepath(self, filepath):
        """
        """
        if filepath is None:
            logging.warning("Not filepath specified (None).")
            return
        if len(filepath) == 0:
            logging.warning("Not filepath specified (empty string).")
            return

        basename, dummyExtension = os.path.splitext(os.path.basename(filepath))
        items = basename.split('_')

        logging.debug("Number of items: %i", len(items))

        numberItems = len(self._keywords)
        if len(items) < numberItems:
            message = "Wrong number of items in filename: got %i expected %i." % (len(items), numberItems)
            logging.error(message)
            raise ValueError, message

#        for index, keyword in enumerate(self._keywords):
#            item = items[index]
#            self[keyword] = self._extractValueFromItem(keyword, item)

        for keyword in self._keywords:
            for index, item in enumerate(items):
                try:
                    self[keyword] = self._extractValueFromItem(keyword, item)
                    items = items[index+1:]
                    break
                except ValueError:
                    pass

    def _extractValueFromItem(self, keyword, item):
        if keyword == self.KEY_PROJECT_NAME:
            return str(item)
        elif keyword == self.KEY_SIMULATION_NAME:
            return str(item)
        elif keyword == self.KEY_PARTICLE_POSITION:
            return _extractParticlePosition(item)
        elif keyword == self.KEY_PARTICLE_POSITION_STRING:
            return str(item)
        elif keyword == self.KEY_PARTICLE_DIAMETER:
            return _extractParticleDiameter(item)
        elif keyword == self.KEY_PARTICLE_RADIUS:
            return _extractParticleRadius(item)
        elif keyword == self.KEY_SAMPLE_NAME:
            return str(item)
        elif keyword == self.KEY_SAMPLE_POSITION:
            return str(item)
        elif keyword == self.KEY_SAMPLE_ORIENTATION:
            return str(item)
        elif keyword == self.KEY_SAMPLE_THICKNESS:
            return _extractSampleThickness(item)
        elif keyword == self.KEY_TILT_Y:
            return _extractSampleTiltY(item)
        elif keyword == self.KEY_SECONDARY_ELECTRON:
            return _extractSecondaryElectron(item)
        elif keyword == self.KEY_SCAN_TYPE:
            return str(item)
        elif keyword == self.KEY_LINESCAN_DIRECTION:
            return str(item)
        elif keyword == self.KEY_LINESCAN_POSITION_X:
            return _extractLinescanPositionX(item)
        elif keyword == self.KEY_LINESCAN_POSITION_Y:
            return _extractLinescanPositionY(item)
        elif keyword == self.KEY_LINESCAN_POSITION_Z:
            return _extractLinescanPositionZ(item)
        elif keyword == self.KEY_LINESCAN_WIDTH:
            return _extractLinescanWidth(item)
        elif keyword == self.KEY_LINESCAN_HEIGHT:
            return _extractLinescanHeight(item)
        elif keyword == self.KEY_LINESCAN_STEP_SIZE:
            return _extractLinescanStepSize(item)
        elif keyword == self.KEY_LINESCAN_NUMBER_POINTS:
            return _extractLinescanNumberPoints(item)
        elif keyword == self.KEY_LINESCAN_NUMBER_LINES:
            return _extractLinescanNumberLines(item)
        elif keyword == self.KEY_SCAN_POINT_X:
            return _extractScanPointX(item)
        elif keyword == self.KEY_SCAN_POINT_Y:
            return _extractScanPointY(item)
        elif keyword == self.KEY_SCAN_POINT_Z:
            return _extractScanPointZ(item)
        elif keyword == self.KEY_ENERGY:
            return _extractEnergy(item)
        elif keyword == self.KEY_BEAM_DISTRIBUTION:
            return _extractBeamDistribution(item)
        elif keyword == self.KEY_BEAM_RADIUS:
            return _extractBeamRadius(item)
        elif keyword == self.KEY_BEAM_SEMI_ANGLE:
            return _extractBeamSemiAngle(item)
        elif keyword == self.KEY_NUMBER_ELECTRONS:
            return _extracNumberElectrons(item)
        elif keyword == self.KEY_REPETITION_ID:
            return _extracRepetitionId(item)

        message = "No method implemented for keyowrd: %s" % (keyword)
        raise NotImplementedError, message

    def _extractValueFromText(self, keyword, text):
        #prefix, format, conversion, suffix = self._formatList[keyword]
        #text = "_" + prefix + format % (conversion(self[keyword])) + suffix
        raise NotImplementedError

    def _generateTextFromValue(self, keyword, value):
        prefix, string_format, conversion, suffix = self._formatList[keyword]
        text = "_" + prefix + string_format % (conversion(self[keyword])) + suffix

        return text

def _extractSampleThickness(text):
    """
    T1000nm
    """

    if text.startswith('T') and text.endswith('nm'):
        value = text[1:-2]
        return value
    elif text.startswith('T') and text.endswith('um'):
        value = text[1:-2]
        return value
    else:
        raise ValueError

def _extractSampleTiltY(text):
    """
    tiltY70deg
    """

    if text.startswith('tiltY') and text.endswith('deg'):
        value = text[5:-3]
        return value
    else:
        raise ValueError

def _extractSecondaryElectron(text):
    """
    woSE
    """

    if text == "woSE":
        value = "woSE"
        return value
    if text == "wSE":
        value = "wSE"
        return value
    else:
        raise ValueError

def _extractLinescanPositionX(text):
    """
    X20nm
    """

    if text.startswith('X') and text.endswith('nm'):
        value = text[1:-2]
        return value
    else:
        raise ValueError

def _extractLinescanPositionY(text):
    """
    y-20nm
    """

    if text.startswith('y') and text.endswith('nm'):
        value = text[1:-2]
        return value
    else:
        raise ValueError

def _extractLinescanWidth(text):
    """
    520nm
    or
    w520nm
    """

    if text.startswith('w') and text.endswith('nm'):
        value = text[1:-2]
        return value
    elif text.endswith('nm'):
        value = text[:-2]
        return value
    else:
        raise ValueError

def _extractLinescanHeight(text):
    """
    h52nm
    """

    if text.startswith('h') and text.endswith('nm'):
        value = text[1:-2]
        return value
    else:
        raise ValueError

def _extractLinescanNumberPoints(text):
    """
    520pts
    """

    if text.endswith('pts'):
        value = text[:-3]
        return value
    else:
        raise ValueError

def _extractLinescanNumberLines(text):
    """
    NL020
    """

    if text.startswith('NL'):
        value = text[2:]
        return value
    else:
        raise ValueError

def _extractScanPointX(text):
    """
    fx-20nm
    """

    if text.startswith('fx') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractScanPointY(text):
    """
    fy-20nm
    """

    if text.startswith('fy') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractScanPointZ(text):
    """
    fz-20nm
    """

    if text.startswith('fz') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractEnergy(text):
    """
    E200.0keV
    """

    if text.startswith('E') and text.endswith('keV'):
        value = text[1:-3]
        return value
    elif text.endswith('keV'):
        value = text[:-3]
        return value
    else:
        raise ValueError

def _extractBeamRadius(text):
    """
    br0.5nm
    """

    if text.startswith('br') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractBeamSemiAngle(text):
    """
    a2.0mrad
    """

    if text.startswith('a') and text.endswith('mrad'):
        value = text[1:-4]
        return value
    else:
        raise ValueError

def _extracNumberElectrons(text):
    """
    N100ke
    """

    if text.startswith('N') and text.endswith('e'):
        value = text[1:-1]
        return value
    elif text.endswith('e'):
        value = text[:-1]
        return value
    else:
        raise ValueError

def _extracRepetitionId(text):
    """
    Id10X
    """

    if text.startswith('Id') and text.endswith('X'):
        value = text[2:-1]
        return value
    else:
        raise ValueError

def _extractParticlePosition(text):
    """
    Z20nm
    """
    if text.startswith('pz') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractParticleDiameter(text):
    """
    d20nm
    """
    if text.startswith('d') and text.endswith('nm'):
        value = text[1:-2]
        return value
    else:
        raise ValueError

def _extractParticleRadius(text):
    """
    sr20nm
    """
    if text.startswith('sr') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractLinescanStepSize(text):
    """
    ps1nm
    """
    if (text.startswith('ps') or text.startswith('ss')) and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractLinescanPositionZ(text):
    """
    fz500nm
    """
    if text.startswith('fz') and text.endswith('nm'):
        value = text[2:-2]
        return value
    else:
        raise ValueError

def _extractBeamDistribution(text):
    """
    bG
    """
    if text.startswith('b') and len(text) == 2:
        value = text[1:]
        return value
    else:
        raise ValueError

def getThicknessFromFilename(filename):
    basename, _extension = os.path.splitext(filename)

    items = basename.split('_')

    for item in items:
        try:
            value = _extractSampleThickness(item)
            return value
        except ValueError:
            pass

    raise ValueError

if __name__ == '__main__':  #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
