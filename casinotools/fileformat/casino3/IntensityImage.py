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
from PIL import Image

# Local modules.
import casinotools.fileformat.casino3.File as File
import casinotools.fileformat.casino3.ScanPointResults as ScanPointResults

# Globals and constants variables.
INTENSITY_TRANSMITTED = "TransmittedIntensity"
INTENSITY_TRANSMITTED_DETECTED = "TransmittedDetectedIntensity"

class IntensityImage(object):
    def __init__(self, filepath, imageName="IntensityImage", intensityType=INTENSITY_TRANSMITTED_DETECTED):
        self._filepath = filepath
        self._imageName = imageName
        self._intensityType = intensityType

        self._imageSize = (800, 600)
        self._createGetIntensityMethod()

    def _createGetIntensityMethod(self):
        if self._intensityType == INTENSITY_TRANSMITTED:
            self._getIntensity = ScanPointResults.ScanPointResults.getTransmittedCoefficient
        elif self._intensityType == INTENSITY_TRANSMITTED_DETECTED:
            self._getIntensity = ScanPointResults.ScanPointResults.getTransmittedDetectedCoefficient

    def _createImage(self):
        self._extractData()
        self._analyzePositions()
        self._createRawImage2()

    def _extractData(self):
        casinoFile = File.File(self._filepath)
        casinoFile.open()

        assert 1 == casinoFile.getNumberSimulations()

        scanPointsResults = casinoFile.getScanPointResults()
        self._numberScanPoints = len(scanPointsResults)

        self._positions = []
        self._intensities = {}
        for scanPointResults in scanPointsResults:
            position = scanPointResults.getPosition()
            self._positions.append(position)
            self._intensities[position] = self._getIntensity(scanPointResults)

    def _analyzePositions(self):
        self._xSet = set()
        self._ySet = set()
        self._zSet = set()

        for position in self._positions:
            x, y, z = position
            self._xSet.add(x)
            self._ySet.add(y)
            self._zSet.add(z)

        numberUniqueX = len(self._xSet)
        numberUniqueY = len(self._ySet)
        numberUniqueZ = len(self._zSet)

        imageType = None
        if numberUniqueX > 1:
            if numberUniqueY > 1:
                if numberUniqueZ > 1:
                    imageType = "3D"
                else:
                    imageType = "XY"
            elif numberUniqueZ > 1:
                imageType = "XZ"
            else:
                imageType = "X"
        elif numberUniqueY > 1:
            if numberUniqueZ > 1:
                imageType = "YZ"
            else:
                imageType = "Y"
        elif numberUniqueZ > 1:
            imageType = "Z"
        else:
            imageType = "P"

        self._imageType = imageType

        logging.info("Number unique X: %i", len(self._xSet))
        logging.info("Number unique Y: %i", len(self._ySet))
        logging.info("Number unique Z: %i", len(self._zSet))
        logging.info("Image type: %s", imageType)

    def _createRawImage(self):
        if self._imageType == "XY":
            size = len(self._xSet), len(self._ySet)
            self._imageRaw = Image.new("F", size, color="black")
            z = list(self._zSet)[0]
            data = []
            for y in sorted(self._xSet):
                for x in sorted(self._ySet):
                    position = x, y, z
                    intensity = self._intensities[position]
                    data.append(intensity)

            self._imageRaw.putdata(data)

    def _createRawImage2(self):
        if self._imageType == "XY":
            size = len(self._xSet), len(self._ySet)
            self._imageRaw = Image.new("F", size, color="black")

            z = list(self._zSet)[0]
            pix = self._imageRaw.load()

            for indexH, x in enumerate(sorted(self._xSet)):
                for indexV, y in enumerate(sorted(self._ySet)):
                    position = (x, y, z)
                    #index = positions.index(position)
                    value = self._intensities[position]
                    pix[indexH, indexV] = value

    def save(self, path):
        self._saveRawImage(path)
        #self._saveImage(path)

    def _saveRawImage(self, path):
        imageFilepath = os.path.join(path, self._imageName + "_raw.tiff")
        self._imageRaw.save(imageFilepath)

    def _saveImage(self, path):
        size = self._imageRaw.size
        zoomFactor = self._computeZoomFactor(size)
        newSize = size[0] * zoomFactor, size[1] * zoomFactor

        filters = {"near": Image.NEAREST, "bilin": Image.BILINEAR,
                             "bicub": Image.BICUBIC, "anti": Image.ANTIALIAS}
        for name, filter in filters.items():
            imageFilepath = os.path.join(path, self._imageName + "_" + name + ".tiff")
            image = self._imageRaw.resize(newSize, filter)
            image.save(imageFilepath)

        imageFilepath = os.path.join(path, self._imageName + ".tiff")
        tmpImage = self._imageRaw.resize(newSize, Image.BICUBIC)
        #tmpImage = tmpImage.convert('L')
        image = Image.new(tmpImage.mode, self._imageSize)
        topCorner = (self._imageSize[0] - tmpImage.size[0]) / 2, (self._imageSize[1] - tmpImage.size[1]) / 2
        box = topCorner[0], topCorner[1], topCorner[0] + tmpImage.size[0], topCorner[1] + tmpImage.size[1]
        image.paste(tmpImage, box)
        image.save(imageFilepath)
        #tmpImage.save(imageFilepath)

    def _computeZoomFactor(self, size):
        xZoom = int(self._imageSize[0] / size[0])
        yZoom = int(self._imageSize[1] / size[1])

        zoom = min(xZoom, yZoom)
        return zoom

def run():
    from pkg_resources import resource_filename #@UnresolvedImport

    resultsPath = resource_filename(__name__, "../../test_data/casino3.x/createImage")
    casBinnedFilepath = os.path.join(resultsPath, "Au_C_thin_1nm_Inside_100ke_binned.cas")

    imageBinned = IntensityImage(casBinnedFilepath)
    imageBinned._createImage()

    imageBinned.save(resultsPath)

if __name__ == '__main__':
    run()