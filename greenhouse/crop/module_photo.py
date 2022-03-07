#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:46:50 2022

@author: jdmolinam
"""

from ModMod import Module
from .functions import V_cmax, R_d, tau, K_C, K_O, Gamma_st, I_2, J, A_R, A_f, A_acum, A # importar funciones fotosíntesis
from .ci_rhs import Ci_rhs

#####################################
##### Módulo de fotosíntesis ########
#####################################
class PhotoModule(Module):
    def __init__( self, Ci_rhs_ins, Dt=1): 
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt) #Time steping of module
        ### Always, use the super class __init__, theare are several otjer initializations
        
        ##############################
        ### Creación de instancias ###
        ##############################
        #Ci_rhs_ins = Ci_rhs(theta)
        
        ### Module specific constructors, add RHS's
        self.AddStateRHS( 'Ci', Ci_rhs_ins)

    def Advance( self, t1):
        ## Actualización de la tasa de asimilación
        V_cmax1 = V_cmax( T_f=self.V('T'), V_cmax25=self.V('V_cmax25'), Q10_Vcmax=self.V('Q10_Vcmax'), k_T=self.V('k_T'), k_d=self.V('k_d') )
        R_d1 = R_d( V_cmax=V_cmax1 )
        tau1 = tau( T_f=self.V('T'), tau_25=self.V('tau_25'), Q10_tau=self.V('Q10_tau'), k_T=self.V('k_T') )
        K_C1 = K_C( T_f=self.V('T'), K_C25=self.V('K_C25'), Q10_KC=self.V('Q10_KC'), k_T=self.V('k_T') )
        K_O1 = K_O( T_f=self.V('T'), K_O25=self.V('K_O25'), Q10_KO=self.V('Q10_KO'), k_T=self.V('k_T') )
        Gamma_st1 = Gamma_st( T_f=self.V('T') )
        I_21 = I_2( I =self.V('PAR'), f=self.V('f'), ab=self.V('ab') )
        J1 = J( I_2=I_21, J_max=self.V('J_max'), theta=self.V('theta'), k_d=self.V('k_d') )
        A_R1 = A_R( O_a=self.V('O_a'), tau=tau1, C_i=self.V('Ci'), V_cmax=V_cmax1, Gamma_st=Gamma_st1, K_C=K_C1, K_O=K_O1, phi=self.V('phi') )
        A_f1 = A_f( C_i=self.V('Ci'), Gamma_st=Gamma_st1, J=J1, k_JV=self.V('k_JV') )
        A_acum1 = A_acum( V_cmax=V_cmax1 )
        A1 = abs( A( A_R=A_R1, A_f=A_f1, A_acum=A_acum1, R_d=R_d1, fc=self.V('fc') ) )
        self.V_Set('A', A1)
        ## Avance del RHS
        self.AdvanceRungeKutta(t1) 
        return 1
