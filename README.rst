=============
pycasinotools
=============


.. image:: https://img.shields.io/pypi/v/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools
   :alt: Pypi Status

.. image:: https://travis-ci.org/drix00/pycasinotools.svg?branch=master
   :target: https://travis-ci.org/drix00/pycasinotools
   :alt: Build Status

.. image:: https://readthedocs.org/projects/pycasinotools/badge/?version=latest
   :target: https://pycasinotools.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/codecov/c/github/pycasinotools/pycasinotools.svg
   :target: https://codecov.io/gh/drix00/pycasinotools
   :alt: Code coverage Status

.. image:: https://codecov.io/gh/drix00/pycasinotools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/drix00/pycasinotools
   :alt: Code coverage Status

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
   :target: https://raw.githubusercontent.com/drix00/pycasinotools/master/LICENSE
   :alt: License Status

Python interface for the Monte Carlo simulation program CASINO version 2 and 3.

CASINO: http://www.gel.usherbrooke.ca/casino/index.html

* Free software: Apache Software License 2.0
* Documentation: https://pycasinotools.readthedocs.io.


Features
========

* TODO

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Badges
======

pypy
----

.. image:: https://img.shields.io/pypi/v/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools

.. image:: https://img.shields.io/pypi/l/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools

.. image:: https://img.shields.io/pypi/dm/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools
.. image:: https://img.shields.io/pypi/dw/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools
.. image:: https://img.shields.io/pypi/dd/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools

.. image:: https://img.shields.io/pypi/wheel/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools
.. image:: https://img.shields.io/pypi/format/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools
.. image:: https://img.shields.io/pypi/pyversions/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools
.. image:: https://img.shields.io/pypi/implementation/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools

.. image:: https://img.shields.io/pypi/status/pycasinotools.svg
   :target: https://pypi.python.org/pypi/pycasinotools

GitHub
------

.. image:: https://pyup.io/repos/github/drix00/casinotools/shield.svg
   :target: https://pyup.io/repos/github/drix00/pycasinotools/
   :alt: Updates

.. image:: https://img.shields.io/github/issues/drix00/pycasinotools.svg
   :target: https://github.com/drix00/pycasinotools/issues

.. image:: https://img.shields.io/github/forks/drix00/pycasinotools.svg
   :target: https://github.com/drix00/pycasinotools/network

.. image:: https://img.shields.io/github/stars/drix00/pycasinotools.svg
   :target: https://github.com/drix00/pycasinotools/stargazers

Development
===========

In the *casinotools folder*, run to install the project in develop mode

.. code:: shell

   pip install -e .

Build the documentation:

.. code-block:: console

    $ cd docs
    $ make html

Add or modify the API documentation:

.. code-block:: console

    $ cd docs
    $ sphinx-apidoc -o api -e -f -P ../casinotools
    $ make html

Before commiting your modification.

In the *casinotools folder*, run the tests:

.. code-block:: console

    $ pytest -v

check the code style:

.. code-block:: console

    $ pycodestyle .
    $ pyflakes .


To do
-----

.. todolist::
