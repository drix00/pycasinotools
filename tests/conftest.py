#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.conftest
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

A Pytest local plugin for testing the project.
"""

# Standard library modules.
import os
import shutil

# Third party modules.
import pytest
from pkg_resources import resource_filename

# Local modules.

# Project modules.
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.


# pytest options.
def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):  # pragma no cover
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


# Test files.
@pytest.fixture()
def filepath_sim_2_45():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.4.6.1/id475_v2.46.sim")
    return file_path


@pytest.fixture()
def filepath_cas_2_45():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.4.6.1/id475_v2.46.cas")
    return file_path


@pytest.fixture()
def filepath_sim_26():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v26/id475_v26.sim")
    return file_path


@pytest.fixture()
def filepath_cas_26():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v26/id475_v26.cas")
    return file_path


@pytest.fixture()
def filepath_std():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.0.0/std_B_04.0keV_40.0TOA_v2.42.sim")
    return file_path


@pytest.fixture()
def filepath_write():
    file_path = resource_filename(__name__, "../test_data/casino2.x/stdTest.sim")

    yield file_path

    if os.path.isfile(file_path):
        os.remove(file_path)


@pytest.fixture()
def filepath_sim_v242():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v23/std_B_3keV_v2.42.sim")
    return file_path


@pytest.fixture()
def filepath_cas_v242():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v23/std_B_3keV_v2.42.cas")
    return file_path


@pytest.fixture()
def filepath_cas_nicr():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.4.6.1/nicr_v2.46.cas")
    return file_path


@pytest.fixture()
def filepath_sim_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.0.0/Al_E2kV_10ke_v2.50.sim")
    return file_path


@pytest.fixture()
def filepath_cas_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.0.0/Al_E2kV_10ke_v2.50.cas")
    return file_path


@pytest.fixture()
def filepath_sim_v251():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.1.0/Al_E2kV_10ke_v2.51.sim")
    return file_path


@pytest.fixture()
def filepath_cas_v251():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.1.0/Al_E2kV_10ke_v2.51.cas")
    return file_path


@pytest.fixture()
def filepath_problem_sim_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.0.0/VerticalLayers3_v2.50.sim")
    return file_path


@pytest.fixture()
def filepath_problem_pymontecarlo_sim_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.0.0/VerticalLayers3_pymontecarlo_v2.50.sim")
    return file_path


@pytest.fixture()
def filepath_good_sim_v251():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.1.0/VerticalLayers3_good_v2.51.sim")
    return file_path


@pytest.fixture()
def filepath_sim():
    file_path = resource_filename(__name__, "../test_data/casino3.x/v3.1/v3.1.7.2/SiSubstrateThreeLines_Points.sim")
    return file_path


@pytest.fixture()
def filepath_sim_3202():
    name = "../test_data/casino3.x/v3.2/v3.2.0.2/SiSubstrateThreeLines_Points_3202.sim"
    file_path = resource_filename(__name__, name)
    return file_path


@pytest.fixture()
def filepath_cas():
    file_path = resource_filename(__name__, "../test_data/casino3.x/v3.1/v3.1.7.2/SiSubstrateThreeLines_Points_1Me.cas")
    return file_path


@pytest.fixture()
def filepath_sim_2_5_1_0():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.1.0/C_15kV_2_5_1_0.sim")
    return file_path


@pytest.fixture()
def filepath_cas_2_5_1_0():
    file_path = resource_filename(__name__, "../test_data/casino2.x/v2.5.1.0/C_15kV_2_5_1_0.cas")
    return file_path


@pytest.fixture()
def file_path_energy_cartesian_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cartesian_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cylindrical_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cylindrical_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_spherical_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_spherical_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_no_deposited_energy_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/no_energy_deposition_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cartesian_dat():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cartesian_v3.3.0.4_Energy_by_position.dat"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cylindrical_dat():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cylindrical_v3.3.0.4_Energy_by_position.dat"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_spherical_dat():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_spherical_v3.3.0.4_Energy_by_position.dat"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cartesian_log_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cartesian_log_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cylindrical_log_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cylindrical_log_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_spherical_log_cas():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_spherical_log_v3.3.0.4.cas"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cartesian_log_dat():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cartesian_log_v3.3.0.4_Energy_by_position.dat"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_cylindrical_log_dat():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_cylindrical_log_v3.3.0.4_Energy_by_position.dat"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_energy_spherical_log_dat():
    name = "../test_data/casino3.x/v3.3/v3.3.0.4/energy_deposition_spherical_log_v3.3.0.4_Energy_by_position.dat"
    file_path = resource_filename(__name__, name)
    if is_bad_file(file_path):
        pytest.skip()
    return file_path


@pytest.fixture()
def file_path_sim_tmp_modify_option(tmpdir):
    file_path = resource_filename(__name__, "../test_data/casino3.x/v3.3/v3.3.0.4/03_1kV_1Me.sim")
    if is_bad_file(file_path):
        pytest.skip()

    in_file_path = file_path
    out_file_path = tmpdir.join("03_3.5kV_1Me.sim")
    shutil.copy(in_file_path, out_file_path)
    return out_file_path


# Test data.
