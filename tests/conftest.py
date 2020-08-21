#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.conftest
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

A Pytest local plugin for testing the project.
"""

# Standard library modules.

# Third party modules.
import pytest

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


# Test data.
