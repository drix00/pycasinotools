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
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

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
        if not self.findTag(file, tagID):
            raise IOError
        self._bseCoefficient = self.readDouble(file)

        # Selected Physical Model variables
        tagID = TAG_PHYSIC_MODELS
        if not self.findTag(file, tagID):
            raise IOError

        self.FRan = self.readInt(file)
        self.FDeds = self.readInt(file)
        self.FSecTotal = self.readInt(file)
        self.FSecPartiel = self.readInt(file)
        self.FCosDirect = self.readInt(file)
        self.FSecIon = self.readInt(file)
        self.FPotMoy = self.readInt(file)

        # Microscope SetUp
        tagID = TAG_MICROSCOPE_SETUP
        if not self.findTag(file, tagID):
            raise IOError

        self.Beam_angle = self.readDouble(file)
        self.Beam_Diameter = self.readDouble(file)
        self.Electron_Number = self.readLong(file)
        self.KEV_End = self.readDouble(file)
        self.KEV_Start = self.readDouble(file)
        self.KEV_Step = self.readDouble(file)

        self.Scan_Image = self.readInt(file)
        POS_End = self.readDouble(file)
        self._positionEnd_nm = POS_End
        POS_Start = self.readDouble(file)
        self._positionStart_nm = POS_Start
        # In CASINO POS_NStep is the step length.
        POS_NStep = self.readDouble(file)
        self._positionStep_nm = POS_NStep
        # In CASINO POS_Step is the number of steps and not used.
        POS_Step = self.readDouble(file)
        self._positionNumberStep = POS_Step

        if version >= 21:
            self.Scan_Energy = self.readInt(file)

        if version >= 25:
            self.UseEnBack = self.readBool(file)
            self.WorkDist = self.readDouble(file)
            self.DetectScaleX = self.readDouble(file)
            self.DetectScaleY = self.readDouble(file)

            if self.UseEnBack:
                self._matrixDetector = []
                for dummy1 in range(101):
                    row = []
                    for dummy2 in range(101):
                        value = self.readDouble(file)
                        row.append(value)
                    self._matrixDetector.append(row)

        # XRay
        tagID = TAG_XRAY
        if not self.findTag(file, tagID):
            raise IOError

        self.FEmissionRX = self.readInt(file)
        self.NbreCoucheRX = self.readLong(file)
        self.EpaisCouche = self.readDouble(file)
        self.TOA = self.readDouble(file)
        self.PhieRX = self.readFloat(file)
        self.RkoMax = self.readDouble(file)

        if version >= 22:
            self.RkoMaxW = self.readDouble(file)

        # Simulation options
        tagID = TAG_SMULATION_OPTIONS
        if not self.findTag(file, tagID):
            raise IOError

        self.Eminimum = self.readDouble(file)
        self.Electron_Display = self.readLong(file)
        self.Electron_Save = self.readLong(file)
        self.Memory_Keep = self.readInt(file)
        self.First = self.readInt(file)
        self.Keep_Sim = self.readInt(file)

        # Display Options
        tagID = TAG_DISPLAY_OPTIONS
        if not self.findTag(file, tagID):
            raise IOError

        self.Display_Colision = self.readInt(file)
        self.Display_Color = self.readInt(file)
        self.Display_Projection = self.readInt(file)
        self.Display_Back = self.readInt(file)
        self.Display_Refresh = self.readInt(file)
        self.Minimum_Trajectory_Display_Distance = self.readDouble(file)

        # Region Info
        tagID = TAG_REGION_INFO
        if not self.findTag(file, tagID):
            raise IOError

        self.FForme = self.readInt(file)
        self.Total_Thickness = self.readDouble(file)
        self.Half_Width = self.readDouble(file)

        # Energy by position
        if version >= 22:
            tagID = TAG_ENERGY_POSITIONS
            if not self.findTag(file, tagID):
                raise IOError

            self.ShowFadedSqr = self.readInt(file)
            self.ShowRegions = self.readInt(file)
            self.SetPointstoRelativePosition = self.readInt(file)
            self.Summation = self.readInt(file)
            self.XZorXY = self.readInt(file)
            self.Yplane = self.readInt(file)
            self.Zplane = self.readInt(file)

        # Distribution selection
        tagID = TAG_DISTRIBUTION_SELECTION
        if not self.findTag(file, tagID):
            raise IOError

        self.FDZmax = self.readInt(file)
        self.FDenr = self.readInt(file)
        self.FDent = self.readInt(file)
        self.FDPoire = self.readInt(file)
        self.FDrsr = self.readInt(file)
        self.FDrsrLit = self.readInt(file)
        self.FDncr = self.readInt(file)

        self.FDEpos = 0
        if version >= 22:
            self.FDEpos = self.readInt(file)

        if version >= 25:
            self.FDbang = self.readInt(file)

        if version >= 26:
            self.FDAngleVSEnergie = self.readInt(file)

        # Distribution points
        tagID = TAG_DISTRIBUTION_POINTS
        if not self.findTag(file, tagID):
            raise IOError

        self.NbPointDZMax = self.readLong(file)
        self.NbPointDENR = self.readLong(file)
        self.NbPointDENT = self.readLong(file)
        self.NbPointDRSR = self.readLong(file)
        self.NbPointDNCR = self.readLong(file)

        if version >= 22:
            self.NbPointDEpos_X = self.readLong(file)
            self.NbPointDEpos_Y = self.readLong(file)
            self.NbPointDEpos_Z = self.readLong(file)

        if version >= 25:
            self.NbPointDBANG = self.readLong(file)

        if version >= 26:
            self.NbPointDAngleVSEnergie = self.readLong(file)

        if version >= 23:
            self.RangeFinder = self.readInt(file)
            self.RangeSafetyFactor = self.readDouble(file)
            self.FixedRange = self.readDouble(file)

        if version >= 24:
            self.BEMin_Angle = self.readDouble(file)
            self.BEMax_Angle = self.readDouble(file)

            self.FEFilter = self.readInt(file)
            self.EFilterMax = self.readDouble(file)
            self.EFilterMin = self.readDouble(file)

            self.EFilterVal = []
            for dummy in range(101):
                value = self.readDouble(file)
                self.EFilterVal.append(value)

        if version >= 2040601:
            self.FDZmax = self.readInt(file)
            self.FDZmaxLog = self.readInt(file)
            self.NbPointDZMax = self.readLong(file)
            self.DZmaxMax = self.readDouble(file)
            self.DZmaxMin = self.readDouble(file)

            self.FDenr = self.readInt(file)
            self.FDenrLog = self.readInt(file)
            self.NbPointDENR = self.readLong(file)
            self.DenrMax = self.readDouble(file)
            self.DenrMin = self.readDouble(file)

            self.FDent = self.readInt(file)
            self.FDentLog = self.readInt(file)
            self.NbPointDENT = self.readLong(file)
            self.DentMax = self.readDouble(file)
            self.DentMin = self.readDouble(file)

            self.FDrsr = self.readInt(file)
            self.FDrsrLog = self.readInt(file)
            self.NbPointDRSR = self.readLong(file)
            self.DrsrMax = self.readDouble(file)
            self.DrsrMin = self.readDouble(file)

            self.FDbang = self.readInt(file)
            self.FDbangLog = self.readInt(file)
            self.NbPointDBANG = self.readLong(file)
            self.DbangMax = self.readDouble(file)
            self.DbangMin = self.readDouble(file)

            self.FDAngleVSEnergie = self.readInt(file)
            self.FDAngleVSEnergieLog = self.readInt(file)
            self.NbPointDAngleVSEnergie = self.readLong(file)
            self.DAngleVSEnergieMax = self.readDouble(file)
            self.DAngleVSEnergieMin = self.readDouble(file)

        # Interrupted Simulation Data
        tagID = TAG_INTERRUPTED_SIMULATION_DATA
        if not self.findTag(file, tagID):
            raise IOError

        self.Eo = self.readDouble(file)
        self.NoElec = self.readLong(file)
        self.PositionF_X = self.readDouble(file)
        self.PositionF_Y = self.readDouble(file)
        self.Theta0 = self.readDouble(file)
        self.Phi0 = self.readDouble(file)
        self.num_at = self.readLong(file)
        if version > 23:
            self.Tot_Ret = self.readDouble(file)
        else:
            self.Tot_Ret = self.readLong(file)

        self.MinX = self.readDouble(file)
        self.MinY = self.readDouble(file)
        self.MinZ = self.readDouble(file)
        self.MaxX = self.readDouble(file)
        self.MaxY = self.readDouble(file)
        self.MaxZ = self.readDouble(file)
        self.NbCollMax = self.readDouble(file)
        self.NbCollMax2 = self.readDouble(file)
        self.RatioX = self.readDouble(file)
        self.RatioY = self.readDouble(file)
        self.RatioZ = self.readDouble(file)

        if version >= 25:
            self.Tot_Ret_En = self.readDouble(file)

        # Scale & grid data
        tagID = TAG_SCALE_GRID
        if not self.findTag(file, tagID):
            raise IOError

        self.NumVtabs = self.readInt(file)
        self.NumHtabs = self.readInt(file)

    def write(self, file):
        assert getattr(file, 'mode', 'wb') == 'wb'
        logging.debug("File position at the start of %s.%s: %i", self.__class__.__name__, "write", file.tell())

        tagID = TAG_BSE_COEFFICIENT
        self.addTagOld(file, tagID)
        self.writeDouble(file, self._bseCoefficient)

        tagID = TAG_PHYSIC_MODELS
        self.addTagOld(file, tagID)
        self.writeInt(file, self.FRan)
        self.writeInt(file, self.FDeds)
        self.writeInt(file, self.FSecTotal)
        self.writeInt(file, self.FSecPartiel)
        self.writeInt(file, self.FCosDirect)
        self.writeInt(file, self.FSecIon)
        self.writeInt(file, self.FPotMoy)

        tagID = TAG_MICROSCOPE_SETUP
        self.addTagOld(file, tagID)
        self.writeDouble(file, self.Beam_angle)
        self.writeDouble(file, self.Beam_Diameter)
        self.writeLong(file, self.Electron_Number)
        self.writeDouble(file, self.KEV_End)
        self.writeDouble(file, self.KEV_Start)
        self.writeDouble(file, self.KEV_Step)

        self.writeInt(file, self.Scan_Image)
        POS_End = self._positionEnd_nm
        self.writeDouble(file, POS_End)
        POS_Start = self._positionStart_nm
        self.writeDouble(file, POS_Start)
        # In CASINO POS_NStep is the step length.
        POS_NStep = self._positionStep_nm
        self.writeDouble(file, POS_NStep)
        # In CASINO POS_Step is the number of steps and not used.
        POS_Step = self._positionNumberStep
        self.writeDouble(file, POS_Step)

        self.writeInt(file, self.Scan_Energy)

        self.writeBool(file, self.UseEnBack)
        self.writeDouble(file, self.WorkDist)
        self.writeDouble(file, self.DetectScaleX)
        self.writeDouble(file, self.DetectScaleY)

        if self.UseEnBack:
            assert len(self._matrixDetector) == 101
            for index1 in range(101):
                row = self._matrixDetector[index1]
                assert len(row) == 101
                for index2 in range(101):
                    value = row[index2]
                    self.writeDouble(file, value)

        tagID = TAG_XRAY
        self.addTagOld(file, tagID)
        self.writeInt(file, self.FEmissionRX)
        self.writeLong(file, self.NbreCoucheRX)
        self.writeDouble(file, self.EpaisCouche)
        self.writeDouble(file, self.TOA)
        self.writeFloat(file, self.PhieRX)
        self.writeDouble(file, self.RkoMax)
        self.writeDouble(file, self.RkoMaxW)

        tagID = TAG_SMULATION_OPTIONS
        self.addTagOld(file, tagID)
        self.writeDouble(file, self.Eminimum)
        self.writeLong(file, self.Electron_Display)
        self.writeLong(file, self.Electron_Save)
        self.writeInt(file, self.Memory_Keep)
        self.writeInt(file, self.First)
        self.writeInt(file, self.Keep_Sim)

        tagID = TAG_DISPLAY_OPTIONS
        self.addTagOld(file, tagID)
        self.writeInt(file, self.Display_Colision)
        self.writeInt(file, self.Display_Color)
        self.writeInt(file, self.Display_Projection)
        self.writeInt(file, self.Display_Back)
        self.writeInt(file, self.Display_Refresh)
        self.writeDouble(file, self.Minimum_Trajectory_Display_Distance)

        tagID = TAG_REGION_INFO
        self.addTagOld(file, tagID)
        self.writeInt(file, self.FForme)
        self.writeDouble(file, self.Total_Thickness)
        self.writeDouble(file, self.Half_Width)

        tagID = TAG_ENERGY_POSITIONS
        self.addTagOld(file, tagID)
        self.writeInt(file, self.ShowFadedSqr)
        self.writeInt(file, self.ShowRegions)
        self.writeInt(file, self.SetPointstoRelativePosition)
        self.writeInt(file, self.Summation)
        self.writeInt(file, self.XZorXY)
        self.writeInt(file, self.Yplane)
        self.writeInt(file, self.Zplane)

        tagID = TAG_DISTRIBUTION_SELECTION
        self.addTagOld(file, tagID)
        self.writeInt(file, self.FDZmax)
        self.writeInt(file, self.FDenr)
        self.writeInt(file, self.FDent)
        self.writeInt(file, self.FDPoire)
        self.writeInt(file, self.FDrsr)
        self.writeInt(file, self.FDrsrLit)
        self.writeInt(file, self.FDncr)
        self.writeInt(file, self.FDEpos)
        self.writeInt(file, self.FDbang)
        self.writeInt(file, self.FDAngleVSEnergie)

        tagID = TAG_DISTRIBUTION_POINTS
        self.addTagOld(file, tagID)
        self.writeLong(file, self.NbPointDZMax)
        self.writeLong(file, self.NbPointDENR)
        self.writeLong(file, self.NbPointDENT)
        self.writeLong(file, self.NbPointDRSR)
        self.writeLong(file, self.NbPointDNCR)

        self.writeLong(file, self.NbPointDEpos_X)
        self.writeLong(file, self.NbPointDEpos_Y)
        self.writeLong(file, self.NbPointDEpos_Z)

        self.writeLong(file, self.NbPointDBANG)

        self.writeLong(file, self.NbPointDAngleVSEnergie)

        self.writeInt(file, self.RangeFinder)
        self.writeDouble(file, self.RangeSafetyFactor)
        self.writeDouble(file, self.FixedRange)

        self.writeDouble(file, self.BEMin_Angle)
        self.writeDouble(file, self.BEMax_Angle)

        self.writeInt(file, self.FEFilter)
        self.writeDouble(file, self.EFilterMax)
        self.writeDouble(file, self.EFilterMin)

        assert len(self.EFilterVal) == 101
        for index in range(101):
            self.writeDouble(file, self.EFilterVal[index])

        self.writeInt(file, self.FDZmax)
        self.writeInt(file, self.FDZmaxLog)
        self.writeLong(file, self.NbPointDZMax)
        self.writeDouble(file, self.DZmaxMax)
        self.writeDouble(file, self.DZmaxMin)

        self.writeInt(file, self.FDenr)
        self.writeInt(file, self.FDenrLog)
        self.writeLong(file, self.NbPointDENR)
        self.writeDouble(file, self.DenrMax)
        self.writeDouble(file, self.DenrMin)

        self.writeInt(file, self.FDent)
        self.writeInt(file, self.FDentLog)
        self.writeLong(file, self.NbPointDENT)
        self.writeDouble(file, self.DentMax)
        self.writeDouble(file, self.DentMin)

        self.writeInt(file, self.FDrsr)
        self.writeInt(file, self.FDrsrLog)
        self.writeLong(file, self.NbPointDRSR)
        self.writeDouble(file, self.DrsrMax)
        self.writeDouble(file, self.DrsrMin)

        self.writeInt(file, self.FDbang)
        self.writeInt(file, self.FDbangLog)
        self.writeLong(file, self.NbPointDBANG)
        self.writeDouble(file, self.DbangMax)
        self.writeDouble(file, self.DbangMin)

        self.writeInt(file, self.FDAngleVSEnergie)
        self.writeInt(file, self.FDAngleVSEnergieLog)
        self.writeLong(file, self.NbPointDAngleVSEnergie)
        self.writeDouble(file, self.DAngleVSEnergieMax)
        self.writeDouble(file, self.DAngleVSEnergieMin)

        tagID = TAG_INTERRUPTED_SIMULATION_DATA
        self.addTagOld(file, tagID)
        self.writeDouble(file, self.Eo)
        self.writeLong(file, self.NoElec)
        self.writeDouble(file, self.PositionF_X)
        self.writeDouble(file, self.PositionF_Y)
        self.writeDouble(file, self.Theta0)
        self.writeDouble(file, self.Phi0)
        self.writeLong(file, self.num_at)
        self.writeDouble(file, self.Tot_Ret)

        self.writeDouble(file, self.MinX)
        self.writeDouble(file, self.MinY)
        self.writeDouble(file, self.MinZ)
        self.writeDouble(file, self.MaxX)
        self.writeDouble(file, self.MaxY)
        self.writeDouble(file, self.MaxZ)
        self.writeDouble(file, self.NbCollMax)
        self.writeDouble(file, self.NbCollMax2)
        self.writeDouble(file, self.RatioX)
        self.writeDouble(file, self.RatioY)
        self.writeDouble(file, self.RatioZ)

        self.writeDouble(file, self.Tot_Ret_En)

        tagID = TAG_SCALE_GRID
        self.addTagOld(file, tagID)
        self.writeInt(file, self.NumVtabs)
        self.writeInt(file, self.NumHtabs)

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
