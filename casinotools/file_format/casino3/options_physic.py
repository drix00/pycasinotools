#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino3.options_physic
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
"""

###############################################################################
# Copyright 2020 Hendrix Demers
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
from enum import Enum

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_int, read_double, write_int, write_double
from casinotools.file_format.tags import find_tag, find_tag_position

# Globals and constants variables.


# Filename to store the defaults settings
OPTIONS_PHYSIC_DEF_FILENAME = "PhysicModel_Settings_Defaults.dat"

# Random number generator choice const declaration
RAND_PRESS = 0
RAND_MTOLD = 1
RAND_MT19937 = 2
RAND_LF607 = 3

# dEdS consts
DEDS_JOYK_GAUVIN = 0
DEDS_JOYLUO_MONSEL = 1
DEDS_BETHERELATIVISTE = 2


# Electron elastic cross section.
class CrossSection(Enum):
    MOTT_FILE = 0
    MOTT_DROUIN = 1
    MOTT_BROWNING = 2
    RUTHERFORD = 3
    REIMER = 4
    ELSEPA = 5


def get_electron_elastic_cross_section_model_label(cs_model):
    cs_model = int(cs_model)
    if cs_model == CrossSection.MOTT_FILE:
        return "Mott Interpolation"
    elif cs_model == CrossSection.MOTT_DROUIN:
        return "Mott eq. Drouin"
    elif cs_model == CrossSection.MOTT_BROWNING:
        return "Mott eq. Browning"
    elif cs_model == CrossSection.RUTHERFORD:
        return "Rutherford"
    elif cs_model == CrossSection.REIMER:
        return "Rutherford Reimer"
    elif cs_model == CrossSection.ELSEPA:
        return "Mott Salvat"
    else:
        raise ValueError


# # partial cross section consts
# PCS_MOTT_FICHIER = 0
# PCS_MOTT_EQ = 1
# PCS_MOTT_BROWNING = 2
# PCS_RUTHE = 3
# PCS_REIMER = 4
# PCS_ELSEPA = 5
#
# # total cross section consts
# TCS_MOTT_FICHIER = 0
# TCS_MOTT_EQ = 1
# TCS_MOTT_BROWNING = 2
# TCS_RUTHE = 3
# TCS_REIMER = 4
# TCS_ELSEPA = 5

# inionisation potential
ION_POT_JOY = 0
ION_POT_BERGER = 1
ION_POT_PH = 2

# Directing Cosine
COS_DIRECT_SOUM = 0
COS_DIRECT_MONSEL = 1
COS_DIRECT_DROUIN = 2

# Effective Ionisation Section
SEC_ION_GAUVIN = 0
SEC_ION_POUCHOU = 1
SEC_ION_BROWN_POWELL = 2
SEC_ION_CASNATI = 3
SEC_ION_GRYZINSKI = 4
SEC_ION_JAKOBY = 5

# Default value for some options
MIN_ENERGY_NOSEC_DEFAULT = 0.05


class OptionsPhysic:
    # Residual energy loss used in the Monsel algorithm of De/Ds calculation.
    # The goal is to account for energy loss not included in the original
    # continual energy loss equation (Bethe algorithm in Monsel). This value
    # should change depending on the sample elements and has a dramatic effect
    # on secondary electron yield.

    #    double Residual_Energy_Loss

    # Minimum energy of the electron in keV.
    # Used to determine when to stop using the electron. Not used in Monsel (secondary electron)
    # simulation : different calculation permit us to use a lower value :
    # (Trajectory_Collision::Region_Info::ect).

    #    double Min_Energy_Nosec

    # Minimum energy of an electron.
    # Will usually be set to the working function of a region, but it can
    # be overided by the user. To use the working function value, leave it
    # to <= 0. Derived from Monsel code.
    # @date 23 October 2003
    # @author Dany Joly

    #    double Min_Energy_With_Sec

    # Minimum energy for a newly generated secondary electron.
    # Will usually be set to the working function of a region, but it can
    # be overided by the user. To use the working function value, leave it
    # to <= 0. Derived from Monsel code
    # @date 23 October 2003
    # @author Dany Joly

    #    double Min_Gen_Secondary_Energy

    # Physical models flags

    # choix du generateur de nombre aleatoires.
    # appelle ran3 (numerical recipes) si =0, appelle mersenne twister si =1

    #    int FRan

    # Flag for the energy lost equation :
    # - 0 JoyKCst de Gauvin
    # - 1 Bethe Relativiste

    #    int FDeds

    # Flag for the total cross section :
    # - 0 Mott par interpolation (fichiers, rapide)
    # - 1 Mott equations de Drouin et Gauvin
    # - 2 Mott equations de Browning
    # - 3 Rutherford par Murata
    #    int FTotalCross

    # Flag for the partial cross section :
    # - 0 Mott par interpolation (fichiers, rapide)
    # - 1 Mott equations de Drouin et Gauvin
    # - 2 Mott equations de Browning
    # - 3 Rutherford par Murata
    #    int FPartialCross

    # Flag for directing cosin
    #    int FCosDirect

    # Flag for ionisation section
    #    int FSecIon

    # Flag for Average Potential
    #    int FPotMoy

    # Physical models options

    # Nombre maximal de niveau d'electrons secondaires pouvant etre crees.
    # Niveaux
    # - 1 : Primaires
    # - 2 : Secondaires
    # - 3 : Tertiaires
    #    int max_secondary_order
    def __init__(self):
        self.FRan = 0
        self.FDeds = DEDS_JOYK_GAUVIN
        self.FTotalCross = CrossSection.MOTT_FILE
        self.FPartialCross = CrossSection.MOTT_FILE
        self.FCosDirect = COS_DIRECT_MONSEL
        self.FSecIon = SEC_ION_CASNATI
        self.FPotMoy = ION_POT_JOY

        self.max_secondary_order = 10
        self.Min_Energy_Nosec = MIN_ENERGY_NOSEC_DEFAULT
        self.Residual_Energy_Loss = 0.0004
        self.Min_Energy_With_Sec = -1.0
        self.Min_Gen_Secondary_Energy = -1.0

        self.version = 0

        self.reset()

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'

        pass
#        Tags::AddTag(file, "*PHYS_MOD_BEG", 15)
#        writeVersion(file)
#
#        safewrite<int>(file, FRan)
#        safewrite<int>(file, FDeds)
#        safewrite<int>(file, FTotalCross)
#        safewrite<int>(file, FPartialCross)
#        safewrite<int>(file, FCosDirect)
#        safewrite<int>(file, FSecIon)
#        safewrite<int>(file, FPotMoy)
#        safewrite<int>(file, max_secondary_order)
#        safewrite<double>(file, Min_Energy_Nosec)
#        safewrite<double>(file, Residual_Energy_Loss)
#        safewrite<double>(file, Min_Energy_With_Sec)
#        safewrite<double>(file, Min_Gen_Secondary_Energy)
#
#        Tags::AddTag(file, "*PHYS_MOD_END", 15)

    def modify(self, file):
        assert getattr(file, 'mode') == 'rb+'

        file.seek(0, 0)
        tag_id = b"*PHYS_MOD_BEG"
        position = find_tag_position(file, tag_id)
        file.seek(position, 0)

        write_int(file, self.version)

        write_int(file, self.FRan)
        write_int(file, self.FDeds)
        write_int(file, self.FTotalCross)
        write_int(file, self.FPartialCross)
        write_int(file, self.FCosDirect)
        #        FCosDirect = COS_DIRECT_MONSEL #Other Cos Direct are flawed for now
        write_int(file, self.FSecIon)
        write_int(file, self.FPotMoy)

        write_int(file, self.max_secondary_order)
        write_double(file, self.Min_Energy_Nosec)
        write_double(file, self.Residual_Energy_Loss)
        write_double(file, self.Min_Energy_With_Sec)
        write_double(file, self.Min_Gen_Secondary_Energy)

    def read(self, file):
        tag_id = b"*PHYS_MOD_BEG"
        find_tag(file, tag_id)

        self.version = read_int(file)

        self.FRan = read_int(file)
        self.FDeds = read_int(file)
        self.FTotalCross = read_int(file)
        self.FPartialCross = read_int(file)
        self.FCosDirect = read_int(file)
#        FCosDirect = COS_DIRECT_MONSEL #Other Cos Direct are flawed for now
        self.FSecIon = read_int(file)
        self.FPotMoy = read_int(file)

        self.max_secondary_order = read_int(file)
        self.Min_Energy_Nosec = read_double(file)
        self.Residual_Energy_Loss = read_double(file)
        self.Min_Energy_With_Sec = read_double(file)
        self.Min_Gen_Secondary_Energy = read_double(file)

        tag_id = b"*PHYS_MOD_END"
        find_tag(file, tag_id)

    def reset(self):
        self.FRan = 0
        self.FDeds = DEDS_JOYK_GAUVIN
        self.FTotalCross = CrossSection.MOTT_FILE
        self.FPartialCross = CrossSection.MOTT_FILE
        self.FCosDirect = COS_DIRECT_MONSEL
        self.FSecIon = SEC_ION_CASNATI
        self.FPotMoy = ION_POT_JOY

        self.max_secondary_order = 10
        self.Min_Energy_Nosec = MIN_ENERGY_NOSEC_DEFAULT
        self.Residual_Energy_Loss = 0.0004
        self.Min_Energy_With_Sec = -1.0
        self.Min_Gen_Secondary_Energy = -1.0

    def is_monsel_settings(self):
        return self.FCosDirect == COS_DIRECT_MONSEL and self.FDeds == DEDS_JOYLUO_MONSEL and \
               self.FPartialCross == CrossSection.MOTT_BROWNING and self.FTotalCross == CrossSection.MOTT_BROWNING and \
               self.FPotMoy == ION_POT_JOY

    def set_to_monsel_settings(self):
        self.FCosDirect = COS_DIRECT_MONSEL
        self.FDeds = DEDS_JOYLUO_MONSEL
        self.FPartialCross = CrossSection.MOTT_BROWNING
        self.FTotalCross = CrossSection.MOTT_BROWNING
        self.FPotMoy = ION_POT_JOY

    def is_interpolation(self):
        return self.FTotalCross == CrossSection.MOTT_FILE or self.FTotalCross == CrossSection.ELSEPA or \
               self.FPartialCross == CrossSection.MOTT_FILE or self.FPartialCross == CrossSection.ELSEPA
