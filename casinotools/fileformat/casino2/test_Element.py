#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.fileformat.casino2.test_Element

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`casinotools.fileformat.casino2.Element`.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
try:
    from io import BytesIO
except ImportError:  # Python 2
    from StringIO import StringIO as BytesIO

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.casino2.Element as Element
import casinotools.fileformat.casino2.test_File as test_File
from casinotools.utilities.path import is_bad_file
from casinotools.fileformat.casino2.line import ATOMLINE_KA1, ATOMLINE_KA2, ATOMLINE_KB1, ATOMLINE_KB2, ATOMLINE_LA, \
    ATOMLINE_LB1, ATOMLINE_LB2, ATOMLINE_LG, ATOMLINE_MA

# Globals and constants variables.


class TestElement(test_File.TestFile):
    """
    TestCase class for the module `casinotools.fileformat.casino2.Element`.
    """

    def test_read(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        with open(self.filepathSim, 'rb') as file:
            self._read_tests(file, self.version_2_45)

    def test_read_StringIO(self):
        if is_bad_file(self.filepathSim):
            raise SkipTest
        f = open(self.filepathSim, 'rb')
        file = BytesIO(f.read())
        file.mode = 'rb'
        f.close()
        self._read_tests(file, self.version_2_45)

    def _read_tests(self, file, version):
        file.seek(0)
        element = Element.Element()
        element.read(file, 500, version)
        self.assertEqual(49953, file.tell())

        self.assertEqual(5, element.Z)
        self.assertEqual('B', element.Nom)
        self.assertAlmostEqual(2.340000000000E+00, element.Rho)
        self.assertAlmostEqual(1.081000000000E+01, element.A)
        self.assertAlmostEqual(5.750000000000E-02, element.J)
        self.assertAlmostEqual(7.790367583747E-01, element.K)
        self.assertAlmostEqual(1.0, element.ef)
        self.assertAlmostEqual(7.000000000000E+07, element.kf)
        self.assertAlmostEqual(2.270000000000E+01, element.ep)

    def test_NUATOM(self):
        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('Ag')
        self.assertEqual(1, fnuatom)
        self.assertAlmostEqual(10.50, rho)
        self.assertEqual(47, z)
        self.assertEqual(107.868, a)
        self.assertAlmostEqual(5.5, ef)
        self.assertAlmostEqual(1.19, kf * 1.0e-8)
        self.assertAlmostEqual(15, ep)

        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('ag')
        self.assertEqual(0, fnuatom)
        self.assertAlmostEqual(0.0, rho)
        self.assertEqual(0, z)
        self.assertEqual(0.0, a)
        self.assertAlmostEqual(0.0, ef)
        self.assertAlmostEqual(0.0, kf)
        self.assertAlmostEqual(0.0, ep)

        fnuatom, rho, z, a, ef, kf, ep = Element.NUATOM('V')
        self.assertEqual(1, fnuatom)
        self.assertAlmostEqual(5.8, rho)
        self.assertEqual(23, z)
        self.assertEqual(50.9415, a)
        self.assertAlmostEqual(1.0, ef)
        self.assertAlmostEqual(7.0, kf * 1.0e-7)
        self.assertAlmostEqual(21.8, ep)

        # self.fail("Test if the testcase is working.")

    def test__computeK(self):
        k_ref = 7.790367583747E-01
        k = Element._computeK(5)
        self.assertAlmostEqual(k_ref, k)

        k_ref = 7.843098263659E-01
        k = Element._computeK(6)
        self.assertAlmostEqual(k_ref, k)

        # self.fail("Test if the testcase is working.")

    def test_get_total_xray_intensities_1_esr(self):
        if is_bad_file(self.filepath_cas_v251):
            raise SkipTest

        with open(self.filepath_cas_v251, 'rb') as file:
            file.seek(0)
            element = Element.Element()
            # read the empty simulation data structure.
            element.read(file, 500, self.version_2_51)
            self.assertEqual(50193, file.tell())
            # read the first simulation data structure.
            element.read(file, 500, self.version_2_51)
            self.assertEqual(100638, file.tell())

            intensities_ref = {}

            intensities_ref[ATOMLINE_KA1] = 9.269059346795805e-07
            intensities_ref[ATOMLINE_KA2] = 4.662984097246555e-07
            intensities_ref[ATOMLINE_KB1] = 1.355707793206891e-08

            intensities = element.get_total_xray_intensities_1_esr()

            self.assertEqual(len(intensities_ref), len(intensities))

            for atomic_line in intensities:
                with self.subTest(atomic_line=atomic_line):
                    self.assertAlmostEqual(intensities_ref[atomic_line]*1.0e6, intensities[atomic_line]*1.0e6)

        # self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()
