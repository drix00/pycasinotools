#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.

setup(name="pyCasinoTools",
      version='0.2',
      url='http://www.gel.usherbrooke.ca/casino',
      description="Python interface to read and write Casino 2 files",
      author="Hendrix Demers",
      author_email="hendrix.demers@mail.mcgill.ca",
      license="LGPL v3",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Physics'],

      packages=find_packages(),

      include_package_data=False, # Do not include test data

      install_requires=['Pillow', # Fork of PIL (Python 3 compatible),
                        'numpy'],
      setup_requires=['nose', 'coverage'],

      test_suite='nose.collector',
)

