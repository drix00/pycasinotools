#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.fileformat.casino4.version
   :synopsis: Module to read, modify, or create CASINO v4 version number.
   
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

CASINO version information.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = "0.1"
__date__ = "Jun 22, 2016"
__copyright__ = "Copyright (c) 2016 Hendrix Demers"
__license__ = "Apache License Version 2"

# Standard library modules.
import copy

# Third party modules.

# Local modules.

# Project modules

# Globals and constants variables.
HDF5_VERSION = "version"
HDF5_MAJOR = "major"
HDF5_MINOR = "minor"
HDF5_REVISION = "revision"
HDF5_BUILD = "build"

class Version(object):
    key = "Version"

    def __init__(self, major, minor, revision, build=0):
        self.major = major
        self.minor = minor
        self.revision = revision
        self.build = build

    def to_string(self):
        text = "%s.%s.%s.%s" % (self.major, self.minor, self.revision, self.build)
        return text

    def from_string(self, versionString):
        items = versionString.split('.')
        self.major = items[0]
        self.minor = items[1]
        self.revision = items[2]
        if len(items) == 4:
            self.build = items[3]
        else:
            self.build = 0

    def __eq__(self, other):
        if self.major == other.major and self.minor == other.minor and self.revision == other.revision and self.build == other.build:
            return True
        else:
            return False

    def __lt__(self, other):
        if self == other:
            return False

        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False

        if self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False

        if self.revision < other.revision:
            return True
        elif self.revision > other.revision:
            return False

        if self.build < other.build:
            return True
        elif self.build > other.build:
            return False

    def __ge__(self, other):
        if self == other:
            return True
        if self < other:
            return False
        else:
            return True
    
    def write(self, hdf5_parent):
        group = hdf5_parent.require_group(HDF5_VERSION)
        group.attrs[HDF5_MAJOR] = self.major
        group.attrs[HDF5_MINOR] = self.minor
        group.attrs[HDF5_REVISION] = self.revision
        group.attrs[HDF5_BUILD] = self.build
        
    def read(self, hdf5_parent):
        group = hdf5_parent.require_group(HDF5_VERSION)
        self.major = group.attrs[HDF5_MAJOR]
        self.minor = group.attrs[HDF5_MINOR]
        self.revision = group.attrs[HDF5_REVISION]
        self.build = group.attrs[HDF5_BUILD]
        
    @property
    def major(self):
        return self._major
    @major.setter
    def major(self, major):
        self._major = int(major)

    @property
    def minor(self):
        return self._minor
    @minor.setter
    def minor(self, minor):
        self._minor = int(minor)

    @property
    def revision(self):
        return self._revision
    @revision.setter
    def revision(self, revision):
        self._revision = int(revision)

    @property
    def build(self):
        return self._build
    @build.setter
    def build(self, build):
        self._build = int(build)

VERSION_4_0_0 = Version(4, 0, 0)

CURRENT_VERSION = copy.deepcopy(VERSION_4_0_0)
