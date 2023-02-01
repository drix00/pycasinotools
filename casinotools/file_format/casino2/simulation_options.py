#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: casinotools.file_format.casino2.simulation_options
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
import logging

# Third party modules.

# Local modules.

# Project modules.
from casinotools.file_format.file_reader_writer_tools import read_double, read_int, read_long, read_float, \
    write_double, write_int, write_long, write_float, read_bool, write_bool
from casinotools.file_format.tags import add_tag_old, find_tag

# Globals and constants variables.
TAG_BSE_COEFFICIENT = b"*BECOEFF%%%%%%%"
TAG_PHYSIC_MODELS = b"*PHYSMODELS%%%%"
TAG_MICROSCOPE_SETUP = b"*MICROSETUP%%%%"
TAG_XRAY = b"*XRAY%%%%%%%%%%"
TAG_SMULATION_OPTIONS = b"*SIMOPTIONS%%%%"
TAG_DISPLAY_OPTIONS = b"*DISPLAYOPTIONS"
TAG_REGION_INFO = b"*REGIONINFO%%%%"
TAG_ENERGY_POSITIONS = b"*ENERGYBYPOS%%%"
TAG_DISTRIBUTION_SELECTION = b"*DISTSELECT%%%%"
TAG_DISTRIBUTION_POINTS = b"*DISTNUMPTS%%%%"
TAG_INTERRUPTED_SIMULATION_DATA = b"*INTSIMDATA%%%%"
TAG_SCALE_GRID = b"*SCALEGRID%%%%%"

DIRECTION_COSINES_SOUM = 0
DIRECTION_COSINES_DROUIN = 1


def get_direction_cosines_string(model_type):
    if model_type == DIRECTION_COSINES_SOUM:
        return 'Soum et al.'
    elif model_type == DIRECTION_COSINES_DROUIN:
        return 'Drouin'
    else:
        raise ValueError('Unknown direction cosines')


CROSS_SECTION_MOTT_JOY = 0
CROSS_SECTION_MOTT_EQUATION = 1
CROSS_SECTION_MOTT_BROWNING = 2
CROSS_SECTION_MOTT_RUTHERFORD = 3


def get_elastic_cross_section_type_string(model_type):
    if model_type == CROSS_SECTION_MOTT_JOY:
        return "Czyzewski"
    elif model_type == CROSS_SECTION_MOTT_EQUATION:
        return "Drouin"
    elif model_type == CROSS_SECTION_MOTT_BROWNING:
        return "Browning"
    elif model_type == CROSS_SECTION_MOTT_RUTHERFORD:
        return "Rutherford"
    else:
        raise ValueError('Unknown elastic cross section')


IONIZATION_CROSS_SECTION_GAUVIN = 0
IONIZATION_CROSS_SECTION_POUCHOU = 1
IONIZATION_CROSS_SECTION_BROWN_POWELL = 2
IONIZATION_CROSS_SECTION_CASNATI = 3
IONIZATION_CROSS_SECTION_GRYZINSKI = 4
IONIZATION_CROSS_SECTION_JAKOBY = 5


def get_ionization_cross_section_type_string(model_type):
    if model_type == IONIZATION_CROSS_SECTION_GAUVIN:
        return "Gauvin"
    elif model_type == IONIZATION_CROSS_SECTION_POUCHOU:
        return "Pouchou"
    elif model_type == IONIZATION_CROSS_SECTION_BROWN_POWELL:
        return "BrownPowell"
    elif model_type == IONIZATION_CROSS_SECTION_CASNATI:
        return "Casnati"
    elif model_type == IONIZATION_CROSS_SECTION_GRYZINSKI:
        return "Gryzinski"
    elif model_type == IONIZATION_CROSS_SECTION_JAKOBY:
        return "Jakoby"
    else:
        raise ValueError('Unknown ionization cross section')


IONIZATION_POTENTIAL_JOY = 0
IONIZATION_POTENTIAL_BERGER = 1
IONIZATION_POTENTIAL_HOVINGTON = 2


def get_ionization_potential_type_string(model_type):
    if model_type == IONIZATION_POTENTIAL_JOY:
        return "Joy"
    elif model_type == IONIZATION_POTENTIAL_BERGER:
        return "Berger"
    elif model_type == IONIZATION_POTENTIAL_HOVINGTON:
        return "Hovington"
    else:
        raise ValueError('Unknown ionization potential')


RANDOM_NUMBER_GENERATOR_PRESS_ET_AL = 0
RANDOM_NUMBER_GENERATOR_MERSENNE_TWISTER = 1


def get_random_number_generator_string(model_type):
    if model_type == RANDOM_NUMBER_GENERATOR_PRESS_ET_AL:
        return 'Press et al.'
    elif model_type == RANDOM_NUMBER_GENERATOR_MERSENNE_TWISTER:
        return 'Mersenne - Twister'
    else:
        raise ValueError("Unknown random number generator")


ENERGY_LOSS_JOY_LUO = 0


def get_energy_loss_string(model_type):
    if model_type == ENERGY_LOSS_JOY_LUO:
        return 'Joy and Luo'
    else:
        raise ValueError('Unknown energy loss')


class SimulationOptions:
    def __init__(self):
        self.bse_coefficient = 0.0
        self.FRan = 0
        self.FDeds = 0
        self.FSecTotal = 0
        self.FSecPartiel = 0
        self.FCosDirect = 0
        self.FSecIon = 0
        self.FPotMoy = 0

        self.Beam_angle = 0.0
        self.Beam_Diameter = 0.0
        self.Electron_Number = 0.0
        self.KEV_End = 0.0
        self.KEV_Start = 0.0
        self.KEV_Step = 0.0

        self.Scan_Image = 0
        self._positionEnd_nm = 0.0
        self._positionStart_nm = 0.0
        self._positionStep_nm = 0.0
        self._positionNumberStep = 0.0

        self.Scan_Energy = 0

        self.UseEnBack = False
        self.WorkDist = 0.0
        self.DetectScaleX = 0.0
        self.DetectScaleY = 0.0

        self._matrixDetector = []

        self.FEmissionRX = 0
        self.NbreCoucheRX = 0
        self.EpaisCouche = 0.0
        self.TOA = 0.0
        self.PhieRX = 0.0
        self.RkoMax = 0.0

        self.RkoMaxW = 0.0

        self.Eminimum = 0.0
        self.Electron_Display = 0
        self.Electron_Save = 0
        self.Memory_Keep = 0
        self.First = 0
        self.Keep_Sim = 0

        self.Display_Colision = 0
        self.Display_Color = 0
        self.Display_Projection = 0
        self.Display_Back = 0
        self.Display_Refresh = 0
        self.Minimum_Trajectory_Display_Distance = 0.0

        self.FForme = 0
        self.Total_Thickness = 0.0
        self.Half_Width = 0.0

        self.ShowFadedSqr = 0
        self.ShowRegions = 0
        self.SetPointstoRelativePosition = 0
        self.Summation = 0
        self.XZorXY = 0
        self.Yplane = 0
        self.Zplane = 0

        self.FDZmax = 0
        self.FDenr = 0
        self.FDent = 0
        self.FDPoire = 0
        self.FDrsr = 0
        self.FDrsrLit = 0
        self.FDncr = 0

        self.FDEpos = 0

        self.FDbang = 0

        self.FDAngleVSEnergie = 0

        self.NbPointDZMax = 0
        self.NbPointDENR = 0
        self.NbPointDENT = 0
        self.NbPointDRSR = 0
        self.NbPointDNCR = 0

        self.NbPointDEpos_X = 0
        self.NbPointDEpos_Y = 0
        self.NbPointDEpos_Z = 0

        self.NbPointDBANG = 0

        self.NbPointDAngleVSEnergie = 0

        self.RangeFinder = 0
        self.RangeSafetyFactor = 0.0
        self.FixedRange = 0.0

        self.BEMin_Angle = 0.0
        self.BEMax_Angle = 0.0

        self.FEFilter = 0
        self.EFilterMax = 0.0
        self.EFilterMin = 0.0

        self.EFilterVal = []

        self.FDZmax = 0
        self.FDZmaxLog = 0
        self.NbPointDZMax = 0
        self.DZmaxMax = 0.0
        self.DZmaxMin = 0.0

        self.FDenr = 0
        self.FDenrLog = 0
        self.NbPointDENR = 0
        self.DenrMax = 0.0
        self.DenrMin = 0.0

        self.FDent = 0
        self.FDentLog = 0
        self.NbPointDENT = 0
        self.DentMax = 0.0
        self.DentMin = 0.0

        self.FDrsr = 0
        self.FDrsrLog = 0
        self.NbPointDRSR = 0
        self.DrsrMax = 0.0
        self.DrsrMin = 0.0

        self.FDbang = 0
        self.FDbangLog = 0
        self.NbPointDBANG = 0
        self.DbangMax = 0.0
        self.DbangMin = 0.0

        self.FDAngleVSEnergie = 0
        self.FDAngleVSEnergieLog = 0
        self.NbPointDAngleVSEnergie = 0
        self.DAngleVSEnergieMax = 0.0
        self.DAngleVSEnergieMin = 0.0

        self.Eo = 0.0
        self.NoElec = 0
        self.PositionF_X = 0.0
        self.PositionF_Y = 0.0
        self.Theta0 = 0.0
        self.Phi0 = 0.0
        self.num_at = 0

        self.Tot_Ret = 0.0

        self.MinX = 0.0
        self.MinY = 0.0
        self.MinZ = 0.0
        self.MaxX = 0.0
        self.MaxY = 0.0
        self.MaxZ = 0.0
        self.NbCollMax = 0.0
        self.NbCollMax2 = 0.0
        self.RatioX = 0.0
        self.RatioY = 0.0
        self.RatioZ = 0.0

        self.Tot_Ret_En = 0.0

        self.NumVtabs = 0
        self.NumHtabs = 0

        self.TOA = 0.0
        self.Total_Thickness = 0.0

    def read(self, file, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tag_id = TAG_BSE_COEFFICIENT
        if not find_tag(file, tag_id):
            raise IOError
        self.bse_coefficient = read_double(file)

        # Selected Physical Model variables
        tag_id = TAG_PHYSIC_MODELS
        if not find_tag(file, tag_id):
            raise IOError

        self.FRan = read_int(file)
        self.FDeds = read_int(file)
        self.FSecTotal = read_int(file)
        self.FSecPartiel = read_int(file)
        self.FCosDirect = read_int(file)
        self.FSecIon = read_int(file)
        self.FPotMoy = read_int(file)

        # Microscope SetUp
        tag_id = TAG_MICROSCOPE_SETUP
        if not find_tag(file, tag_id):
            raise IOError

        self.Beam_angle = read_double(file)
        self.Beam_Diameter = read_double(file)
        self.Electron_Number = read_long(file)
        self.KEV_End = read_double(file)
        self.KEV_Start = read_double(file)
        self.KEV_Step = read_double(file)

        self.Scan_Image = read_int(file)
        pos_end = read_double(file)
        self._positionEnd_nm = pos_end
        pos_start = read_double(file)
        self._positionStart_nm = pos_start
        # In CASINO pos_number_steps is the step length.
        pos_number_steps = read_double(file)
        self._positionStep_nm = pos_number_steps
        # In CASINO pos_step is the number of steps and not used.
        pos_step = read_double(file)
        self._positionNumberStep = pos_step

        if version >= 21:
            self.Scan_Energy = read_int(file)

        if version >= 25:
            self.UseEnBack = read_bool(file)
            self.WorkDist = read_double(file)
            self.DetectScaleX = read_double(file)
            self.DetectScaleY = read_double(file)

            if self.UseEnBack:
                self._matrixDetector = []
                for dummy1 in range(101):
                    row = []
                    for dummy2 in range(101):
                        value = read_double(file)
                        row.append(value)
                    self._matrixDetector.append(row)

        # XRay
        tag_id = TAG_XRAY
        if not find_tag(file, tag_id):
            raise IOError

        self.FEmissionRX = read_int(file)
        self.NbreCoucheRX = read_long(file)
        self.EpaisCouche = read_double(file)
        self.TOA = read_double(file)
        self.PhieRX = read_float(file)
        self.RkoMax = read_double(file)

        if version >= 22:
            self.RkoMaxW = read_double(file)

        # Simulation options
        tag_id = TAG_SMULATION_OPTIONS
        if not find_tag(file, tag_id):
            raise IOError

        self.Eminimum = read_double(file)
        self.Electron_Display = read_long(file)
        self.Electron_Save = read_long(file)
        self.Memory_Keep = read_int(file)
        self.First = read_int(file)
        self.Keep_Sim = read_int(file)

        # Display Options
        tag_id = TAG_DISPLAY_OPTIONS
        if not find_tag(file, tag_id):
            raise IOError

        self.Display_Colision = read_int(file)
        self.Display_Color = read_int(file)
        self.Display_Projection = read_int(file)
        self.Display_Back = read_int(file)
        self.Display_Refresh = read_int(file)
        self.Minimum_Trajectory_Display_Distance = read_double(file)

        # Region Info
        tag_id = TAG_REGION_INFO
        if not find_tag(file, tag_id):
            raise IOError

        self.FForme = read_int(file)
        self.Total_Thickness = read_double(file)
        self.Half_Width = read_double(file)

        # Energy by position
        if version >= 22:
            tag_id = TAG_ENERGY_POSITIONS
            if not find_tag(file, tag_id):
                raise IOError

            self.ShowFadedSqr = read_int(file)
            self.ShowRegions = read_int(file)
            self.SetPointstoRelativePosition = read_int(file)
            self.Summation = read_int(file)
            self.XZorXY = read_int(file)
            self.Yplane = read_int(file)
            self.Zplane = read_int(file)

        # Distribution selection
        tag_id = TAG_DISTRIBUTION_SELECTION
        if not find_tag(file, tag_id):
            raise IOError

        self.FDZmax = read_int(file)
        self.FDenr = read_int(file)
        self.FDent = read_int(file)
        self.FDPoire = read_int(file)
        self.FDrsr = read_int(file)
        self.FDrsrLit = read_int(file)
        self.FDncr = read_int(file)

        self.FDEpos = 0
        if version >= 22:
            self.FDEpos = read_int(file)

        if version >= 25:
            self.FDbang = read_int(file)

        if version >= 26:
            self.FDAngleVSEnergie = read_int(file)

        # Distribution points
        tag_id = TAG_DISTRIBUTION_POINTS
        if not find_tag(file, tag_id):
            raise IOError

        self.NbPointDZMax = read_long(file)
        self.NbPointDENR = read_long(file)
        self.NbPointDENT = read_long(file)
        self.NbPointDRSR = read_long(file)
        self.NbPointDNCR = read_long(file)

        if version >= 22:
            self.NbPointDEpos_X = read_long(file)
            self.NbPointDEpos_Y = read_long(file)
            self.NbPointDEpos_Z = read_long(file)

        if version >= 25:
            self.NbPointDBANG = read_long(file)

        if version >= 26:
            self.NbPointDAngleVSEnergie = read_long(file)

        if version >= 23:
            self.RangeFinder = read_int(file)
            self.RangeSafetyFactor = read_double(file)
            self.FixedRange = read_double(file)

        if version >= 24:
            self.BEMin_Angle = read_double(file)
            self.BEMax_Angle = read_double(file)

            self.FEFilter = read_int(file)
            self.EFilterMax = read_double(file)
            self.EFilterMin = read_double(file)

            self.EFilterVal = []
            for dummy in range(101):
                value = read_double(file)
                self.EFilterVal.append(value)

        if version >= 2040601:
            self.FDZmax = read_int(file)
            self.FDZmaxLog = read_int(file)
            self.NbPointDZMax = read_long(file)
            self.DZmaxMax = read_double(file)
            self.DZmaxMin = read_double(file)

            self.FDenr = read_int(file)
            self.FDenrLog = read_int(file)
            self.NbPointDENR = read_long(file)
            self.DenrMax = read_double(file)
            self.DenrMin = read_double(file)

            self.FDent = read_int(file)
            self.FDentLog = read_int(file)
            self.NbPointDENT = read_long(file)
            self.DentMax = read_double(file)
            self.DentMin = read_double(file)

            self.FDrsr = read_int(file)
            self.FDrsrLog = read_int(file)
            self.NbPointDRSR = read_long(file)
            self.DrsrMax = read_double(file)
            self.DrsrMin = read_double(file)

            self.FDbang = read_int(file)
            self.FDbangLog = read_int(file)
            self.NbPointDBANG = read_long(file)
            self.DbangMax = read_double(file)
            self.DbangMin = read_double(file)

            self.FDAngleVSEnergie = read_int(file)
            self.FDAngleVSEnergieLog = read_int(file)
            self.NbPointDAngleVSEnergie = read_long(file)
            self.DAngleVSEnergieMax = read_double(file)
            self.DAngleVSEnergieMin = read_double(file)

        # Interrupted Simulation Data
        tag_id = TAG_INTERRUPTED_SIMULATION_DATA
        if not find_tag(file, tag_id):
            raise IOError

        self.Eo = read_double(file)
        self.NoElec = read_long(file)
        self.PositionF_X = read_double(file)
        self.PositionF_Y = read_double(file)
        self.Theta0 = read_double(file)
        self.Phi0 = read_double(file)
        self.num_at = read_long(file)
        if version > 23:
            self.Tot_Ret = read_double(file)
        else:
            self.Tot_Ret = read_long(file)

        self.MinX = read_double(file)
        self.MinY = read_double(file)
        self.MinZ = read_double(file)
        self.MaxX = read_double(file)
        self.MaxY = read_double(file)
        self.MaxZ = read_double(file)
        self.NbCollMax = read_double(file)
        self.NbCollMax2 = read_double(file)
        self.RatioX = read_double(file)
        self.RatioY = read_double(file)
        self.RatioZ = read_double(file)

        if version >= 25:
            self.Tot_Ret_En = read_double(file)

        # Scale & grid data
        tag_id = TAG_SCALE_GRID
        if not find_tag(file, tag_id):
            raise IOError

        self.NumVtabs = read_int(file)
        self.NumHtabs = read_int(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_BSE_COEFFICIENT
        add_tag_old(file, tag_id)
        write_double(file, self.bse_coefficient)

        tag_id = TAG_PHYSIC_MODELS
        add_tag_old(file, tag_id)
        write_int(file, self.FRan)
        write_int(file, self.FDeds)
        write_int(file, self.FSecTotal)
        write_int(file, self.FSecPartiel)
        write_int(file, self.FCosDirect)
        write_int(file, self.FSecIon)
        write_int(file, self.FPotMoy)

        tag_id = TAG_MICROSCOPE_SETUP
        add_tag_old(file, tag_id)
        write_double(file, self.Beam_angle)
        write_double(file, self.Beam_Diameter)
        write_long(file, self.Electron_Number)
        write_double(file, self.KEV_End)
        write_double(file, self.KEV_Start)
        write_double(file, self.KEV_Step)

        write_int(file, self.Scan_Image)
        pos_end = self._positionEnd_nm
        write_double(file, pos_end)
        pos_start = self._positionStart_nm
        write_double(file, pos_start)
        # In CASINO pos_number_steps is the step length.
        pos_number_steps = self._positionStep_nm
        write_double(file, pos_number_steps)
        # In CASINO pos_step is the number of steps and not used.
        pos_step = self._positionNumberStep
        write_double(file, pos_step)

        write_int(file, self.Scan_Energy)

        write_bool(file, self.UseEnBack)
        write_double(file, self.WorkDist)
        write_double(file, self.DetectScaleX)
        write_double(file, self.DetectScaleY)

        if self.UseEnBack:
            assert len(self._matrixDetector) == 101
            for index1 in range(101):
                row = self._matrixDetector[index1]
                assert len(row) == 101
                for index2 in range(101):
                    value = row[index2]
                    write_double(file, value)

        tag_id = TAG_XRAY
        add_tag_old(file, tag_id)
        write_int(file, self.FEmissionRX)
        write_long(file, self.NbreCoucheRX)
        write_double(file, self.EpaisCouche)
        write_double(file, self.TOA)
        write_float(file, self.PhieRX)
        write_double(file, self.RkoMax)
        write_double(file, self.RkoMaxW)

        tag_id = TAG_SMULATION_OPTIONS
        add_tag_old(file, tag_id)
        write_double(file, self.Eminimum)
        write_long(file, self.Electron_Display)
        write_long(file, self.Electron_Save)
        write_int(file, self.Memory_Keep)
        write_int(file, self.First)
        write_int(file, self.Keep_Sim)

        tag_id = TAG_DISPLAY_OPTIONS
        add_tag_old(file, tag_id)
        write_int(file, self.Display_Colision)
        write_int(file, self.Display_Color)
        write_int(file, self.Display_Projection)
        write_int(file, self.Display_Back)
        write_int(file, self.Display_Refresh)
        write_double(file, self.Minimum_Trajectory_Display_Distance)

        tag_id = TAG_REGION_INFO
        add_tag_old(file, tag_id)
        write_int(file, self.FForme)
        write_double(file, self.Total_Thickness)
        write_double(file, self.Half_Width)

        tag_id = TAG_ENERGY_POSITIONS
        add_tag_old(file, tag_id)
        write_int(file, self.ShowFadedSqr)
        write_int(file, self.ShowRegions)
        write_int(file, self.SetPointstoRelativePosition)
        write_int(file, self.Summation)
        write_int(file, self.XZorXY)
        write_int(file, self.Yplane)
        write_int(file, self.Zplane)

        tag_id = TAG_DISTRIBUTION_SELECTION
        add_tag_old(file, tag_id)
        write_int(file, self.FDZmax)
        write_int(file, self.FDenr)
        write_int(file, self.FDent)
        write_int(file, self.FDPoire)
        write_int(file, self.FDrsr)
        write_int(file, self.FDrsrLit)
        write_int(file, self.FDncr)
        write_int(file, self.FDEpos)
        write_int(file, self.FDbang)
        write_int(file, self.FDAngleVSEnergie)

        tag_id = TAG_DISTRIBUTION_POINTS
        add_tag_old(file, tag_id)
        write_long(file, self.NbPointDZMax)
        write_long(file, self.NbPointDENR)
        write_long(file, self.NbPointDENT)
        write_long(file, self.NbPointDRSR)
        write_long(file, self.NbPointDNCR)

        write_long(file, self.NbPointDEpos_X)
        write_long(file, self.NbPointDEpos_Y)
        write_long(file, self.NbPointDEpos_Z)

        write_long(file, self.NbPointDBANG)

        write_long(file, self.NbPointDAngleVSEnergie)

        write_int(file, self.RangeFinder)
        write_double(file, self.RangeSafetyFactor)
        write_double(file, self.FixedRange)

        write_double(file, self.BEMin_Angle)
        write_double(file, self.BEMax_Angle)

        write_int(file, self.FEFilter)
        write_double(file, self.EFilterMax)
        write_double(file, self.EFilterMin)

        assert len(self.EFilterVal) == 101
        for index in range(101):
            write_double(file, self.EFilterVal[index])

        write_int(file, self.FDZmax)
        write_int(file, self.FDZmaxLog)
        write_long(file, self.NbPointDZMax)
        write_double(file, self.DZmaxMax)
        write_double(file, self.DZmaxMin)

        write_int(file, self.FDenr)
        write_int(file, self.FDenrLog)
        write_long(file, self.NbPointDENR)
        write_double(file, self.DenrMax)
        write_double(file, self.DenrMin)

        write_int(file, self.FDent)
        write_int(file, self.FDentLog)
        write_long(file, self.NbPointDENT)
        write_double(file, self.DentMax)
        write_double(file, self.DentMin)

        write_int(file, self.FDrsr)
        write_int(file, self.FDrsrLog)
        write_long(file, self.NbPointDRSR)
        write_double(file, self.DrsrMax)
        write_double(file, self.DrsrMin)

        write_int(file, self.FDbang)
        write_int(file, self.FDbangLog)
        write_long(file, self.NbPointDBANG)
        write_double(file, self.DbangMax)
        write_double(file, self.DbangMin)

        write_int(file, self.FDAngleVSEnergie)
        write_int(file, self.FDAngleVSEnergieLog)
        write_long(file, self.NbPointDAngleVSEnergie)
        write_double(file, self.DAngleVSEnergieMax)
        write_double(file, self.DAngleVSEnergieMin)

        tag_id = TAG_INTERRUPTED_SIMULATION_DATA
        add_tag_old(file, tag_id)
        write_double(file, self.Eo)
        write_long(file, self.NoElec)
        write_double(file, self.PositionF_X)
        write_double(file, self.PositionF_Y)
        write_double(file, self.Theta0)
        write_double(file, self.Phi0)
        write_long(file, self.num_at)
        write_double(file, self.Tot_Ret)

        write_double(file, self.MinX)
        write_double(file, self.MinY)
        write_double(file, self.MinZ)
        write_double(file, self.MaxX)
        write_double(file, self.MaxY)
        write_double(file, self.MaxZ)
        write_double(file, self.NbCollMax)
        write_double(file, self.NbCollMax2)
        write_double(file, self.RatioX)
        write_double(file, self.RatioY)
        write_double(file, self.RatioZ)

        write_double(file, self.Tot_Ret_En)

        tag_id = TAG_SCALE_GRID
        add_tag_old(file, tag_id)
        write_int(file, self.NumVtabs)
        write_int(file, self.NumHtabs)

    def set_number_electrons(self, number_electrons):
        self.Electron_Number = number_electrons

    def get_number_electrons(self):
        return self.Electron_Number

    def set_incident_energy_keV(self, energy_keV):
        if self.Scan_Energy is False:
            self.KEV_End = energy_keV
            self.KEV_Step = 1.0

        self.KEV_Start = energy_keV

    def get_incident_energy_keV(self, index=None):
        if index is None:
            return self.KEV_Start
        else:
            incident_energy_keV = self.KEV_Start + index * self.KEV_Step
            if incident_energy_keV <= self.KEV_End:
                return incident_energy_keV
            else:
                raise ValueError

    def set_toa_deg(self, toa_deg):
        self.TOA = toa_deg

    def get_toa_deg(self):
        return self.TOA

    def set_beam_angle_deg(self, beam_angle_deg):
        self.Beam_angle = beam_angle_deg

    def get_beam_angle_deg(self):
        return self.TOA

    def get_number_x_ray_layers(self):
        return self.NbreCoucheRX

    def set_direction_cosines(self, direction_cosines_model):
        self.FCosDirect = direction_cosines_model

    def get_direction_cosines(self):
        return self.FCosDirect

    def set_total_electron_elastic_cross_section(self, cross_section_model):
        self.FSecTotal = cross_section_model

    def get_total_electron_elastic_cross_section(self):
        return self.FSecTotal

    def set_partial_electron_elastic_cross_section(self, cross_section_model):
        self.FSecPartiel = cross_section_model

    def get_partial_electron_elastic_cross_section(self):
        return self.FSecPartiel

    def set_elastic_cross_section_type(self, cross_section_model):
        self.FSecTotal = cross_section_model
        self.FSecPartiel = cross_section_model

    def set_ionization_cross_section_type(self, model_type):
        self.FSecIon = model_type

    def get_ionization_cross_section_type(self):
        return self.FSecIon

    def set_ionization_potential_type(self, model_type):
        self.FPotMoy = model_type

    def get_ionization_potential_type(self):
        return self.FPotMoy

    def set_random_number_generator_type(self, model_type):
        self.FRan = model_type

    def get_random_number_generator_type(self):
        return self.FRan

    def set_energy_loss_type(self, model_type):
        self.FDeds = model_type

    def get_energy_loss_type(self):
        return self.FDeds

    def set_total_thickness_nm(self, total_thickness_nm):
        self.Total_Thickness = total_thickness_nm

    def get_bse_coefficient(self):
        return self.bse_coefficient

    def get_line_scan_parameters(self):
        parameters = (self._positionStart_nm, self._positionEnd_nm, self._positionNumberStep, self._positionStep_nm)
        return parameters

    def set_linescan_parameters(self, start_nm, end_nm, step_nm):
        """
        Sets the linescan parameters.
        If the beam is stationary, use :meth:`.set_position` instead.

        .. note::

           The CASINO v2 code is very bad with naming variables.
           The POS_NStep is actually the step length and the POS_Step is not used.
           The correct variable are used in the read and write methods.

        :arg start_nm: start position (in nm)
        :arg end_nm: end position (in nm)
        :arg step_nm: step length (in nm)
        """
        number_steps = (end_nm - start_nm) / step_nm

        self.Scan_Image = 1  # Turn on the line scan mode
        self._positionStart_nm = start_nm
        self._positionEnd_nm = end_nm
        self._positionNumberStep = number_steps
        self._positionStep_nm = step_nm

    def set_position(self, pos_nm):
        """
        Sets the position of the beam.

        :arg pos_nm: position of the beam (in nm)
        """
        self.Scan_Image = 0  # Turn off the line scan mode
        self._positionStart_nm = pos_nm
        self._positionEnd_nm = pos_nm
        self._positionNumberStep = 1
        self._positionStep_nm = 1.0  # Cannot be 0.0 as Casino2 returns "Out of memory" error

    def get_maximum_depth_nm(self):
        return self.RkoMax

    def get_maximum_lateral_width(self):
        return self.RkoMaxW
