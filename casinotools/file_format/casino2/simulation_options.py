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
from casinotools.file_format.file_reader_writer_tools import FileReaderWriterTools

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


class SimulationOptions(FileReaderWriterTools):
    def __init__(self):
        self._bseCoefficient = 0.0
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
        if not self.find_tag(file, tag_id):
            raise IOError
        self._bseCoefficient = self.read_double(file)

        # Selected Physical Model variables
        tag_id = TAG_PHYSIC_MODELS
        if not self.find_tag(file, tag_id):
            raise IOError

        self.FRan = self.read_int(file)
        self.FDeds = self.read_int(file)
        self.FSecTotal = self.read_int(file)
        self.FSecPartiel = self.read_int(file)
        self.FCosDirect = self.read_int(file)
        self.FSecIon = self.read_int(file)
        self.FPotMoy = self.read_int(file)

        # Microscope SetUp
        tag_id = TAG_MICROSCOPE_SETUP
        if not self.find_tag(file, tag_id):
            raise IOError

        self.Beam_angle = self.read_double(file)
        self.Beam_Diameter = self.read_double(file)
        self.Electron_Number = self.read_long(file)
        self.KEV_End = self.read_double(file)
        self.KEV_Start = self.read_double(file)
        self.KEV_Step = self.read_double(file)

        self.Scan_Image = self.read_int(file)
        pos_end = self.read_double(file)
        self._positionEnd_nm = pos_end
        pos_start = self.read_double(file)
        self._positionStart_nm = pos_start
        # In CASINO pos_number_steps is the step length.
        pos_number_steps = self.read_double(file)
        self._positionStep_nm = pos_number_steps
        # In CASINO pos_step is the number of steps and not used.
        pos_step = self.read_double(file)
        self._positionNumberStep = pos_step

        if version >= 21:
            self.Scan_Energy = self.read_int(file)

        if version >= 25:
            self.UseEnBack = self.read_bool(file)
            self.WorkDist = self.read_double(file)
            self.DetectScaleX = self.read_double(file)
            self.DetectScaleY = self.read_double(file)

            if self.UseEnBack:
                self._matrixDetector = []
                for dummy1 in range(101):
                    row = []
                    for dummy2 in range(101):
                        value = self.read_double(file)
                        row.append(value)
                    self._matrixDetector.append(row)

        # XRay
        tag_id = TAG_XRAY
        if not self.find_tag(file, tag_id):
            raise IOError

        self.FEmissionRX = self.read_int(file)
        self.NbreCoucheRX = self.read_long(file)
        self.EpaisCouche = self.read_double(file)
        self.TOA = self.read_double(file)
        self.PhieRX = self.read_float(file)
        self.RkoMax = self.read_double(file)

        if version >= 22:
            self.RkoMaxW = self.read_double(file)

        # Simulation options
        tag_id = TAG_SMULATION_OPTIONS
        if not self.find_tag(file, tag_id):
            raise IOError

        self.Eminimum = self.read_double(file)
        self.Electron_Display = self.read_long(file)
        self.Electron_Save = self.read_long(file)
        self.Memory_Keep = self.read_int(file)
        self.First = self.read_int(file)
        self.Keep_Sim = self.read_int(file)

        # Display Options
        tag_id = TAG_DISPLAY_OPTIONS
        if not self.find_tag(file, tag_id):
            raise IOError

        self.Display_Colision = self.read_int(file)
        self.Display_Color = self.read_int(file)
        self.Display_Projection = self.read_int(file)
        self.Display_Back = self.read_int(file)
        self.Display_Refresh = self.read_int(file)
        self.Minimum_Trajectory_Display_Distance = self.read_double(file)

        # Region Info
        tag_id = TAG_REGION_INFO
        if not self.find_tag(file, tag_id):
            raise IOError

        self.FForme = self.read_int(file)
        self.Total_Thickness = self.read_double(file)
        self.Half_Width = self.read_double(file)

        # Energy by position
        if version >= 22:
            tag_id = TAG_ENERGY_POSITIONS
            if not self.find_tag(file, tag_id):
                raise IOError

            self.ShowFadedSqr = self.read_int(file)
            self.ShowRegions = self.read_int(file)
            self.SetPointstoRelativePosition = self.read_int(file)
            self.Summation = self.read_int(file)
            self.XZorXY = self.read_int(file)
            self.Yplane = self.read_int(file)
            self.Zplane = self.read_int(file)

        # Distribution selection
        tag_id = TAG_DISTRIBUTION_SELECTION
        if not self.find_tag(file, tag_id):
            raise IOError

        self.FDZmax = self.read_int(file)
        self.FDenr = self.read_int(file)
        self.FDent = self.read_int(file)
        self.FDPoire = self.read_int(file)
        self.FDrsr = self.read_int(file)
        self.FDrsrLit = self.read_int(file)
        self.FDncr = self.read_int(file)

        self.FDEpos = 0
        if version >= 22:
            self.FDEpos = self.read_int(file)

        if version >= 25:
            self.FDbang = self.read_int(file)

        if version >= 26:
            self.FDAngleVSEnergie = self.read_int(file)

        # Distribution points
        tag_id = TAG_DISTRIBUTION_POINTS
        if not self.find_tag(file, tag_id):
            raise IOError

        self.NbPointDZMax = self.read_long(file)
        self.NbPointDENR = self.read_long(file)
        self.NbPointDENT = self.read_long(file)
        self.NbPointDRSR = self.read_long(file)
        self.NbPointDNCR = self.read_long(file)

        if version >= 22:
            self.NbPointDEpos_X = self.read_long(file)
            self.NbPointDEpos_Y = self.read_long(file)
            self.NbPointDEpos_Z = self.read_long(file)

        if version >= 25:
            self.NbPointDBANG = self.read_long(file)

        if version >= 26:
            self.NbPointDAngleVSEnergie = self.read_long(file)

        if version >= 23:
            self.RangeFinder = self.read_int(file)
            self.RangeSafetyFactor = self.read_double(file)
            self.FixedRange = self.read_double(file)

        if version >= 24:
            self.BEMin_Angle = self.read_double(file)
            self.BEMax_Angle = self.read_double(file)

            self.FEFilter = self.read_int(file)
            self.EFilterMax = self.read_double(file)
            self.EFilterMin = self.read_double(file)

            self.EFilterVal = []
            for dummy in range(101):
                value = self.read_double(file)
                self.EFilterVal.append(value)

        if version >= 2040601:
            self.FDZmax = self.read_int(file)
            self.FDZmaxLog = self.read_int(file)
            self.NbPointDZMax = self.read_long(file)
            self.DZmaxMax = self.read_double(file)
            self.DZmaxMin = self.read_double(file)

            self.FDenr = self.read_int(file)
            self.FDenrLog = self.read_int(file)
            self.NbPointDENR = self.read_long(file)
            self.DenrMax = self.read_double(file)
            self.DenrMin = self.read_double(file)

            self.FDent = self.read_int(file)
            self.FDentLog = self.read_int(file)
            self.NbPointDENT = self.read_long(file)
            self.DentMax = self.read_double(file)
            self.DentMin = self.read_double(file)

            self.FDrsr = self.read_int(file)
            self.FDrsrLog = self.read_int(file)
            self.NbPointDRSR = self.read_long(file)
            self.DrsrMax = self.read_double(file)
            self.DrsrMin = self.read_double(file)

            self.FDbang = self.read_int(file)
            self.FDbangLog = self.read_int(file)
            self.NbPointDBANG = self.read_long(file)
            self.DbangMax = self.read_double(file)
            self.DbangMin = self.read_double(file)

            self.FDAngleVSEnergie = self.read_int(file)
            self.FDAngleVSEnergieLog = self.read_int(file)
            self.NbPointDAngleVSEnergie = self.read_long(file)
            self.DAngleVSEnergieMax = self.read_double(file)
            self.DAngleVSEnergieMin = self.read_double(file)

        # Interrupted Simulation Data
        tag_id = TAG_INTERRUPTED_SIMULATION_DATA
        if not self.find_tag(file, tag_id):
            raise IOError

        self.Eo = self.read_double(file)
        self.NoElec = self.read_long(file)
        self.PositionF_X = self.read_double(file)
        self.PositionF_Y = self.read_double(file)
        self.Theta0 = self.read_double(file)
        self.Phi0 = self.read_double(file)
        self.num_at = self.read_long(file)
        if version > 23:
            self.Tot_Ret = self.read_double(file)
        else:
            self.Tot_Ret = self.read_long(file)

        self.MinX = self.read_double(file)
        self.MinY = self.read_double(file)
        self.MinZ = self.read_double(file)
        self.MaxX = self.read_double(file)
        self.MaxY = self.read_double(file)
        self.MaxZ = self.read_double(file)
        self.NbCollMax = self.read_double(file)
        self.NbCollMax2 = self.read_double(file)
        self.RatioX = self.read_double(file)
        self.RatioY = self.read_double(file)
        self.RatioZ = self.read_double(file)

        if version >= 25:
            self.Tot_Ret_En = self.read_double(file)

        # Scale & grid data
        tag_id = TAG_SCALE_GRID
        if not self.find_tag(file, tag_id):
            raise IOError

        self.NumVtabs = self.read_int(file)
        self.NumHtabs = self.read_int(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tag_id = TAG_BSE_COEFFICIENT
        self.add_tag_old(file, tag_id)
        self.write_double(file, self._bseCoefficient)

        tag_id = TAG_PHYSIC_MODELS
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.FRan)
        self.write_int(file, self.FDeds)
        self.write_int(file, self.FSecTotal)
        self.write_int(file, self.FSecPartiel)
        self.write_int(file, self.FCosDirect)
        self.write_int(file, self.FSecIon)
        self.write_int(file, self.FPotMoy)

        tag_id = TAG_MICROSCOPE_SETUP
        self.add_tag_old(file, tag_id)
        self.write_double(file, self.Beam_angle)
        self.write_double(file, self.Beam_Diameter)
        self.write_long(file, self.Electron_Number)
        self.write_double(file, self.KEV_End)
        self.write_double(file, self.KEV_Start)
        self.write_double(file, self.KEV_Step)

        self.write_int(file, self.Scan_Image)
        pos_end = self._positionEnd_nm
        self.write_double(file, pos_end)
        pos_start = self._positionStart_nm
        self.write_double(file, pos_start)
        # In CASINO pos_number_steps is the step length.
        pos_number_steps = self._positionStep_nm
        self.write_double(file, pos_number_steps)
        # In CASINO pos_step is the number of steps and not used.
        pos_step = self._positionNumberStep
        self.write_double(file, pos_step)

        self.write_int(file, self.Scan_Energy)

        self.write_bool(file, self.UseEnBack)
        self.write_double(file, self.WorkDist)
        self.write_double(file, self.DetectScaleX)
        self.write_double(file, self.DetectScaleY)

        if self.UseEnBack:
            assert len(self._matrixDetector) == 101
            for index1 in range(101):
                row = self._matrixDetector[index1]
                assert len(row) == 101
                for index2 in range(101):
                    value = row[index2]
                    self.write_double(file, value)

        tag_id = TAG_XRAY
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.FEmissionRX)
        self.write_long(file, self.NbreCoucheRX)
        self.write_double(file, self.EpaisCouche)
        self.write_double(file, self.TOA)
        self.write_float(file, self.PhieRX)
        self.write_double(file, self.RkoMax)
        self.write_double(file, self.RkoMaxW)

        tag_id = TAG_SMULATION_OPTIONS
        self.add_tag_old(file, tag_id)
        self.write_double(file, self.Eminimum)
        self.write_long(file, self.Electron_Display)
        self.write_long(file, self.Electron_Save)
        self.write_int(file, self.Memory_Keep)
        self.write_int(file, self.First)
        self.write_int(file, self.Keep_Sim)

        tag_id = TAG_DISPLAY_OPTIONS
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.Display_Colision)
        self.write_int(file, self.Display_Color)
        self.write_int(file, self.Display_Projection)
        self.write_int(file, self.Display_Back)
        self.write_int(file, self.Display_Refresh)
        self.write_double(file, self.Minimum_Trajectory_Display_Distance)

        tag_id = TAG_REGION_INFO
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.FForme)
        self.write_double(file, self.Total_Thickness)
        self.write_double(file, self.Half_Width)

        tag_id = TAG_ENERGY_POSITIONS
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.ShowFadedSqr)
        self.write_int(file, self.ShowRegions)
        self.write_int(file, self.SetPointstoRelativePosition)
        self.write_int(file, self.Summation)
        self.write_int(file, self.XZorXY)
        self.write_int(file, self.Yplane)
        self.write_int(file, self.Zplane)

        tag_id = TAG_DISTRIBUTION_SELECTION
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.FDZmax)
        self.write_int(file, self.FDenr)
        self.write_int(file, self.FDent)
        self.write_int(file, self.FDPoire)
        self.write_int(file, self.FDrsr)
        self.write_int(file, self.FDrsrLit)
        self.write_int(file, self.FDncr)
        self.write_int(file, self.FDEpos)
        self.write_int(file, self.FDbang)
        self.write_int(file, self.FDAngleVSEnergie)

        tag_id = TAG_DISTRIBUTION_POINTS
        self.add_tag_old(file, tag_id)
        self.write_long(file, self.NbPointDZMax)
        self.write_long(file, self.NbPointDENR)
        self.write_long(file, self.NbPointDENT)
        self.write_long(file, self.NbPointDRSR)
        self.write_long(file, self.NbPointDNCR)

        self.write_long(file, self.NbPointDEpos_X)
        self.write_long(file, self.NbPointDEpos_Y)
        self.write_long(file, self.NbPointDEpos_Z)

        self.write_long(file, self.NbPointDBANG)

        self.write_long(file, self.NbPointDAngleVSEnergie)

        self.write_int(file, self.RangeFinder)
        self.write_double(file, self.RangeSafetyFactor)
        self.write_double(file, self.FixedRange)

        self.write_double(file, self.BEMin_Angle)
        self.write_double(file, self.BEMax_Angle)

        self.write_int(file, self.FEFilter)
        self.write_double(file, self.EFilterMax)
        self.write_double(file, self.EFilterMin)

        assert len(self.EFilterVal) == 101
        for index in range(101):
            self.write_double(file, self.EFilterVal[index])

        self.write_int(file, self.FDZmax)
        self.write_int(file, self.FDZmaxLog)
        self.write_long(file, self.NbPointDZMax)
        self.write_double(file, self.DZmaxMax)
        self.write_double(file, self.DZmaxMin)

        self.write_int(file, self.FDenr)
        self.write_int(file, self.FDenrLog)
        self.write_long(file, self.NbPointDENR)
        self.write_double(file, self.DenrMax)
        self.write_double(file, self.DenrMin)

        self.write_int(file, self.FDent)
        self.write_int(file, self.FDentLog)
        self.write_long(file, self.NbPointDENT)
        self.write_double(file, self.DentMax)
        self.write_double(file, self.DentMin)

        self.write_int(file, self.FDrsr)
        self.write_int(file, self.FDrsrLog)
        self.write_long(file, self.NbPointDRSR)
        self.write_double(file, self.DrsrMax)
        self.write_double(file, self.DrsrMin)

        self.write_int(file, self.FDbang)
        self.write_int(file, self.FDbangLog)
        self.write_long(file, self.NbPointDBANG)
        self.write_double(file, self.DbangMax)
        self.write_double(file, self.DbangMin)

        self.write_int(file, self.FDAngleVSEnergie)
        self.write_int(file, self.FDAngleVSEnergieLog)
        self.write_long(file, self.NbPointDAngleVSEnergie)
        self.write_double(file, self.DAngleVSEnergieMax)
        self.write_double(file, self.DAngleVSEnergieMin)

        tag_id = TAG_INTERRUPTED_SIMULATION_DATA
        self.add_tag_old(file, tag_id)
        self.write_double(file, self.Eo)
        self.write_long(file, self.NoElec)
        self.write_double(file, self.PositionF_X)
        self.write_double(file, self.PositionF_Y)
        self.write_double(file, self.Theta0)
        self.write_double(file, self.Phi0)
        self.write_long(file, self.num_at)
        self.write_double(file, self.Tot_Ret)

        self.write_double(file, self.MinX)
        self.write_double(file, self.MinY)
        self.write_double(file, self.MinZ)
        self.write_double(file, self.MaxX)
        self.write_double(file, self.MaxY)
        self.write_double(file, self.MaxZ)
        self.write_double(file, self.NbCollMax)
        self.write_double(file, self.NbCollMax2)
        self.write_double(file, self.RatioX)
        self.write_double(file, self.RatioY)
        self.write_double(file, self.RatioZ)

        self.write_double(file, self.Tot_Ret_En)

        tag_id = TAG_SCALE_GRID
        self.add_tag_old(file, tag_id)
        self.write_int(file, self.NumVtabs)
        self.write_int(file, self.NumHtabs)

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
        return self._bseCoefficient

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
