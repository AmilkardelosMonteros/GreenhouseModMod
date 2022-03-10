#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:05:21 2022

@author: jdmolinam
"""

from ModMod import StateRHS
from .functions import s, mol_air, m, d, C, g, pa, ppm, mu_mol_O2, mu_mol_CO2, mu_mol_phot # importar simbolos 
from .functions import f_R, Sr, C_ev3, f_C, C_ev4, V_sa, VPD, f_V, r_s, gTC, Ca, W, mg # importar funciones

states = ['Ci', 'A', 'C1', 'RH', 'T1', 'I2'] 
constants = ['k_Ag', 'r_m', 'C_ev1', 'C_ev2', 'k_fc', 'C_ev3d', 'C_ev3n', 'S', 'Rs', 
        'C_ev4d', 'C_ev4n', 'ks', 'Rb', 'k_d', 'k_T', 'k_JV', 'fc', 'phi', 'O_a', 'V_cmax25', 
        'Q10_Vcmax', 'K_C25', 'Q10_KC', 'K_O25', 'Q10_KO', 'tau_25', 'Q10_tau', 'J_max', 'ab', 
        'f', 'theta']

all_parameters = states + constants

#################################################################
############ RHS del CO2 intracelular ###########################
#################################################################    

class Ci_rhs(StateRHS):
    """
    Ci es el CO2 intracelular 
    """
    def __init__( self, theta_p=[0.7, 3.3, 0.25]):
        super().__init__()
        self.SetSymbTimeUnits(d) # días
        ### Add variables ###
        ## State variables
        self.AddVarLocal( typ='State', varid='Ci', prn=r'$C_i$',\
                    desc="Intracellular CO2", units= ppm , val=410)
        
        self.AddVarLocal( typ='State', varid='A', prn=r'$A$',\
           desc="Assimilation rate", units= g * (m**-2), val=0)
        
        ## Inputs
        self.AddVar( typ='State', varid='C1', prn=r'$C_1$',\
                    desc="CO2 concentrartion in the greenhouse air", \
                    units= mg * m**-3 , val=429.3) ######################## -> NO REPETIR
        
        self.AddVar( typ='State', varid='RH', prn=r'$RH$',\
           desc="Relative humidity percentage in the greenhouse air", \
           units=1, val=50)
        
        self.AddVar( typ='State', varid='T1', prn=r'$T_1$',\
                    desc="Canopy temperature", units= C , val=20) # It's take as the leaves temperature
        
        #self.AddVar( typ='State', varid='PAR', prn=r'$PAR$',\
        #    desc="PAR radiation", units=mu_mol_phot * (m**-2) * d**-1 , val=300.00)
        self.AddVar( typ='State', varid='I2', prn=r'$I_2$',\
                    desc="External global radiation", units= W * m**-2 , val=100) # It's takes as the PAR 
         
        ## Canstants
        ### Stomatal Resistance Calculation
        self.AddVar( typ='Cnts', varid='k_Ag', \
           desc="Constant for units transformation", \
           units= m**3 * g**-1 * s**-1 * mu_mol_CO2 * mol_air**-1, val=1)
        
        self.AddVar( typ='Cnts', varid='r_m', \
           desc="minimal stomatal resistance", \
           units= s * m**-1, val=100)
        
        self.AddVar( typ='Cnts', varid='C_ev1', \
           desc="Constant in the formula of f_R", \
           units= mu_mol_phot * (m**-2) * d**-1, val=4.3)
        
        self.AddVar( typ='Cnts', varid='C_ev2', \
           desc="Constant in the formula of f_R", \
           units= mu_mol_phot * (m**-2) * d**-1 , val=0.54)
        
        self.AddVar( typ='Cnts', varid='k_fc', \
           desc="Constant for units completation", \
           units= mu_mol_CO2 * mol_air**-1, val=1)
        
        self.AddVar( typ='Cnts', varid='C_ev3d', \
           desc="Constant in the formula of f_C", \
           units= mol_air * mu_mol_CO2**-1, val=6.1e-7)
        
        self.AddVar( typ='Cnts', varid='C_ev3n', \
           desc="Constant in the formula of f_C", \
           units= mol_air * mu_mol_CO2**-1, val=1.1e-11)
        
        self.AddVar( typ='Cnts', varid='S', \
           desc="Constant in the formula of Sr", \
           units= m**2 * d * mu_mol_phot**-1, val=-1)
        
        self.AddVar( typ='Cnts', varid='Rs', \
           desc="Radiation setpoint to switch day and night", \
           units= mu_mol_phot * (m**-2) * d**-1, val=5)
        
        self.AddVar( typ='Cnts', varid='C_ev4d', \
           desc="Constant in the formula of f_C", \
           units= pa**-1, val=4.3e-6)
        
        self.AddVar( typ='Cnts', varid='C_ev4n', \
           desc="Constant in the formula of f_C", \
           units= pa**-1, val=5.2e-6)
        
        ## CO2 absorption
        self.AddVar( typ='Cnts', varid='ks', \
           desc="Stomatal ratio", \
           units= 1, val=0.5)
        
        self.AddVar( typ='Cnts', varid='Rb', \
           desc="Stomatal resistance of the canopy boundary layer", \
           units= s * m**-1, val=711)
        
        ## Assimilates
        self.AddVar( typ='Cnts', varid='k_d', \
           desc="factor to transform s**-1 into d**-1", units=1, val=1)
        
        self.AddVar( typ='Cnts', varid='k_T', \
           desc="Auxiliary constant to add temperature units", units= C, val=1.0)
        
        self.AddVar( typ='Cnts', varid='k_JV', \
           desc="Auxiliary constant which transforms the units of the electron transport rate, J to those of the maximum Rubisco rate, V_cmax", \
           units= mu_mol_CO2 * mu_mol_phot**-1, val=1.0)
        
        self.AddVar( typ='Cnts', varid='fc', \
           desc="Factor to transform mu-mols_CO2/sec to grms_CH20/day", \
           units= g * d * mu_mol_CO2**-1 , val=3.418181e-1) # 7.891414141414142e-6
        
        self.AddVar( typ='Cnts', varid='phi', \
           desc="Ratio of oxigenation to carboxylation rates", \
           units= mu_mol_O2 * mu_mol_CO2**-1, val=2)
        
        self.AddVar( typ='Cnts', varid='O_a', \
           desc="O2 concentration in the enviroment", \
           units= mu_mol_O2 * mol_air**-1, val=210000)
        
        self.AddVar( typ='Cnts', varid='V_cmax25', \
           desc="Maximum Rubisco Rate, per unit area", \
           units= mu_mol_CO2 * (m**-2) * d**-1, val=200)
        
        self.AddVar( typ='Cnts', varid='Q10_Vcmax', \
           desc="Temperatura response of Vcmax", \
           units=1, val=2.4)
        
        self.AddVar( typ='Cnts', varid='K_C25', \
           desc="Michaelis-Menten for CO2", \
           units= mu_mol_CO2 * mol_air**-1 , val=300)
        
        self.AddVar( typ='Cnts', varid='Q10_KC', \
           desc="Temperatura response of Michaelis-Menten for CO2", \
           units=1, val=2.1)
        
        self.AddVar( typ='Cnts', varid='K_O25', \
           desc="Michaelis-Menten for O2", \
           units= mu_mol_O2 * mol_air**-1 , val=3e5)
        
        self.AddVar( typ='Cnts', varid='Q10_KO', \
           desc="Temperatura response of Michaelis-Menten for O2", \
           units=1, val=1.2) 
        
        self.AddVar( typ='Cnts', varid='tau_25', \
           desc="Specificity factor", \
           units=1 , val=2600)
        
        self.AddVar( typ='Cnts', varid='Q10_tau', \
           desc="Temperatura response of specificity factor", \
           units=1, val=2.1) 
        
        self.AddVar( typ='Cnts', varid='J_max', \
           desc="Maximum electron transport rate", \
           units= mu_mol_phot * (m**-2) * d**-1, val=400)
        
        self.AddVar( typ='Cnts', varid='ab', \
           desc="Leafs absorbance", \
           units=1 , val=0.85)
        
        self.AddVar( typ='Cnts', varid='f', \
           desc="Correction factor for the spectral quality of the light", \
           units=1 , val=0.15)
        
        self.AddVar( typ='Cnts', varid='theta', \
           desc="Empirical factor", \
           units=1 , val=theta_p[0])
    
    
    def RHS( self, Dt):
        """RHS( Dt ) = \kappa_1^{-1} F_1( t+Dt, X+k) where X is the current value of
           all state variables.  k is a simple dictionary { 'v1':k1, 'v2':k2 ... etc}
           
           ************* JUST CALL STATE VARIABLES WITH self.Vk ******************
           
           Use from ModMod TranslateArgNames() for guide you how call the functions 
        """
        ## Cálculos de la resitencia estomática
        f_R1 = f_R( I=self.V('I2'), C_ev1=self.V('C_ev1'), C_ev2=self.V('C_ev2') )
        Sr1 = Sr( I=self.V('I2'), S=self.V('S'), Rs=self.V('Rs') )
        C_ev31 = C_ev3( C_ev3n=self.V('C_ev3n'), C_ev3d=self.V('C_ev3d'), Sr=Sr1 )
        f_C1 = f_C( C_ev3=C_ev31, C1=self.V('C1'), k_fc=self.V('k_fc') ) 
        C_ev41 = C_ev4( C_ev4n=self.V('C_ev4n'), C_ev4d=self.V('C_ev4d'), Sr=Sr1 )
        V_sa1 = V_sa( T =self.V('T1') )
        VPD1 = VPD( V_sa=V_sa1, RH=self.V('RH') )
        f_V1 = f_V( C_ev4=C_ev41, VPD = VPD1)
        R_s1 = r_s( r_m=self.V('r_m'), f_R=f_R1, f_C=f_C1, f_V=f_V1, k_d=self.V('k_d') ) 
        ## Cálculos absorción de CO2
        g_s = gTC( k=self.V('ks'), Rb=self.V('Rb'), Rs=R_s1, k_d=self.V('k_d') )
        Ca1 = Ca( gtc=g_s, C=self.V('C1'), Ci=self.Vk('Ci') )
        Dt_Ci = ( Ca1 - (1e-3)*self.V('A') )/0.554 # Los asimilados se pasan a mg/m**2 y el incremento del Ci queda en ppm
        return Dt_Ci
