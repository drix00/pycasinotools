#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.
import casinotools.fileformat.FileReaderWriterTools as FileReaderWriterTools

# Globals and constants variables.
#-----------------------------------------------------------------------------
#/ Filename to store the defaults settings
#-----------------------------------------
OPTIONS_PHYSIC_DEF_FILENAME = "PhysicModel_Settings_Defaults.dat"
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ Random number generator choice const declaration
#-----------------------------------------------------------------------------
RAND_PRESS = 0
RAND_MTOLD = 1
RAND_MT19937 = 2
RAND_LF607 = 3
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ dEdS consts
#-----------------------------------------------------------------------------
DEDS_JOYK_GAUVIN = 0
DEDS_JOYLUO_MONSEL = 1
DEDS_BETHERELATIVISTE = 2
#-----------------------------------------------------------------------------


# Electron elastic cross section.
CS_MOTT_FICHIER = 0
CS_MOTT_EQ = 1
CS_MOTT_BROWNING = 2
CS_RUTHE = 3
CS_REIMER = 4
CS_ELSEPA = 5

def getElectronElasticCrossSectionModelLabel(csModel):
        csModel = int(csModel)
        if csModel == CS_MOTT_FICHIER:
                return "Mott Interpolation"
        elif csModel == CS_MOTT_EQ:
                return "Mott eq. Drouin"
        elif csModel == CS_MOTT_BROWNING:
                return "Mott eq. Browning"
        elif csModel == CS_RUTHE:
                return "Rutherford"
        elif csModel == CS_REIMER:
                return "Rutherford Reimer"
        elif csModel == CS_ELSEPA:
                return "Mott Salvat"
        else:
                raise ValueError

#-----------------------------------------------------------------------------
#/ partial cross section consts
#-----------------------------------------------------------------------------
PCS_MOTT_FICHIER = 0
PCS_MOTT_EQ = 1
PCS_MOTT_BROWNING = 2
PCS_RUTHE = 3
PCS_REIMER = 4
PCS_ELSEPA = 5
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ total cross section consts
#-----------------------------------------------------------------------------
TCS_MOTT_FICHIER = 0
TCS_MOTT_EQ = 1
TCS_MOTT_BROWNING = 2
TCS_RUTHE = 3
TCS_REIMER = 4
TCS_ELSEPA = 5
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ inionisation potential
#-----------------------------------------------------------------------------
ION_POT_JOY = 0
ION_POT_BERGER = 1
ION_POT_PH = 2
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ Directing Cosine
#-----------------------------------------------------------------------------
COS_DIRECT_SOUM = 0
COS_DIRECT_MONSEL = 1
COS_DIRECT_DROUIN = 2
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ Effective Ionisation Section
#-----------------------------------------------------------------------------
SEC_ION_GAUVIN = 0
SEC_ION_POUCHOU = 1
SEC_ION_BROWN_POWELL = 2
SEC_ION_CASNATI = 3
SEC_ION_GRYZINSKI = 4
SEC_ION_JAKOBY = 5
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#/ Default value for some options
#-----------------------------------------------------------------------------
MIN_ENERGY_NOSEC_DEFAULT = 0.05
#-----------------------------------------------------------------------------

class OptionsPhysic(FileReaderWriterTools.FileReaderWriterTools):
##-----------------------------------------------------------------------------
##/ Residual energy loss used in the Monsel algorithm of De/Ds calculation.
##/ The goal is to account for energy loss not included in the original
##/ continual energy loss equation (Bethe algorithm in Monsel). This value
##/ should change depending on the sample elements and has a dramatic effect
##/ on secondary electron yield.
##-----------------------------------------------------------------------------
#    double Residual_Energy_Loss
##-----------------------------------------------------------------------------
##/ Minimum energy of the electron in keV.
##/ Used to determine when to stop using the electron. Not used in Monsel (secondary electron)
##/ simulation : different calculation permit us to use a lower value :
##/ (Trajectory_Collision::Region_Info::ect).
##-----------------------------------------------------------------------------
#    double Min_Energy_Nosec
##-----------------------------------------------------------------------------
##/ Minimum energy of an electron.
##/ Will usually be set to the working function of a region, but it can
##/ be overided by the user. To use the working function value, leave it
##/ to <= 0. Derived from Monsel code.
##/ @date 23 October 2003
##/ @author Dany Joly
##-----------------------------------------------------------------------------
#    double Min_Energy_With_Sec
##-----------------------------------------------------------------------------
##/ Minimum energy for a newly generated secondary electron.
##/ Will usually be set to the working function of a region, but it can
##/ be overided by the user. To use the working function value, leave it
##/ to <= 0. Derived from Monsel code
##/ @date 23 October 2003
##/ @author Dany Joly
##-----------------------------------------------------------------------------
#    double Min_Gen_Secondary_Energy
##-----------------------------------------------------------------------------
#
#
##/--------------------------------------
## Physical models flags
##/--------------------------------------
#
##-----------------------------------------------------------------------------
##/ choix du generateur de nombre aleatoires.
##/ appelle ran3 (numerical recipes) si =0, appelle mersenne twister si =1
##-----------------------------------------------------------------------------
#    int FRan
##-----------------------------------------------------------------------------
##/ Flag for the energy lost equation :
##/ - 0 JoyKCst de Gauvin
##/ - 1 Bethe Relativiste
##-----------------------------------------------------------------------------
#    int FDeds
##-----------------------------------------------------------------------------
##/ Flag for the total cross section :
##/ - 0 Mott par interpolation (fichiers, rapide)
##/ - 1 Mott equations de Drouin et Gauvin
##/ - 2 Mott equations de Browning
##/ - 3 Rutherford par Murata
##-----------------------------------------------------------------------------
#    int FTotalCross
##-----------------------------------------------------------------------------
##/ Flag for the partial cross section :
##/ - 0 Mott par interpolation (fichiers, rapide)
##/ - 1 Mott equations de Drouin et Gauvin
##/ - 2 Mott equations de Browning
##/ - 3 Rutherford par Murata
##-----------------------------------------------------------------------------
#    int FPartialCross
##-----------------------------------------------------------------------------
##/ Flag for directing cosin
##-----------------------------------------------------------------------------
#    int FCosDirect
##-----------------------------------------------------------------------------
##/ Flag for ionisation section
##-----------------------------------------------------------------------------
#    int FSecIon
##-----------------------------------------------------------------------------
##/Flag for Average Potential
##-----------------------------------------------------------------------------
#    int FPotMoy
##-----------------------------------------------------------------------------
#
##--------------------------------------
## Physical models options
##--------------------------------------
#
##-----------------------------------------------------------------------------
##/ Nombre maximal de niveau d'electrons secondaires pouvant etre crees.
##/ Niveaux
##/ - 1 : Primaires
##/ - 2 : Secondaires
##/ - 3 : Tertiaires
##-----------------------------------------------------------------------------
#    int max_secondary_order
##-----------------------------------------------------------------------------
    def __init__(self):
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

    def read(self, file):
        tagID = b"*PHYS_MOD_BEG"
        self.findTag(file, tagID)

        self._version = self.readInt(file)

        self.FRan = self.readInt(file)
        self.FDeds = self.readInt(file)
        self.FTotalCross = self.readInt(file)
        self.FPartialCross = self.readInt(file)
        self.FCosDirect = self.readInt(file)
#        FCosDirect = COS_DIRECT_MONSEL #Other Cos Direct are flawed for now
        self.FSecIon = self.readInt(file)
        self.FPotMoy = self.readInt(file)

        self.max_secondary_order = self.readInt(file)
        self.Min_Energy_Nosec = self.readDouble(file)
        self.Residual_Energy_Loss = self.readDouble(file)
        self.Min_Energy_With_Sec = self.readDouble(file)
        self.Min_Gen_Secondary_Energy = self.readDouble(file)

        tagID = b"*PHYS_MOD_END"
        self.findTag(file, tagID)

    def reset(self):
        self.FRan = 0
        self.FDeds = DEDS_JOYK_GAUVIN
        self.FTotalCross = TCS_MOTT_FICHIER
        self.FPartialCross = PCS_MOTT_FICHIER
        self.FCosDirect = COS_DIRECT_MONSEL
        self.FSecIon = SEC_ION_CASNATI
        self.FPotMoy = ION_POT_JOY

        self.max_secondary_order = 10
        self.Min_Energy_Nosec = MIN_ENERGY_NOSEC_DEFAULT
        self.Residual_Energy_Loss = 0.0004
        self.Min_Energy_With_Sec = -1.0
        self.Min_Gen_Secondary_Energy = -1.0

    def IsMonselSettings(self):
        return self.FCosDirect == COS_DIRECT_MONSEL and self.FDeds == DEDS_JOYLUO_MONSEL and self.FPartialCross == PCS_MOTT_BROWNING and self.FTotalCross == TCS_MOTT_BROWNING and self.FPotMoy == ION_POT_JOY

    def SetToMonselSettings(self):
        self.FCosDirect = COS_DIRECT_MONSEL
        self.FDeds = DEDS_JOYLUO_MONSEL
        self.FPartialCross = PCS_MOTT_BROWNING
        self.FTotalCross = TCS_MOTT_BROWNING
        self.FPotMoy = ION_POT_JOY

    def isInterpolation(self):
        return self.FTotalCross == TCS_MOTT_FICHIER or self.FTotalCross == TCS_ELSEPA or self.FPartialCross == PCS_MOTT_FICHIER or self.FPartialCross == PCS_ELSEPA
