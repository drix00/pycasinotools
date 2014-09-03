#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.
import logging
import os.path
import math
import csv

# Third party modules.
import Image

# Local modules.
from casinotools.analysis.casino3.simulation import AnalyzeCasinoSimulation
import casinotools.scripting.casino3.SimulationParameters as SimulationParameters
import casinotools.fileformat.casino3.ScanPointsFile.ScanPointsFile as ScanPointsFile
import casinotools.fileformat.casino3.File as CasinoFile
from casinotools.analysis.casino3.transmitted_electrons import Result
from casinotools.utilities.path import create_path

# Project modules
import _parameters

# Globals and constants variables.

class _AnalyzeCasinoSimulation(AnalyzeCasinoSimulation):
    def getAnalysisName(self):
        return "DataSetBatenburg"

    def createScanPointsFiles(self):
        logging.info("createScanPointsFiles")

        self._createScanPointsFilesLinescans()
        self._createScanPointsFilesImageBatenburg()

    def _createScanPointsFilesLinescans(self):
        logging.info("_createScanPointsFilesLinescans")
        width_nm = 520.0
        spacings_nm = [1, 2, 4]
        numberPointsList = [int((width_nm)/s) for s in spacings_nm]

        for numberPoints in numberPointsList:
            for linescanPositionY_nm in self._linescanPositionsY_nm:
                scanPointsFile = ScanPointsFile.ScanPointsFileScript()
                scanPointsFile.setNumberPoints(numberPoints)
                scanPointsFile.setWidth_nm(width_nm)
                scanPointsFile.setHeight_nm(0.0)
                scanPointsFile.setCenterPoint((0.0, linescanPositionY_nm, 0.0))

                scanPointsFilename = "ScanPointsScript_X_y%inm_%inm_%ipts.txt" % (int(linescanPositionY_nm), int(width_nm), int(numberPoints))
                scanPointsFilepath = os.path.join(self.getInputPath(), scanPointsFilename)
                scanPointsFile.write(scanPointsFilepath)

    def _createScanPointsFilesImageBatenburg(self):
        logging.info("_createScanPointsFilesImageBatenburg")
        width_nm = 520.0
        height_nm = 50.0
        spacings_nm = [1, 2]
        numberPointsList = [int((width_nm*height_nm)/s) for s in spacings_nm]

        for numberPoints in numberPointsList:
            scanPointsFile = ScanPointsFile.ScanPointsFileScript()
            scanPointsFile.setNumberPoints(numberPoints)
            scanPointsFile.setWidth_nm(width_nm)
            scanPointsFile.setHeight_nm(height_nm)
            scanPointsFile.setCenterPoint((0.0, 0.0, 0.0))

            scanPointsFilename = "ScanPointsScript_XY_w%inm_h%inm_%ipts.txt" % (int(width_nm), int(height_nm), int(numberPoints))
            scanPointsFilepath = os.path.join(self.getInputPath(), scanPointsFilename)
            scanPointsFile.write(scanPointsFilepath)

    def createScripts(self):
        logging.info("createScripts")

        self._createScriptsImages()

    def _createScriptsImages(self):
        logging.info("_createScriptsImages")

        energies_keV = [200.0]
        beamDiameters_nm = [1]
        semiAngles_mrad = [2.0]
        numberElectronsList = [50000]

        basename = self.getAnalysisName()
        simulationParameters = SimulationParameters.SimulationParameters()
        simulationParameters.setBasename(basename)
        simulationParameters.setEnergies(energies_keV)
        simulationParameters.setNumberElectrons(numberElectronsList)
        simulationParameters.setSemiAngles_mrad(semiAngles_mrad)
        simulationParameters.setBeamDiameters_nm(beamDiameters_nm)

        simulationFilenames = []
        for filename in self.getAllSimulationFilenames():
            if filename.startswith("DataSetBatenburg_GoldinCarbon_Center_X"):
                simulationFilenames.append(filename)

        simulationParameters.setFilenames(simulationFilenames)
        scanPointFile = "ScanPointsScript_XY_w520nm_h50nm_13000pts.txt"
        scanPointFilepath = os.path.join(self.getInputPath(), scanPointFile)
        scanPointFiles = [scanPointFilepath]
        simulationParameters.setScanPointFiles(scanPointFiles)

        self._createScripts(basename, simulationParameters)

    def readAllResults(self):
        logging.info("readAllResults")

        self._resultFilepaths = []

        self._useSerialization = False
        self._readAllResults()
        self._simulationResultsList = None

    def _generateSerializationFilename(self):
        serializationFilename = self.getAnalysisName()
        serializationFilename += "_%s" % (self._detectorType)
        serializationFilename += ".ser"
        return serializationFilename

    def doAnalyze(self, output):
        logging.info("doAnalyze")

        self._output = output

        self._resultFilepaths = []
        self._useSerialization = True

        serializationFilename = self._generateSerializationFilename()
        self._readAllResults(serializationFilename)

        graphicPath = os.path.join(self.getSimulationPath(), "Graphics", "Analyze")

        graphicPath = create_path(graphicPath)

        imageList = {}
        parametersList = self.getParametersList()
        for parameters in parametersList:
            tilt_deg, imageFilepath = self.createImages(parameters, graphicPath)

            if tilt_deg is not None:
                imageList[tilt_deg] = imageFilepath

        outputFilepath = os.path.join(self._imagePath, "ImageList.txt")
        outputFile = open(outputFilepath, "wb")

        for tilt_deg in sorted(imageList.keys()):
            outputFile.write(imageList[tilt_deg]+"\n")

        outputFile.close()

    def _extractParametersFromFilepath(self, filepath):
        parameters = _parameters.Parameters(filepath)
        return parameters

    def _readResults(self, filepath):
        casinoFile = CasinoFile.File(filepath)
        result = Result()
        result.setSimulations(casinoFile.getSimulations())

        positions = result.getPositions()
        betaMin_mrad = self._betaMin_mrad
        betaMax_mrad = self._betaMax_mrad
        y = result.getDetectedTransmittedElectrons(betaMin_mrad, betaMax_mrad)

        return (positions, y)

    def createImages(self, parameters, graphicPath):
        if parameters[parameters.KEY_LINESCAN_NUMBER_POINTS] == "13000":
            tilt_deg = float(parameters[parameters.KEY_TILT_Y])
            basename = self.getAnalysisName() + "_tilt%+05.1f" % (tilt_deg)
            logging.info(basename)

            positions, intensity = self.getResults(parameters)

            xList = set()
            yList = set()

            for x, y, z in positions:
                assert z == 0.0
                xList.add(x)
                yList.add(y)

            assert len(xList) == 368, len(xList)
            assert len(yList) == 36, len(yList)

            imagePath = os.path.join(self._imagePath, "data")
            imagePath = create_path(imagePath)

            dataFilepath = os.path.join(imagePath, basename)
            dataFilepath += '.csv'

            imageFilepath = os.path.join(imagePath, basename)
            imageFilepath += '.tiff'

            size = (len(xList), len(yList))
            image = Image.new('F', size)

            pix = image.load()

            z = 0.0
            rows = []
            for indexH, x in enumerate(sorted(xList)):
                for indexV, y in enumerate(sorted(yList)):
                    position = (x, y, z)
                    index = positions.index(position)
                    value = intensity[index]
                    pix[indexH, indexV] = value

                    row = [x, y, value]
                    rows.append(row)
            image.save(imageFilepath)

            writer = csv.writer(open(dataFilepath, 'wb'))

            row = ["X (nm)", "Y (nm)", "NumberElectron"]
            writer.writerow(row)
            writer.writerows(rows)

            return tilt_deg, imageFilepath

        return None, ""

    def computeNewPositions(self):
        xPositions = ['L', 'C', 'R']
        zPositions = ["-250", "-150", "-50", "50", "150", "250"]

        nanoparticles = {}

        nanoparticles[('L', "-250")] = (-20, -250.0)
        nanoparticles[('C', "-250")] = (0, -250.0)
        nanoparticles[('R', "-250")] = (20, -250.0)

        nanoparticles[('L', "-150")] = (-20, -150.0)
        nanoparticles[('C', "-150")] = (0, -150.0)
        nanoparticles[('R', "-150")] = (20, -150.0)

        nanoparticles[('L', "-50")] = (-20, -50.0)
        nanoparticles[('C', "-50")] = (0, -50.0)
        nanoparticles[('R', "-50")] = (20, -50.0)

        nanoparticles[('L', "50")] = (-20, 50.0)
        nanoparticles[('C', "50")] = (0, 50.0)
        nanoparticles[('R', "50")] = (20, 50.0)

        nanoparticles[('L', "150")] = (-20, 150.0)
        nanoparticles[('C', "150")] = (0, 150.0)
        nanoparticles[('R', "150")] = (20, 150.0)

        nanoparticles[('L', "250")] = (-20, 250.0)
        nanoparticles[('C', "250")] = (0, 250.0)
        nanoparticles[('R', "250")] = (20, 250.0)

        tiltAngles_deg = [-70.0, -20.0, 0.0, 20.0, 70.0]

        print "%6s\t%4s\t%7s\t%7s\t%7s" % ("Tilt", "Z", "L", "C", "R")

        for tiltAngle_deg in tiltAngles_deg:
            for zPosition in zPositions:
                xList = []
                for xPosition in xPositions:
                    key = (xPosition, zPosition)
                    x, y = nanoparticles[key]
                    x, y = self._rotation(x, y, tiltAngle_deg)
                    xList.append(x)
                print "%4i\t%4s\t%7.2f\t%7.2f\t%7.2f" % (tiltAngle_deg, zPosition, xList[0], xList[1], xList[2])

    def _rotation(self, x, y, tiltAngle_deg):
        angle_rad = math.radians(tiltAngle_deg)
        newX = x*math.cos(angle_rad) - y*math.sin(angle_rad)
        newY = x*math.sin(angle_rad) + y*math.cos(angle_rad)

        return newX, newY

    def getImagePath(self):
        #configurationFilepath = Files.getCurrentModulePath(__file__, "../../pyUdeS.cfg")
        #labBookPath = Files.getUdeSPath(configurationFilepath, 'documents/labBook')
        #imagePath = os.path.join(labBookPath, 'graphics', self.getAnalysisName(), self._detectorType)
        imagePath = os.path.join(self.getSimulationPath(), 'graphics', self._detectorType)
        imagePath = create_path(imagePath)

        return imagePath

class SimulationDiscreteTomographyDarkField(_AnalyzeCasinoSimulation):
    def _initData(self):
        self._scanPointsFilenames = []
        self._linescanPositionsY_nm = [-20, 0, 20]

        self._detectorType = "DF"
        self._betaMin_mrad = 40
        self._betaMax_mrad = 200

        self._imagePath = self.getImagePath()

class SimulationDiscreteTomographyBrightField(_AnalyzeCasinoSimulation):
    def _initData(self):
        self._scanPointsFilenames = []
        self._linescanPositionsY_nm = [-20, 0, 20]

        self._detectorType = "BF"
        self._betaMin_mrad = 0.0
        self._betaMax_mrad = 15.0

        self._imagePath = self.getImagePath()
