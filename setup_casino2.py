#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.
from setuptools import setup

# Local modules.

# Globals and constants variables.

setup(name="casinoTools-Casino2",
      version='0.1',
      url='http://www.gel.usherbrooke.ca/casino',
      description="Python interface to read and write Casino 2 files",
      author="Hendrix Demers",
      author_email="hendrix.demers@mail.mcgill.ca",
      license="GPL v3",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Physics'],

      packages=['casinotools.fileformat.casino2'],
      py_modules=['casinoTools.__init__',
                  'casinotools.fileformat.__init__',
                  'casinotools.fileformat.XrayRadial',
                  'casinotools.fileformat.casino3.FileReaderWriterTools',
                  'casinotools.fileformat.casino3.Tags'],
      package_dir={'casinoTools': '.'},
)

