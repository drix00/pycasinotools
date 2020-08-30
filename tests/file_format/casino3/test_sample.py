#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.file_format.casino3.test_sample
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`casinotools.file_format.casino3.sample` module.
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
import os.path
import shutil

# Third party modules.
import pytest

# Local modules.

# Project modules.
from casinotools.file_format.casino3.sample import Sample
from casinotools.file_format.casino3.sample_object_factory import SHAPE_BOX
from casinotools.file_format.casino3.file import File
from casinotools.utilities.path import get_current_module_path
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(filepath_sim):
    if is_bad_file(filepath_sim):
        pytest.skip()
    file = open(filepath_sim, "rb")
    file.seek(55)
    sample = Sample()
    sample.read(file)

    assert sample._version == 30107002
    assert sample._useSubstrate == 0

    assert sample._count == 4

    box_shape = sample._sample_objects[0]

    assert box_shape._shape_type == SHAPE_BOX
    assert box_shape._version == 30105004
    assert box_shape._name == "Box_0"
    assert box_shape._region_name == "Undefined"
    assert box_shape._translation == (0.0, 0.0, 5000.0)
    assert box_shape._rotation == (0.0, 0.0, 0.0)
    assert box_shape._scale == (10000.0, 10000.0, 10000.0)
    assert box_shape._color == (0.984375, 0.0, 0.0)

    assert sample._maxSampleTreeLevel == 20


def test_read3202(filepath_sim_3202):
    if is_bad_file(filepath_sim_3202):
        pytest.skip()
    file = open(filepath_sim_3202, "rb")
    file.seek(55)
    sample = Sample()
    sample.read(file)

    assert sample._version == 30200002
    assert sample._useSubstrate == 0

    assert sample._count == 4

    box_shape = sample._sample_objects[0]

    assert box_shape._shape_type == SHAPE_BOX
    assert box_shape._version == 30105004
    assert box_shape._name == "Box_0"
    assert box_shape._region_name == "Undefined"
    assert box_shape._translation == (0.0, 0.0, 5000.0)
    assert box_shape._rotation == (0.0, 0.0, 0.0)
    assert box_shape._scale == (10000.0, 10000.0, 10000.0)
    assert box_shape._color == (0.984375, 0.0, 0.0)

    assert sample._maxSampleTreeLevel == 20


def test_get_rotation_yz_deg():
    test_data_path = get_current_module_path(__file__, "../../../test_data")

    filepath_sim = os.path.join(test_data_path, "casino3.x/NoRotationY.sim")
    if is_bad_file(filepath_sim):
        pytest.skip()

    casino_file = open(filepath_sim, "rb")
    casino_file.seek(55)
    sample = Sample()
    sample.read(casino_file)

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(0.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(0.0)

    filepath_sim = os.path.join(test_data_path, "casino3.x/RotationY10.sim")
    if is_bad_file(filepath_sim):
        pytest.skip()

    casino_file = open(filepath_sim, "rb")
    casino_file.seek(55)
    sample = Sample()
    sample.read(casino_file)

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(10.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(0.0)

    filepath_sim = os.path.join(test_data_path, "casino3.x/RotationZ15.sim")
    if is_bad_file(filepath_sim):
        pytest.skip()

    casino_file = open(filepath_sim, "rb")
    casino_file.seek(55)
    sample = Sample()
    sample.read(casino_file)

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(0.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(15.0)

    filepath_sim = os.path.join(test_data_path, "casino3.x/RotationY20Z35.sim")
    if is_bad_file(filepath_sim):
        pytest.skip()

    casino_file = open(filepath_sim, "rb")
    casino_file.seek(55)
    sample = Sample()
    sample.read(casino_file)

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(20.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(35.0)


def test_modify_rotation_yz_deg(tmpdir):
    test_data_path = get_current_module_path(__file__, "../../../test_data")
    source_filepath = os.path.join(test_data_path, "casino3.x/NoRotationY.sim")
    if is_bad_file(source_filepath):
        pytest.skip()

    rotation_y_ref_deg = 10.0
    filename = "RotationY10.sim"
    destination_filepath = os.path.join(tmpdir, filename)

    shutil.copy2(source_filepath, destination_filepath)

    casino_file = File(destination_filepath, is_modifiable=True)
    sample = casino_file.get_first_simulation().get_sample()

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(0.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(0.0)

    sample.modify_rotation_y_deg(rotation_y_ref_deg)
    del casino_file

    casino_file = File(destination_filepath, is_modifiable=False)
    sample = casino_file.get_first_simulation().get_sample()

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(rotation_y_ref_deg)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(0.0)

    del casino_file

    rotation_z_ref_deg = 15.0
    filename = "RotationZ15.sim"
    destination_filepath = os.path.join(tmpdir, filename)

    shutil.copy2(source_filepath, destination_filepath)

    casino_file = File(destination_filepath, is_modifiable=True)
    sample = casino_file.get_first_simulation().get_sample()

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(0.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(0.0)

    sample.modify_rotation_z_deg(rotation_z_ref_deg)
    del casino_file

    casino_file = File(destination_filepath, is_modifiable=False)
    sample = casino_file.get_first_simulation().get_sample()

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(0.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(rotation_z_ref_deg)

    del casino_file

    rotation_y_ref_deg = 20.0
    rotation_z_ref_deg = 35.0
    filename = "RotationY20Z35.sim"
    destination_filepath = os.path.join(tmpdir, filename)

    shutil.copy2(source_filepath, destination_filepath)

    casino_file = File(destination_filepath, is_modifiable=True)
    sample = casino_file.get_first_simulation().get_sample()

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(0.0)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(0.0)

    sample.modify_rotation_y_deg(rotation_y_ref_deg)
    sample.modify_rotation_z_deg(rotation_z_ref_deg)
    del casino_file

    casino_file = File(destination_filepath, is_modifiable=False)
    sample = casino_file.get_first_simulation().get_sample()

    rotation_y_deg = sample.get_rotation_y_deg()
    assert rotation_y_deg == pytest.approx(rotation_y_ref_deg)
    rotation_z_deg = sample.get_rotation_z_deg()
    assert rotation_z_deg == pytest.approx(rotation_z_ref_deg)

    del casino_file
