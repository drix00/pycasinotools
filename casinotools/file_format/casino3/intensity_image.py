#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.intensity_image
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
"""

###############################################################################
# Copyright 2020 Hendrix Demers
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
from PIL import Image

# Local modules.

# Project modules.
from casinotools.file_format.casino3.file import File
from casinotools.file_format.casino3.scan_point_results import ScanPointResults

# Globals and constants variables.
INTENSITY_TRANSMITTED = "TransmittedIntensity"
INTENSITY_TRANSMITTED_DETECTED = "TransmittedDetectedIntensity"


class IntensityImage(object):
    def __init__(self, filepath, image_name="IntensityImage", intensity_type=INTENSITY_TRANSMITTED_DETECTED):
        self._filepath = filepath
        self._image_name = image_name
        self._intensity_type = intensity_type

        self._image_size = (800, 600)
        self._create_get_intensity_method()

    def _create_get_intensity_method(self):
        if self._intensity_type == INTENSITY_TRANSMITTED:
            self._getIntensity = ScanPointResults.get_transmitted_coefficient
        elif self._intensity_type == INTENSITY_TRANSMITTED_DETECTED:
            self._getIntensity = ScanPointResults.get_transmitted_detected_coefficient

    def _create_image(self):
        self._extract_data()
        self._analyze_positions()
        self._create_raw_image2()

    def _extract_data(self):
        casino_file = File(self._filepath)
        casino_file.open()

        assert 1 == casino_file.get_number_simulations()

        scan_points_results = casino_file.get_scan_point_results()
        self._number_scan_points = len(scan_points_results)

        self._positions = []
        self._intensities = {}
        for scan_point_results in scan_points_results:
            position = scan_point_results.get_position()
            self._positions.append(position)
            self._intensities[position] = self._getIntensity(scan_point_results)

    def _analyze_positions(self):
        self._xSet = set()
        self._ySet = set()
        self._zSet = set()

        for position in self._positions:
            x, y, z = position
            self._xSet.add(x)
            self._ySet.add(y)
            self._zSet.add(z)

        number_unique_x = len(self._xSet)
        number_unique_y = len(self._ySet)
        number_unique_z = len(self._zSet)

        if number_unique_x > 1:
            if number_unique_y > 1:
                if number_unique_z > 1:
                    image_type = "3D"
                else:
                    image_type = "XY"
            elif number_unique_z > 1:
                image_type = "XZ"
            else:
                image_type = "X"
        elif number_unique_y > 1:
            if number_unique_z > 1:
                image_type = "YZ"
            else:
                image_type = "Y"
        elif number_unique_z > 1:
            image_type = "z"
        else:
            image_type = "P"

        self._imageType = image_type

        logging.info("Number unique X: %i", len(self._xSet))
        logging.info("Number unique Y: %i", len(self._ySet))
        logging.info("Number unique z: %i", len(self._zSet))
        logging.info("Image shape_type: %s", image_type)

    def _create_raw_image(self):
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

    def _create_raw_image2(self):
        if self._imageType == "XY":
            size = len(self._xSet), len(self._ySet)
            self._imageRaw = Image.new("F", size, color="black")

            z = list(self._zSet)[0]
            pix = self._imageRaw.load()

            for indexH, x in enumerate(sorted(self._xSet)):
                for indexV, y in enumerate(sorted(self._ySet)):
                    position = (x, y, z)
                    # index = positions.index(position)
                    value = self._intensities[position]
                    pix[indexH, indexV] = value

    def save(self, path):
        self._save_raw_image(path)
        # self._save_image(path)

    def _save_raw_image(self, path):
        image_filepath = os.path.join(path, self._image_name + "_raw.tiff")
        self._imageRaw.save(image_filepath)

    def _save_image(self, path):
        size = self._imageRaw.size
        zoom_factor = self._compute_zoom_factor(size)
        new_size = size[0] * zoom_factor, size[1] * zoom_factor

        filters = {"near": Image.NEAREST, "bilin": Image.BILINEAR, "bicub": Image.BICUBIC, "anti": Image.ANTIALIAS}
        for name, image_filter in filters.items():
            image_filepath = os.path.join(path, self._image_name + "_" + name + ".tiff")
            image = self._imageRaw.resize(new_size, image_filter)
            image.save(image_filepath)

        image_filepath = os.path.join(path, self._image_name + ".tiff")
        tmp_image = self._imageRaw.resize(new_size, Image.BICUBIC)
        # tmp_image = tmp_image.convert('L')
        image = Image.new(tmp_image.mode, self._image_size)
        top_corner = (self._image_size[0] - tmp_image.size[0]) / 2, (self._image_size[1] - tmp_image.size[1]) / 2
        box = top_corner[0], top_corner[1], top_corner[0] + tmp_image.size[0], top_corner[1] + tmp_image.size[1]
        image.paste(tmp_image, box)
        image.save(image_filepath)
        # tmp_image.save(image_filepath)

    def _compute_zoom_factor(self, size):
        x_zoom = int(self._image_size[0] / size[0])
        y_zoom = int(self._image_size[1] / size[1])

        zoom = min(x_zoom, y_zoom)
        return zoom


def run():
    from pkg_resources import resource_filename  # @UnresolvedImport

    results_path = resource_filename(__name__, "../../test_data/casino3.x/create_image")
    cas_binned_filepath = os.path.join(results_path, "Au_C_thin_1nm_Inside_100ke_binned.cas")

    image_binned = IntensityImage(cas_binned_filepath)
    image_binned._create_image()

    image_binned.save(results_path)


if __name__ == '__main__':
    run()
