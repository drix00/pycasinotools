#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import logging

# Third party modules.

# Local modules.
import casinotools.fileformat.file_reader_writer_tools as FileReaderWriterTools

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

def getDirectionCosinesString(type):
    if type == DIRECTION_COSINES_SOUM:
        return 'Soum et al.'
    elif type == DIRECTION_COSINES_DROUIN:
        return 'Drouin'
    else:
        raise ValueError('Unknown direction cosines')

CROSS_SECTION_MOTT_JOY = 0
CROSS_SECTION_MOTT_EQUATION = 1
CROSS_SECTION_MOTT_BROWNING = 2
CROSS_SECTION_MOTT_RUTHERFORD = 3

def getElasticCrossSectionTypeString(type):
    if type == CROSS_SECTION_MOTT_JOY:
        return "Czyzewski"
    elif type == CROSS_SECTION_MOTT_EQUATION:
        return "Drouin"
    elif type == CROSS_SECTION_MOTT_BROWNING:
        return "Browning"
    elif type == CROSS_SECTION_MOTT_RUTHERFORD:
        return "Rutherford"
    else:
        raise ValueError('Unknown elastic cross section')

IONIZATION_CROSS_SECTION_GAUVIN = 0
IONIZATION_CROSS_SECTION_POUCHOU = 1
IONIZATION_CROSS_SECTION_BROWN_POWELL = 2
IONIZATION_CROSS_SECTION_CASNATI = 3
IONIZATION_CROSS_SECTION_GRYZINSKI = 4
IONIZATION_CROSS_SECTION_JAKOBY = 5

def getIonizationCrossSectionTypeString(type):
    if type == IONIZATION_CROSS_SECTION_GAUVIN:
        return "Gauvin"
    elif type == IONIZATION_CROSS_SECTION_POUCHOU:
        return "Pouchou"
    elif type == IONIZATION_CROSS_SECTION_BROWN_POWELL:
        return "BrownPowell"
    elif type == IONIZATION_CROSS_SECTION_CASNATI:
        return "Casnati"
    elif type == IONIZATION_CROSS_SECTION_GRYZINSKI:
        return "Gryzinski"
    elif type == IONIZATION_CROSS_SECTION_JAKOBY:
        return "Jakoby"
    else:
        raise ValueError('Unknown ionization cross section')

IONIZATION_POTENTIAL_JOY = 0
IONIZATION_POTENTIAL_BERGER = 1
IONIZATION_POTENTIAL_HOVINGTON = 2

def getIonizationPotentialTypeString(type):
    if type == IONIZATION_POTENTIAL_JOY:
        return "Joy"
    elif type == IONIZATION_POTENTIAL_BERGER:
        return "Berger"
    elif type == IONIZATION_POTENTIAL_HOVINGTON:
        return "Hovington"
    else:
        raise ValueError('Unknown ionization potential')

RANDOM_NUMBER_GENERATOR_PRESS_ET_AL = 0
RANDOM_NUMBER_GENERATOR_MERSENNE_TWISTER = 1

def getRandomNumberGeneratorString(type):
    if type == RANDOM_NUMBER_GENERATOR_PRESS_ET_AL:
        return 'Press et al.'
    elif type == RANDOM_NUMBER_GENERATOR_MERSENNE_TWISTER:
        return 'Mersenne - Twister'
    else:
        raise ValueError("Unknown random number generator")

ENERGY_LOSS_JOY_LUO = 0

def getEnergyLossString(type):
    if type == ENERGY_LOSS_JOY_LUO:
        return 'Joy and Luo'
    else:
        raise ValueError('Unknown energy loss')

class SimulationOptions(FileReaderWriterTools.FileReaderWriterTools):
    def read(self, file, version):
        assert getattr(file, 'mode', 'rb') == 'rb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "read", file.tell())

        tagID = TAG_BSE_COEFFICIENT
        if not self.find_tag(file, tagID):
            raise IOError
        self._bseCoefficient = self.read_double(file)

        # Selected Physical Model variables
        tagID = TAG_PHYSIC_MODELS
        if not self.find_tag(file, tagID):
            raise IOError

        self.FRan = self.read_int(file)
        self.FDeds = self.read_int(file)
        self.FSecTotal = self.read_int(file)
        self.FSecPartiel = self.read_int(file)
        self.FCosDirect = self.read_int(file)
        self.FSecIon = self.read_int(file)
        self.FPotMoy = self.read_int(file)

        # Microscope SetUp
        tagID = TAG_MICROSCOPE_SETUP
        if not self.find_tag(file, tagID):
            raise IOError

        self.Beam_angle = self.read_double(file)
        self.Beam_Diameter = self.read_double(file)
        self.Electron_Number = self.read_long(file)
        self.KEV_End = self.read_double(file)
        self.KEV_Start = self.read_double(file)
        self.KEV_Step = self.read_double(file)

        self.Scan_Image = self.read_int(file)
        POS_End = self.read_double(file)
        self._positionEnd_nm = POS_End
        POS_Start = self.read_double(file)
        self._positionStart_nm = POS_Start
        # In CASINO POS_NStep is the step length.
        POS_NStep = self.read_double(file)
        self._positionStep_nm = POS_NStep
        # In CASINO POS_Step is the number of steps and not used.
        POS_Step = self.read_double(file)
        self._positionNumberStep = POS_Step

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
        tagID = TAG_XRAY
        if not self.find_tag(file, tagID):
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
        tagID = TAG_SMULATION_OPTIONS
        if not self.find_tag(file, tagID):
            raise IOError

        self.Eminimum = self.read_double(file)
        self.Electron_Display = self.read_long(file)
        self.Electron_Save = self.read_long(file)
        self.Memory_Keep = self.read_int(file)
        self.First = self.read_int(file)
        self.Keep_Sim = self.read_int(file)

        # Display Options
        tagID = TAG_DISPLAY_OPTIONS
        if not self.find_tag(file, tagID):
            raise IOError

        self.Display_Colision = self.read_int(file)
        self.Display_Color = self.read_int(file)
        self.Display_Projection = self.read_int(file)
        self.Display_Back = self.read_int(file)
        self.Display_Refresh = self.read_int(file)
        self.Minimum_Trajectory_Display_Distance = self.read_double(file)

        # Region Info
        tagID = TAG_REGION_INFO
        if not self.find_tag(file, tagID):
            raise IOError

        self.FForme = self.read_int(file)
        self.Total_Thickness = self.read_double(file)
        self.Half_Width = self.read_double(file)

        # Energy by position
        if version >= 22:
            tagID = TAG_ENERGY_POSITIONS
            if not self.find_tag(file, tagID):
                raise IOError

            self.ShowFadedSqr = self.read_int(file)
            self.ShowRegions = self.read_int(file)
            self.SetPointstoRelativePosition = self.read_int(file)
            self.Summation = self.read_int(file)
            self.XZorXY = self.read_int(file)
            self.Yplane = self.read_int(file)
            self.Zplane = self.read_int(file)

        # Distribution selection
        tagID = TAG_DISTRIBUTION_SELECTION
        if not self.find_tag(file, tagID):
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
        tagID = TAG_DISTRIBUTION_POINTS
        if not self.find_tag(file, tagID):
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
        tagID = TAG_INTERRUPTED_SIMULATION_DATA
        if not self.find_tag(file, tagID):
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
        tagID = TAG_SCALE_GRID
        if not self.find_tag(file, tagID):
            raise IOError

        self.NumVtabs = self.read_int(file)
        self.NumHtabs = self.read_int(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tagID = TAG_BSE_COEFFICIENT
        self.add_tag_old(file, tagID)
        self.write_double(file, self._bseCoefficient)

        tagID = TAG_PHYSIC_MODELS
        self.add_tag_old(file, tagID)
        self.write_int(file, self.FRan)
        self.write_int(file, self.FDeds)
        self.write_int(file, self.FSecTotal)
        self.write_int(file, self.FSecPartiel)
        self.write_int(file, self.FCosDirect)
        self.write_int(file, self.FSecIon)
        self.write_int(file, self.FPotMoy)

        tagID = TAG_MICROSCOPE_SETUP
        self.add_tag_old(file, tagID)
        self.write_double(file, self.Beam_angle)
        self.write_double(file, self.Beam_Diameter)
        self.write_long(file, self.Electron_Number)
        self.write_double(file, self.KEV_End)
        self.write_double(file, self.KEV_Start)
        self.write_double(file, self.KEV_Step)

        self.write_int(file, self.Scan_Image)
        POS_End = self._positionEnd_nm
        self.write_double(file, POS_End)
        POS_Start = self._positionStart_nm
        self.write_double(file, POS_Start)
        # In CASINO POS_NStep is the step length.
        POS_NStep = self._positionStep_nm
        self.write_double(file, POS_NStep)
        # In CASINO POS_Step is the number of steps and not used.
        POS_Step = self._positionNumberStep
        self.write_double(file, POS_Step)

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

        tagID = TAG_XRAY
        self.add_tag_old(file, tagID)
        self.write_int(file, self.FEmissionRX)
        self.write_long(file, self.NbreCoucheRX)
        self.write_double(file, self.EpaisCouche)
        self.write_double(file, self.TOA)
        self.write_float(file, self.PhieRX)
        self.write_double(file, self.RkoMax)
        self.write_double(file, self.RkoMaxW)

        tagID = TAG_SMULATION_OPTIONS
        self.add_tag_old(file, tagID)
        self.write_double(file, self.Eminimum)
        self.write_long(file, self.Electron_Display)
        self.write_long(file, self.Electron_Save)
        self.write_int(file, self.Memory_Keep)
        self.write_int(file, self.First)
        self.write_int(file, self.Keep_Sim)

        tagID = TAG_DISPLAY_OPTIONS
        self.add_tag_old(file, tagID)
        self.write_int(file, self.Display_Colision)
        self.write_int(file, self.Display_Color)
        self.write_int(file, self.Display_Projection)
        self.write_int(file, self.Display_Back)
        self.write_int(file, self.Display_Refresh)
        self.write_double(file, self.Minimum_Trajectory_Display_Distance)

        tagID = TAG_REGION_INFO
        self.add_tag_old(file, tagID)
        self.write_int(file, self.FForme)
        self.write_double(file, self.Total_Thickness)
        self.write_double(file, self.Half_Width)

        tagID = TAG_ENERGY_POSITIONS
        self.add_tag_old(file, tagID)
        self.write_int(file, self.ShowFadedSqr)
        self.write_int(file, self.ShowRegions)
        self.write_int(file, self.SetPointstoRelativePosition)
        self.write_int(file, self.Summation)
        self.write_int(file, self.XZorXY)
        self.write_int(file, self.Yplane)
        self.write_int(file, self.Zplane)

        tagID = TAG_DISTRIBUTION_SELECTION
        self.add_tag_old(file, tagID)
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

        tagID = TAG_DISTRIBUTION_POINTS
        self.add_tag_old(file, tagID)
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

        tagID = TAG_INTERRUPTED_SIMULATION_DATA
        self.add_tag_old(file, tagID)
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

        tagID = TAG_SCALE_GRID
        self.add_tag_old(file, tagID)
        self.write_int(file, self.NumVtabs)
        self.write_int(file, self.NumHtabs)

    def setNumberElectrons(self, numberElectrons):
        self.Electron_Number = numberElectrons

    def getNumberElectrons(self):
        return self.Electron_Number

    def setIncidentEnergy_keV(self, energy_keV):
        if self.Scan_Energy == False:
            self.KEV_End = energy_keV
            self.KEV_Step = 1.0

        self.KEV_Start = energy_keV

    def getIncidentEnergy_keV(self, index=None):
        if index == None:
            return self.KEV_Start
        else:
            incidentEnergy_keV = self.KEV_Start + index * self.KEV_Step
            if incidentEnergy_keV <= self.KEV_End:
                return incidentEnergy_keV
            else:
                raise ValueError

    def setTOA_deg(self, toa_deg):
        self.TOA = toa_deg

    def getTOA_deg(self):
        return self.TOA

    def setBeamAngle_deg(self, beamAngle_deg):
        self.Beam_angle = beamAngle_deg

    def getBeamAngle_deg(self):
        return self.TOA

    def getNumberXRayLayers(self):
        return self.NbreCoucheRX

    def setDirectionCosines(self, directionCosinesModel):
        self.FCosDirect = directionCosinesModel

    def getDirectionCosines(self):
        return self.FCosDirect

    def setTotalElectronElasticCrossSection(self, crossSectionModel):
        self.FSecTotal = crossSectionModel

    def getTotalElectronElasticCrossSection(self):
        return self.FSecTotal

    def setPartialElectronElasticCrossSection(self, crossSectionModel):
        self.FSecPartiel = crossSectionModel

    def getPartialElectronElasticCrossSection(self):
        return self.FSecPartiel

    def setElasticCrossSectionType(self, crossSectionModel):
        self.FSecTotal = crossSectionModel
        self.FSecPartiel = crossSectionModel

    def setIonizationCrossSectionType(self, type):
        self.FSecIon = type

    def getIonizationCrossSectionType(self):
        return self.FSecIon

    def setIonizationPotentialType(self, type):
        self.FPotMoy = type

    def getIonizationPotentialType(self):
        return self.FPotMoy

    def setRandomNumberGeneratorType(self, type):
        self.FRan = type

    def getRandomNumberGeneratorType(self):
        return self.FRan

    def setEnergyLossType(self, type):
        self.FDeds = type

    def getEnergyLossType(self):
        return self.FDeds

    def setTotalThickness_nm(self, totalThickness_nm):
        self.Total_Thickness = totalThickness_nm

    def getBseCoefficient(self):
        return self._bseCoefficient

    def getLinescanParameters(self):
        parameters = (self._positionStart_nm, self._positionEnd_nm, self._positionNumberStep, self._positionStep_nm)
        return parameters

    def setLinescanParameters(self, start_nm, end_nm, step_nm):
        """
        Sets the linescan parameters.
        If the beam is stationary, use :meth:`.setPosition` instead.

        .. note::

           The CASINO v2 code is very bad with naming variables.
           The POS_NStep is actually the step length and the POS_Step is not used.
           The correct variable are used in the read and write methods.

        :arg start_nm: start position (in nm)
        :arg end_nm: end position (in nm)
        :arg step_nm: step length (in nm)
        """
        nstep = (end_nm - start_nm) / step_nm

        self.Scan_Image = 1 # Turn on the line scan mode
        self._positionStart_nm = start_nm
        self._positionEnd_nm = end_nm
        self._positionNumberStep = nstep
        self._positionStep_nm = step_nm

    def setPosition(self, pos_nm):
        """
        Sets the position of the beam.

        :arg pos_nm: position of the beam (in nm)
        """
        self.Scan_Image = 0 # Turn off the line scan mode
        self._positionStart_nm = pos_nm
        self._positionEnd_nm = pos_nm
        self._positionNumberStep = 1
        self._positionStep_nm = 1.0 # Cannot be 0.0 as Casino2 returns "Out of memory" error

    def getMaximumDepth_nm(self):
        return self.RkoMax

    def getMaximumLateralWidth(self):
        return self.RkoMaxW
