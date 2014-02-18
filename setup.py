#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import zipfile
from distutils.cmd import Command
from distutils.command import clean, bdist, bdist_dumb

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.

class TestDataCommand(Command):

    description = "create a zip of all files in the testData folder"
    user_options = [('dist-dir=', 'd',
                     "directory to put final built distributions in "
                     "[default: dist]"), ]

    def initialize_options(self):
        self.dist_dir = None

    def finalize_options(self):
        if self.dist_dir is None:
            self.dist_dir = "dist"

    def run(self):
        basepath = os.path.dirname(__file__)
        testdatapath = os.path.join(basepath, 'src', 'casinotools', 'testData')

        zipfilename = self.distribution.get_fullname() + '-testData.zip'
        zipfilepath = os.path.join(self.dist_dir, zipfilename)
        with zipfile.ZipFile(zipfilepath, 'w') as z:
            for root, dirs, files in os.walk(testdatapath):
                for file in files:
                    filename = os.path.join(root, file)
                    arcname = os.path.relpath(filename, basepath)
                    z.write(filename, arcname)

setup(name="pyCasinoTools",
      version='0.1',
      url='http://www.gel.usherbrooke.ca/casino',
      description="Python interface to read and write Casino 2 files",
      author="Hendrix Demers",
      author_email="hendrix.demers@mail.mcgill.ca",
      license="LGPL v3",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Physics'],

      packages=find_packages('src'),
      package_dir={'':'src'},

      include_package_data=False, # Do not include test data

      install_requires=['Pillow', # Fork of PIL (Python 3 compatible),
                        'numpy',
                        'scipy'],

      tests_require=['nose'],
      test_suite='nose.collector',

      cmdclass={'zip_testdata': TestDataCommand},
)

