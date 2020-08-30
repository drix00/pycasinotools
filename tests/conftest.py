#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.conftest
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

A Pytest local plugin for testing the project.
"""

# Standard library modules.
import os

# Third party modules.
import pytest
from pkg_resources import resource_filename

# Local modules.

# Project modules.

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
    file_path = resource_filename(__name__, "../test_data/wincasino2.45/id475_v2.46.sim")
    return file_path


@pytest.fixture()
def filepath_cas_2_45():
    file_path = resource_filename(__name__, "../test_data/wincasino2.45/id475_v2.46.cas")
    return file_path


@pytest.fixture()
def filepath_std():
    file_path = resource_filename(__name__, "../test_data/casino2.x/std_B_04.0keV_40.0TOA_v2.42.sim")
    return file_path


@pytest.fixture()
def filepath_write():
    file_path = resource_filename(__name__, "../test_data/casino2.x/stdTest.sim")

    yield file_path

    if os.path.isfile(file_path):
        os.remove(file_path)


@pytest.fixture()
def filepath_sim_v242():
    file_path = resource_filename(__name__, "../test_data/casino2.x/std_B_3keV_v2.42.sim")
    return file_path


@pytest.fixture()
def filepath_cas_v242():
    file_path = resource_filename(__name__, "../test_data/casino2.x/std_B_3keV_v2.42.cas")
    return file_path


@pytest.fixture()
def filepath_cas_nicr():
    file_path = resource_filename(__name__, "../test_data/casino2.x/nicr_v2.46.cas")
    return file_path


@pytest.fixture()
def filepath_sim_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/Al_E2kV_10ke_v2.50.sim")
    return file_path


@pytest.fixture()
def filepath_cas_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/Al_E2kV_10ke_v2.50.cas")
    return file_path


@pytest.fixture()
def filepath_sim_v251():
    file_path = resource_filename(__name__, "../test_data/casino2.x/Al_E2kV_10ke_v2.51.sim")
    return file_path


@pytest.fixture()
def filepath_cas_v251():
    file_path = resource_filename(__name__, "../test_data/casino2.x/Al_E2kV_10ke_v2.51.cas")
    return file_path


@pytest.fixture()
def filepath_problem_sim_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/VerticalLayers3_v2.50.sim")
    return file_path


@pytest.fixture()
def filepath_problem_pymontecarlo_sim_v250():
    file_path = resource_filename(__name__, "../test_data/casino2.x/VerticalLayers3_pymontecarlo_v2.50.sim")
    return file_path


@pytest.fixture()
def filepath_good_sim_v251():
    file_path = resource_filename(__name__, "../test_data/casino2.x/VerticalLayers3_good_v2.51.sim")
    return file_path


@pytest.fixture()
def filepath_sim():
    file_path = resource_filename(__name__, "../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
    return file_path


@pytest.fixture()
def filepath_sim_3202():
    file_path = resource_filename(__name__, "../test_data/casino3.x/SiSubstrateThreeLines_Points_3202.sim")
    return file_path


@pytest.fixture()
def filepath_cas():
    file_path = resource_filename(__name__, "../test_data/casino3.x/SiSubstrateThreeLines_Points_1Me.cas")
    return file_path


# Test data.
