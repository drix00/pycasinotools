#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.examples.casino3.AnalyseTransmittedElectrons
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Examples of transmitted electrons anlysis from CASINO v3 simulations.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import logging
import math

# Third party modules.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection

# Local modules.
import pyHendrixDemersTools.Files as Files
import pyHendrixDemersTools.Graphics as Graphics

# Project modules
import casinotools.fileformat.casino3.File as CasinoFile
from casinotools.analysis.casino3.transmitted_electrons import Result

# Globals and constants variables.

class TransmittedElectrons(object):
    def __init__(self, output, labels=None):
        self._output = output
        self._labels = labels
        self._names = []

        self._results = {}

    def _readFile(self, filepath):
        logging.info("Reading filepath: %s", filepath)
        name = self._extractNameFromFilepath(filepath)
        self._names.append(name)

        casinoFile = CasinoFile.File(filepath)
        result = Result()

        result.setSimulations(casinoFile.getSimulations())

        self._results[name] = result

    def _extractNameFromFilepath(self, filepath):
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]

        return name

    def _doGraphicDetected(self, name, normalized=False, error=False):
        result = self._results[name]
        plt.figure()
        plt.title(name)

        #x = result.getDistancesFromFirstOne()
        x = result.getDistancesFromOrigine()
        y = result.getDetectedTransmittedElectronsCoefficient()
        yError = result.getDetectedTransmittedElectronsCoefficientError()

        if error:
            plt.errorbar(x, y, yError)
        else:
            if normalized:
                yMin = min(y)
                if yMin != 0.0:
                    y = [yy/yMin for yy in y]
            plt.plot(x, y)

        plt.xlabel("Distance (nm)")
        plt.ylabel("Detected TE coefficient")

        if self._output != Graphics.DISPLAY:
            graphicsPath = Graphics.getOutputPath(self._output)

            for extension in Graphics.getGraphicsExtentions(self._output):
                filename = name
                if normalized:
                    filename += "_norm"
                if error:
                    filename += "_error"
                filename += extension

                filepath = os.path.join(graphicsPath, filename)
                plt.savefig(filepath)

    def _doGraphicAngles3D2(self, name):
        result = self._results[name]
        figure = plt.figure()
        axes = Axes3D(figure)

        plt.title(name)

        numberAngles = 90
        angleBins = np.linspace(0.0, math.pi/2.0, numberAngles)

        transmittedElectronsList = result.getTransmittedElectronsByAngles(angleBins)

        for distance, transmittedElectrons in zip(result.getDistancesFromFirstOne(), transmittedElectronsList):
            print "%.2f\t:%s" % (distance, transmittedElectrons)
            axes.bar(angleBins, transmittedElectrons, zs=distance, zdir='y', alpha=0.8)

        axes.set_xlabel("Angle (mrad)")
        axes.set_ylabel("Distance (nm)")
        axes.set_zlabel("Number TE")

    def _doGraphicAngles3D(self, name):
        result = self._results[name]
        figure = plt.figure()
        axes = Axes3D(figure)

        plt.title(name)

        distances = result.getDistancesFromFirstOne()
        numberAngles = 90
        angleBins = np.linspace(0.0, math.pi/2.0, numberAngles)

        transmittedElectronsList = result.getTransmittedElectronsByAngles(angleBins)

        maxZ = 0.0
        verts = []
        for dummy, transmittedElectrons in zip(distances, transmittedElectronsList):
            y = np.array(transmittedElectrons)
            logY = np.log(y)
            logY[0], logY[-1] = 0, 0
            y[0], y[-1] = 0, 0
            verts.append(zip(angleBins, logY))
            maxZ = max(maxZ, max(logY))

        poly = PolyCollection(verts)

        poly.set_alpha(0.7)
        axes.add_collection3d(poly, zs=distances, zdir='y')

        axes.set_xlim3d(0, math.pi/2.0)
        axes.set_ylim3d(distances[0], distances[-1])
        axes.set_zlim3d(0, maxZ)

        axes.set_xlabel("Angle (mrad)")
        axes.set_ylabel("Distance (nm)")
        axes.set_zlabel("Number TE")

    def _doGraphicDetectedAll(self, graphicName, normalized=False, error=False):
        plt.figure()
        plt.title(graphicName)
        for name in self._names:
            result = self._results[name]

            #x = result.getDistancesFromFirstOne()
            x = result.getDistancesFromOrigine()
            y = result.getDetectedTransmittedElectronsCoefficient()
            yError = result.getDetectedTransmittedElectronsCoefficientError()

            label = self._labels[name]
            if error:
                plt.errorbar(x, y, yError, label=label)
            else:
                if normalized:
                    yMin = min(y)
                    if yMin != 0.0:
                        y = [yy/yMin for yy in y]
                plt.plot(x, y, label=label)

            plt.xlabel("Distance (nm)")
            plt.ylabel("Detected TE coefficient")
            plt.legend(loc='best')

        if self._output != Graphics.DISPLAY:
            graphicsPath = Graphics.getOutputPath(self._output)

            for extension in Graphics.getGraphicsExtentions(self._output):
                filename = graphicName
                if normalized:
                    filename += "_norm"
                if error:
                    filename += "_error"
                filename += extension

                filename = Files.sanitizeFilename(filename)
                filepath = os.path.join(graphicsPath, filename)
                plt.savefig(filepath)

    def doGraphics(self, experimentName):
        logging.info("doGraphics ...")
        self._doGraphicDetectedAll(experimentName)
        self._doGraphicDetectedAll(experimentName, normalized=True)
        self._doGraphicDetectedAll(experimentName, error=True)

        for name in self._results:
            self._doGraphicDetected(name)
            self._doGraphicDetected(name, normalized=True)
            self._doGraphicDetected(name, error=True)

            #self._doGraphicAngles3D(name)

    def doAnalysis(self):
        logging.info("doAnalysis ...")
        for name in self._results:
            self._doAnalysisDetected(name)

    def _doAnalysisDetected(self, name):
        import pyUdeS.ParticleLinescanAnalysis as ParticleLinescanAnalysis

        result = self._results[name]
        plt.figure()
        plt.title(name)

        #x = result.getDistancesFromFirstOne()
        x = result.getDistancesFromOrigine()
        y = result.getDetectedTransmittedElectronsCoefficient()
        yError = result.getDetectedTransmittedElectronsCoefficientError()

        plt.errorbar(x, y, yError)
        #plt.plot(x, y)

        particleLinescanAnalysis = ParticleLinescanAnalysis.ParticleLinescanAnalysis()
        particleLinescanAnalysis.setLinescan(x, y, yError)
        particleLinescanAnalysis.doAnalysis()
        particleLinescanAnalysis.doGraphics()

        plt.xlabel("Distance (nm)")
        plt.ylabel("Detected TE coefficient")

        if self._output != Graphics.DISPLAY:
            graphicsPath = Graphics.getOutputPath(self._output)

            for extension in Graphics.getGraphicsExtentions(self._output):
                filename = name + "_SNR"
                filename += extension

                filename = Files.sanitizeFilename(filename)
                filepath = os.path.join(graphicsPath, filename)
                plt.savefig(filepath)

def runTest():
    #logging.getLogger().setLevel(logging.DEBUG)
    output = Graphics.DISPLAY
    Graphics.setDefault(output)

    basepath = Files.getWorksPath("casinotools.cfg", "/UdeS/3DSTEM/simulations/Microfluidic/SecondaryElectrons/")

    label = {"WaterAuTop_wSE": "Top w SE"}
    analyze = TransmittedElectrons(output, label)
    filename = "WaterAuTop_wSE.cas"
    filepath = os.path.join(basepath, filename)
    analyze._readFile(filepath)

    analyze.doAnalysis()

    if output == Graphics.DISPLAY:
        plt.show()

def run():
    output = Graphics.DISPLAY
    Graphics.setDefault(output)

    basepath = Files.getResultsSherbrookePath("casinotools.cfg", "Simulations/Microfluidic/SecondaryElectrons/")

    labels = {}
    experiments = {}

    filenames = ["WaterAuTop_wSE.cas", "WaterAuTop_woSE.cas"
                             , "WaterAuBottom_wSE.cas", "WaterAuBottom_woSE.cas"]
    experiments["Au 5nm"] = filenames
    labels["Au 5nm"] = {"WaterAuTop_wSE": "Top w SE" , "WaterAuTop_woSE": "Top wo SE"
                        , "WaterAuBottom_wSE": "Bottom w SE", "WaterAuBottom_woSE": "Bottom wo SE"}

#    filenames = ["WaterAuTop_45nm_wSE.cas", "WaterAuTop_45nm_woSE.cas"
#                             , "WaterAuBottom_45nm_wSE.cas", "WaterAuBottom_45nm_woSE.cas"]
#    experiments["Au 45nm"] = filenames
#    labels["Au 45nm"] = {"WaterAuTop_45nm_wSE": "Top w SE" , "WaterAuTop_45nm_woSE": "Top wo SE"
#                        , "WaterAuBottom_45nm_wSE": "Bottom w SE", "WaterAuBottom_45nm_woSE": "Bottom wo SE"}
#
#    filenames = ["WaterAuTop_wSE.cas", "WaterAuTop_woSE.cas"]
#    experiments["Au 5nm Top"] = filenames
#    labels["Au 5nm Top"] = {"WaterAuTop_wSE": "w SE" , "WaterAuTop_woSE": "wo SE"}
#
#    filenames = ["WaterAuBottom_wSE.cas", "WaterAuBottom_woSE.cas"]
#    experiments["Au 5nm Bottom"] = filenames
#    labels["Au 5nm Bottom"] = {"WaterAuBottom_wSE": "w SE" , "WaterAuBottom_woSE": "wo SE"}
#
#    filenames = ["WaterAuTop_45nm_wSE.cas", "WaterAuTop_45nm_woSE.cas"]
#    experiments["Au 45nm Top"] = filenames
#    labels["Au 45nm Top"] = {"WaterAuTop_45nm_wSE": "w SE" , "WaterAuTop_45nm_woSE": "wo SE"}
#
#    filenames = ["WaterAuBottom_45nm_wSE.cas", "WaterAuBottom_45nm_woSE.cas"]
#    experiments["Au 45nm Bottom"] = filenames
#    labels["Au 45nm Bottom"] = {"WaterAuBottom_45nm_wSE": "w SE" , "WaterAuBottom_45nm_woSE": "wo SE"}

    for experimentName in experiments:
        label = labels[experimentName]
        analyze = TransmittedElectrons(output, label)
        filenames = experiments[experimentName]
        for filename in filenames:
            try:
                filepath = os.path.join(basepath, filename)
                analyze._readFile(filepath)
            except IOError:
                logging.warning("File not found: %s", filepath)

        #analyze.doGraphics(experimentName)
        analyze.doAnalysis()

    if output == Graphics.DISPLAY:
        plt.show()

def runMaxOrderSE():
    output = Graphics.LABBOOK_SHERBROOKE
    Graphics.setDefault(output)

    basepath = Files.getWorksPath("casinotools.cfg", "/UdeS/3DSTEM/simulations/Microfluidic/SecondaryElectrons/")

    labels = {}
    experiments = {}

    filenames = ["AuSphere_woSE.cas", "AuSphere_wSE_10.cas"
                             , "AuSphere_wSE_20.cas", "AuSphere_wSE_50.cas", "AuSphere_wSE_100.cas"]
    experiments["Maximum Order"] = filenames
    labels["Maximum Order"] = {"AuSphere_woSE" : "wo SE", "AuSphere_wSE_10": "10"
                             , "AuSphere_wSE_20": "20", "AuSphere_wSE_50": "50", "AuSphere_wSE_100": "100"}

    for experimentName in experiments:
        label = labels[experimentName]
        analyze = TransmittedElectrons(output, label)
        filenames = experiments[experimentName]
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            analyze._readFile(filepath)

        analyze.doGraphics(experimentName)
        #analyze.doAnalysis()

    if output == Graphics.DISPLAY:
        plt.show()

def runWaterSE():
    output = Graphics.DISPLAY
    Graphics.setDefault(output)

    basepath = Files.getResultsSherbrookePath("casinotools.cfg", "Simulations/Microfluidic/SecondaryElectrons/")

    labels = {}
    experiments = {}

    filenames = ["Water_woSE.cas", "Water_wSE.cas"]
    experiments["Water"] = filenames
    labels["Water"] = {"Water_woSE" : "wo SE", "Water_wSE": "w SE"}

    for experimentName in experiments:
        label = labels[experimentName]
        analyze = TransmittedElectrons(output, label)
        filenames = experiments[experimentName]
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            analyze._readFile(filepath)

        analyze.doGraphics(experimentName)
        #analyze.doAnalysis()

    if output == Graphics.DISPLAY:
        plt.show()

def _run():
    basepath = Files.getWorksPath("casinotools.cfg", "/UdeS/3DSTEM/simulations/Microfluidic/SecondaryElectrons/")
    filenames = ["WaterAuTop_wSE.cas"]
    analyze = TransmittedElectrons()

    for filename in filenames:
        filepath = os.path.join(basepath, filename)
        analyze._readFile(filepath)

def runProfile():
    import cProfile
    cProfile.run('_run()', 'AnalyzeTransmittedElectrons.prof')

def runH2O():
    output = Graphics.DISPLAY
    Graphics.setDefault(output)

    basepath = Files.getResultsSherbrookePath("casinotools.cfg", "Simulations\water")

    label = {"WaterAuTop_wSE": "Top w SE"}
    analyze = TransmittedElectrons(output, label)
    filename = "C_00mrad_1um_wSE.cas"
    filepath = os.path.join(basepath, filename)
    analyze._readFile(filepath)

    result = analyze._results.values()[0]
    angles = result.getTransmittedElectronsAngles()[0]
    logging.info("Nunber angles: %i", len(angles))
    logging.info("Min: %f", np.min(angles))
    logging.info("Max: %f", np.max(angles))
    logging.info("Mean: %f", np.mean(angles))

    plt.hist(angles, bins=1000)
    plt.xlim(xmax=0.175)
    #analyze.doAnalysis()

    angles = np.array(angles)
    histogram, binEdges = np.histogram(angles, bins=1000)
    #weights = 1.0/(np.sin(angles)*len(angles))
    #histogram, binEdges = np.histogram(angles, bins=10, normed=True, weights=weights)

    x = []
    for i in range(len(binEdges)-1):
        x.append(binEdges[i] + (binEdges[i+1] - binEdges[i])/2.0)

    y = [h/(np.sin(xx)*len(angles)) for xx,h in zip(x, histogram)]
    plt.figure()
    plt.plot(x, y)

    if output == Graphics.DISPLAY:
        plt.show()

if __name__ == '__main__':    #pragma: no cover
    run()
