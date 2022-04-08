#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:46:50 2022

@author: jdmolinam
"""

from ModMod import Module
from numpy import arange, append
from .functions import V_cmax, R_d, tau, K_C, K_O, Gamma_st, I_2, J, A_R, A_f, A_acum, A # importar funciones fotosíntesis
from .ci_rhs import Ci_rhs

#####################################
##### Módulo de fotosíntesis ########
#####################################
class PhotoModule(Module):
    def __init__( self, Ci_rhs_ins, Dt=60): 
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
        tt = append( arange(self.t(), t1, step=self.Dt), [t1])
        n = len(tt)  ### Number of time steps
        for i in range( 1, n): 
            ind_pho = self.V('ind_pho')
            T1 = self.V_GetRec('T1', ind_get=-n+i)
            I2 = self.V_GetRec('I2', ind_get=-n+i)
            V_cmax1 = V_cmax( T_f=T1, V_cmax25=self.V('V_cmax25'), Q10_Vcmax=self.V('Q10_Vcmax'), k_T=self.V('k_T') )
            R_d1 = R_d( V_cmax=V_cmax1 )
            tau1 = tau( T_f=T1, tau_25=self.V('tau_25'), Q10_tau=self.V('Q10_tau'), k_T=self.V('k_T') )
            K_C1 = K_C( T_f=T1, K_C25=self.V('K_C25'), Q10_KC=self.V('Q10_KC'), k_T=self.V('k_T') )
            K_O1 = K_O( T_f=T1, K_O25=self.V('K_O25'), Q10_KO=self.V('Q10_KO'), k_T=self.V('k_T') )
            Gamma_st1 = Gamma_st( T_f=T1 )
            I_21 = I_2( I = I2, f=self.V('f'), ab=self.V('ab') )
            J1 = J( I_2=I_21, J_max=self.V('J_max'), theta=self.V('theta') )
            A_R1 = A_R( O_a=self.V('O_a'), tau=tau1, C_i=self.V('Ci'), V_cmax=V_cmax1, Gamma_st=Gamma_st1, K_C=K_C1, K_O=K_O1)
            A_f1 = A_f( C_i=self.V('Ci'), Gamma_st=Gamma_st1, J=J1, k_JV=self.V('k_JV') )
            A_acum1 = A_acum( V_cmax=V_cmax1 )
            A1 = A( A_R=A_R1, A_f=A_f1, A_acum=A_acum1, R_d=R_d1, fc=self.V('fc') ) 
            self.V_Set('A', A1)
            #if A1 > 1000:
                #breakpoint()
            #
            self.V_Set('ind_pho', ind_pho + 1) # Después de que se calcularon los asimilados, se actualiza el valor del indice auxiliar pues se avanza un minuto
            ## Avance del RHS
            self.AdvanceRungeKutta(t1=tt[i], t0=tt[i-1]) 

        return 1
