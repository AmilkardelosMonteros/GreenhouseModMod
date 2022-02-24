#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:05:21 2022

@author: jdmolinam
"""

from ModMod import StateRHS
from .functions import s, mol_air, m, d, C, g, pa, ppm, mu_mol_O2, mu_mol_CO2, mu_mol_phot # importar simbolos 
from .functions import f_R, Sr, C_ev3, f_C, C_ev4, V_sa, VPD, f_V, r_s, gTC, Ca # importar funciones

states = ['Ci', 'A', 'C1', 'RH', 'T', 'PAR']
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
    def __init__( self, parameters):
        super().__init__()
        self.SetSymbTimeUnits(d) # días
        ### Add variables ###
        ## State variables
        for name in all_parameters:
            parameters[name].addvar_rhs(self)
    
    
    def RHS( self, Dt):
        """RHS( Dt ) = \kappa_1^{-1} F_1( t+Dt, X+k) where X is the current value of
           all state variables.  k is a simple dictionary { 'v1':k1, 'v2':k2 ... etc}
           
           ************* JUST CALL STATE VARIABLES WITH self.Vk ******************
           
           Use from ModMod TranslateArgNames() for guide you how call the functions 
        """
        ## Cálculos de la resitencia estomática
        f_R1 = f_R( I=self.V('PAR'), C_ev1=self.V('C_ev1'), C_ev2=self.V('C_ev2') )
        Sr1 = Sr( I=self.V('PAR'), S=self.V('S'), Rs=self.V('Rs') )
        C_ev31 = C_ev3( C_ev3n=self.V('C_ev3n'), C_ev3d=self.V('C_ev3d'), Sr=Sr1 )
        f_C1 = f_C( C_ev3=C_ev31, C1=self.V('C1'), k_fc=self.V('k_fc') ) 
        C_ev41 = C_ev4( C_ev4n=self.V('C_ev4n'), C_ev4d=self.V('C_ev4d'), Sr=Sr1 )
        V_sa1 = V_sa( T =self.V('T') )
        VPD1 = VPD( V_sa=V_sa1, RH=self.V('RH') )
        f_V1 = f_V( C_ev4=C_ev41, VPD = VPD1)
        R_s1 = r_s( r_m=self.V('r_m'), f_R=f_R1, f_C=f_C1, f_V=f_V1, k_d=self.V('k_d') ) 
        ## Cálculos absorción de CO2
        g_s = gTC( k=self.V('ks'), Rb=self.V('Rb'), Rs=R_s1, k_d=self.V('k_d') )
        Ca1 = Ca( gtc=g_s, C=self.V('C1'), Ci=self.Vk('Ci') )
        Dt_Ci = ( Ca1 - (1e-3)*self.V('A') )/0.554 # Los asimilados se pasan a mg/m**2 y el incremento del Ci queda en ppm
        return Dt_Ci
