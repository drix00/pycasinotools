#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2010 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import os

# Third party modules.

# Local modules.
import casinotools.fileformat.casino3.File as Casino3File

# Globals and constants variables.

class ExportSimulationParameters(object):
    def __init__(self):
        self._isExportAllParameters = True

    def export(self, filepath):
        exportFilepath = _getExportFilepath(filepath)

        exportFile = open(exportFilepath, 'wb')

        casinoFile = Casino3File.File(filepath)

        casinoFile.export(exportFile)

        exportFile.close()

    def getRegionCompositionData(self, filepath):
        casinoFile = Casino3File.File(filepath)
        regions = casinoFile.getFirstSimulation().getSample().getRegions()

        data = []

        for region in regions:
            regionName = region.getName()
            composition = region.getComposition()

            data.append((regionName, composition))

        return data

    def getShapePositionDimensionData(self, filepath):
        casinoFile = Casino3File.File(filepath)
        sample = casinoFile.getFirstSimulation().getSample()

        shapes = sample.getShapes()

        data = []
        for shape in shapes:
            name = shape.getName()
            type = shape.getType()
            position_nm = shape.getTranslation_nm()
            dimension_nm = shape.getScale_nm()

            datum = (name, type, position_nm, dimension_nm)
            data.append(datum)

        return data

def _getExportFilepath(filepath):
    exportFilepath, dummyExtension = os.path.splitext(filepath)
    exportFilepath += ".txt"

    return exportFilepath

def run():
    import pyHendrixDemersTools.Files as Files
    path = Files.getCurrentModulePath(__file__, "testData/casino3.x/ExportParameters")

    filenames = ["ProblemSampleRotation_fz0nm_t0deg.sim", "ProblemSampleRotation_fz0nm_t30deg.sim", "ProblemSampleRotation_fz0nm_t-30deg.sim"]
    for filename in filenames:
        filepath = os.path.join(path, filename)
        exportParameters = ExportSimulationParameters()
        exportParameters.export(filepath)

if __name__ == '__main__':  #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
