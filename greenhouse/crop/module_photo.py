#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:46:50 2022

@author: jdmolinam
"""

from ModMod import Module
from numpy import arange, append
from .functions import V_cmax, R_d, tau, K_C, K_O, Gamma_st, I_2, J, A_R, A_f, A_acum, A # importar funciones fotosíntesis
from .functions import f_R, V_sa, fRH, Sr, C_ev3, f_C, C_ev4, VPD, f_V, r_s, gsf # importar funciones fotosíntesis
from .ci_rhs import Ci_rhs

#####################################
##### Módulo de fotosíntesis ########
#####################################
class PhotoModule(Module):
    def __init__( self, Ci_rhs_ins, modelo, Dt=60): 
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
        self.Modelo = modelo

    def Advance( self, t1):
        ## Actualización de la tasa de asimilación
        tt = append( arange(self.t(), t1, step=self.Dt), [t1])
        n = len(tt)  ### Number of time steps
        for i in range( 1, n): 
            #ind_pho = self.V('ind_pho')
            T1 = self.V_GetRec('T1', ind_get=-n+i)
            I2 = self.V_GetRec('I2T', ind_get=-n+i) # Este es el I2 = sol + lamparas
            C1 = self.V_GetRec('C1', ind_get=-n+i)
            V1 = self.V_GetRec('V1', ind_get=-n+i)
            #self.V_Set('Ci',(C1*0.554)*0.67) #67%  ppm and mg/m**-3 = 0.556 ppm
            
            # Calculo de la presión de vapor de saturación
            Vsat = V_sa( T1)
            # Calculo de la Humedad Relativa 
            RH = fRH( V1, Vsat)
            
            # Calculo de las constantes para las formulas de fotosintesis 
            V_cmax1 = V_cmax( T_f=T1, V_cmax25=self.V('V_cmax25'), Q10_Vcmax=self.V('Q10_Vcmax'), k_T=self.V('k_T') )
            R_d1 = R_d( V_cmax=V_cmax1 )
            #tau1 = tau( T_f=T1, tau_25=self.V('tau_25'), Q10_tau=self.V('Q10_tau'), k_T=self.V('k_T') )
            K_C1 = K_C( T_f=T1, K_C25=self.V('K_C25'), Q10_KC=self.V('Q10_KC'), k_T=self.V('k_T') )
            K_O1 = K_O( T_f=T1, K_O25=self.V('K_O25'), Q10_KO=self.V('Q10_KO'), k_T=self.V('k_T') )
            Gamma_st1 = Gamma_st( T_f=T1 )
            I_21 = I_2( I = I2, f = self.V('f'), ab = self.V('ab') )
            J1 = J( I_2 = I_21, J_max=self.V('J_max'), theta = self.V('theta') )


            # Modelos de fotosintesis:
            #
            # (A) Surrogate: Consiste de una función concava en PAR y Ca 
            #            (CO2 atmosférico) que simula  el comportamiento 
            #            de la fotosintesis. 
            #             
            # (B) Simplificado: Considera el modelo completo de Farquhar, von Caemmerer 
            #               & Berry 1980 (FvCB-1980), pero se asumen que: 
            #
            #               1) La conductancia del CO2 en los estomas es tal que 
            #                  la concentración del CO2 intracelular (Ci) es el 68% 
            #                  de la concentración del CO2 atmosférico  (Ca). Es decir:
            #                       Cippm = 0.67*(0.554*Ca) (C1*)*0.67 
            #                  En el modelo Ca esta mg * m**-3  ylo debemos trasnformar a ppm.
            #                  En Factor de conversion es 1 mg * m**-3 = 0.556 ppm
            #                  El 67% se toma de Vanthoor que a su vez lo toma de 
            #                  Evans and Farquhar (1991). Ellos asumen que esto da el CO2
            #                  a pasando los estimas (esto es Ci).
            #               2) La conductancia de Ci a través de la membrana mesofilica es 
            #                  constante y esta dada por g_t = g_m = 0.14  mu_mul m**-2 s**-1 ppm**-1 
            #                  (= mol m**−2 s**−1 bar**−1)
            #
            #                  Con estas suposiciones el para el CO2 en los sitios de carboxilacion (Cc) 
            #                  es:
            #                               A = g_t(Cc - Cippm )
            #                  De esta ecuación combinada con FvCB-1980 se obtienen las ecuaciones 
            #                  cuadráticas para A_R y A_F (los asimilados limitados por Rubisto y Radiación) 

            # (C) Estomatas variables: Considera el modelo completo de Farquhar, von Caemmerer 
            #               & Berry 1980 (FvCB-1980), pero se asumen que: 
            #
            #               1) La conductancia del CO2 en los estomas  (g_s) varia segun la 
            #               concentración de CO2, radiación global y deficit de presión de valor según 
            #               el modelo de Stanghellini 1980.  En realidad este modelo es para la resistrencia
            #               del H2O en los estomas. La resistencia (rs_s) se mide en unidades de s * m**-1, 
            #               y la conductancia sería:  g_s = rs**-1 (1.66)**-1. Para transformar este valor a las 
            #               uniddades de mu_mol_CH20 * ppm_CO2**-1 * m**-2 s**-1 necesitmos multiplicar a 
            #               gs * (0.553/0.044) ver función  gsf.     
            #               
            #               2) En este modelo no se toman en cuenta la conductancia de Ci a través 
            #                  de la membrana mesofilica. 

            # Trasform C1 from mg * m*-3 to ppm  
            # (Conversion factor 0.556 ppm / (mg * m*-3)  
            C1ppm = (C1*0.554)
            
            if self.Modelo['Simplificado']:
                # 68 % para modelar la conductancia por estomas (Vanthoor)
                C1ppm =  0.67 * C1ppm 
                # Conductancia del mesofilo se usa consisntente con Patric2009
                # Notemos que la g_s esta en unidades de mu_mol_CH20 * ppm_CO2**-1 * m**-2 s**-1
                g_m = self.V('g_m25')
                g_t = g_m
 
            if self.Modelo['EstomataVar']:
                # Factor de resistencia debida a la radiación global
                f_R1 = f_R( I=I_21, C_ev1=self.V('C_ev1'), C_ev2=self.V('C_ev2'), LAI = self.V('I1') )
                Sr1 = Sr( I=I2, S=self.V('S'), Rs=self.V('Rs') )
            
                # Factor de resistencia debida a la concentración de CO2
                C_ev31 = C_ev3( C_ev3n=self.V('C_ev3n'), C_ev3d=self.V('C_ev3d'), Sr=Sr1 )
                f_C1 = f_C( C_ev3=C_ev31, C1=C1 ) 

                # Factor de resistencia debida a presion de vapor
                C_ev41 = C_ev4( C_ev4n=self.V('C_ev4n'), C_ev4d=self.V('C_ev4d'), Sr=Sr1 )
                VPD1 = VPD( V_sa=Vsat, RH = RH )
                f_V1 = f_V( C_ev4=C_ev41, VPD = VPD1)

                # Resistencia estomática para el agua en unidades de s * m**-1
                R_agua = r_s( r_m=self.V('r_m'), f_R=f_R1, f_C=f_C1, f_V=f_V1) 
            
                # La conductividad estomática del CO2 es proporcional a la del agua. 
                # Notemos que la g_s esta en unidades de mu_mol_CH20 * ppm_CO2**-1 * m**-2 s**-1
                g_s = gsf( Ragua = R_agua)
                
                # Con esto la conductancia total es:
                g_t = g_s 
             
            # Calculo de los asimilados a partir de la relación cuadrática

            # Rubisco limited cuadratic function
            Ra1 = 1
            Rb1 = -(V_cmax1 + g_t*(C1ppm + K_C1*(1 + self.V('O_a')/K_O1)) - R_d1)
            Rc1 =  g_t*( V_cmax1 *  max([C1ppm - Gamma_st1 ,0])  - R_d1 * (C1ppm + K_C1*(1+self.V('O_a')/K_O1)))
            A_R1 =  ( - Rb1 - (Rb1**2 - 4.0 * Ra1 * Rc1)**(0.5) ) / (2.0 * Ra1) 

            # Radiation limited cuadratic fucntion
            if J1 < 0 :
                A_f1 = - R_d1
            else:
                fa1= 1
                fb1= - ( J1 / 4.0 + g_t *( C1ppm + 2*Gamma_st1)  - R_d1)
                fc1= g_t * (  max([ C1ppm - Gamma_st1, 0]) * J1 / 4.0 - R_d1 * (C1ppm + 2*Gamma_st1))
                A_f1 = (- fb1 - (fb1**2 - 4.0 * fa1 * fc1 )**(0.5))/(2.0 * fa1)
   
            # Assimilates store limitation
            A_acum1 = A_acum( V_cmax = V_cmax1 ) - R_d1

            # Combining all three limiting factors ti obtain the asimilates
            A1 = max([A( A_R = A_R1 , A_f = A_f1 , A_acum = A_acum1),- R_d1]) 


            # Save variables computed during the step
            self.V_Set('Ci',C1ppm - A1/g_t) # Ci en ppm ( mg/m**-3 = 0.556 ppm)
            self.V_Set('RH', RH)            # Humedad relativa en porcentaje
            self.V_Set('A', A1)             # Asimilados en 
            
            ## Avance del RHS (En esta version no se usa, pero si las definiciones del RHS)
            #self.AdvanceRungeKutta(t1=tt[i], t0=tt[i-1]) 

        return 1
