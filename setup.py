#!/usr/bin/env python

# Standard library modules.

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Pillow',  # Fork of PIL (Python 3 compatible),
    'numpy'
]

test_requirements = [
    'nose', 'coverage'
]

long_description = """
Python interface for the Monte Carlo simulation program CASINO version 2 and 3.

CASINO: http://www.gel.usherbrooke.ca/casino/index.html
"""

packages = find_packages()

setup(name="pyCasinoTools",
      version='0.2.1',
      description="Python interface for the Monte Carlo simulation program CASINO version 2 and 3.",
      long_description=long_description,
      author="Hendrix Demers",
      author_email="hendrix.demers@mail.mcgill.ca",
      url='https://github.com/drix00/casinotools',
      include_package_data=True,
      install_requires=requirements,
      license="Apache Software License 2.0",
      zip_safe=False,
      keywords='casinotools',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Physics'],

      packages=packages,
      package_dir={'casinotools':
                       'casinotools'},

      test_suite='nose.collector',
      tests_require=test_requirements
      )
