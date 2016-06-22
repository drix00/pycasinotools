#!/usr/bin/env python
"""
.. py:currentmodule:: casinotools.fileformat.casino4.file
   :synopsis: Module to read, modify, or create CASINO v4 file.
   
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Module to read, modify, or create CASINO v4 file.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = "0.1"
__date__ = "Jun 14, 2016"
__copyright__ = "Copyright (c) 2016 Hendrix Demers"
__license__ = "Apache License Version 2"

# Standard library modules.
import os.path

# Third party modules.
import h5py

# Local modules.

# Project modules
from casinotools.utilities.path import create_path, get_current_module_path
from casinotools.fileformat.casino4.version import CURRENT_VERSION

# Globals and constants variables.

class File():
    def __init__(self, filepath):
        self.filepath = filepath
        
        self.set_default_values()
        
    def set_default_values(self):
        self.version = CURRENT_VERSION
        
    def save(self, overwrite=False):
        if overwrite:
            hdf5_file = h5py.File(self.filepath, 'w')
        else:
            hdf5_file = h5py.File(self.filepath, 'a')
        
        self.version.write(hdf5_file)
        
        hdf5_file.close()
        
    def open(self, modify=False):
        if modify:
            hdf5_file = h5py.File(self.filepath, 'r+')
        else:
            hdf5_file = h5py.File(self.filepath, 'r')
        
        self.version.read(hdf5_file)
        
        hdf5_file.close()

def create_sim_v4_0_0():
    """
    Create CASINO simulation file version 4.0.0 using python script.
    """
    from casinotools.fileformat.casino4.version import VERSION_4_0_0
    
    path = get_current_module_path(__file__, "../../../test_data/casino4/py")
    path = create_path(path)
    filepath = os.path.join(path, "version_4_0_0_py.sim.hdf5")
    
    casino_file = File(filepath)
    casino_file.version = VERSION_4_0_0
    casino_file.save(overwrite=True)
    
if __name__ == '__main__': #pragma: no cover
    create_sim_v4_0_0()