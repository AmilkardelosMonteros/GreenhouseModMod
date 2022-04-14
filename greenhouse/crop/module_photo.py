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
            #ind_pho = self.V('ind_pho')
            T1 = self.V_GetRec('T1', ind_get=-n+i)
            I2 = self.V_GetRec('I2', ind_get=-n+i)
            C1 = self.V_GetRec('C1', ind_get=-n+i)
            #self.V_Set('Ci',(C1*0.554)*0.67) #67%  ppm and mg/m**-3 = 0.556 ppm
            
            #if I2 > 400:
            #    breakpoint()
            V_cmax1 = V_cmax( T_f=T1, V_cmax25=self.V('V_cmax25'), Q10_Vcmax=self.V('Q10_Vcmax'), k_T=self.V('k_T') )
            R_d1 = R_d( V_cmax=V_cmax1 )
            tau1 = tau( T_f=T1, tau_25=self.V('tau_25'), Q10_tau=self.V('Q10_tau'), k_T=self.V('k_T') )
            K_C1 = K_C( T_f=T1, K_C25=self.V('K_C25'), Q10_KC=self.V('Q10_KC'), k_T=self.V('k_T') )
            K_O1 = K_O( T_f=T1, K_O25=self.V('K_O25'), Q10_KO=self.V('Q10_KO'), k_T=self.V('k_T') )
            Gamma_st1 = Gamma_st( T_f=T1 )
            I_21 = I_2( I = I2, f = self.V('f'), ab = self.V('ab') )
            J1 = J( I_2 = I_21, J_max=self.V('J_max'), theta = self.V('theta') )

            # Solo tomamos el 67 % de la concentración de CO2 en Ci
            C1ppm = (C1*0.554)*0.67 #C1 in ppm we use that mg/m**-3 = 0.556 ppm
            # Conductividad estomática. 
            # Hay que arreglar esto para que se calcule bien
            # Conductividad (mesophylic) es 
            g_s = 0.14370869660918402  # este número es consistente con Patrick et al   

            # en este calculo seguimos a Von Creamer pp 42 que se basa en la 
            # solución de una ecuación de segund grado. 
            # OJO: la ecuación en Von Creamer tiene errores de signo.
            # tomamos la raiz negativa en ambos casos. Esto da valores razonables
            # de los parámetros. 

            # En esta version la Rd1 ya esta incorposada, por lo que modificamos 
            # a la función A mas adelante. 
            Ra1 = 1
            Rb1 = -(V_cmax1 + g_s*(C1ppm + K_C1*(1 + self.V('O_a')/K_O1)) - R_d1)
            Rc1 =  g_s*( V_cmax1 *  max([C1ppm - Gamma_st1 ,0])  - R_d1 * (C1ppm + K_C1*(1+self.V('O_a')/K_O1)))
            A_R1 =  ( - Rb1 - (Rb1**2 - 4.0 * Ra1 * Rc1)**(0.5) ) / (2.0 * Ra1) 

            if J1 < 0 :
                A_f1 = - R_d1
            else:
                fa1= 1
                fb1= - ( J1 / 4.0 + g_s *( C1ppm + 2*Gamma_st1)  - R_d1)
                fc1= g_s * (  max([ C1ppm - Gamma_st1, 0]) * J1 / 4.0 - R_d1 * (C1ppm + 2*Gamma_st1))
                A_f1 = (- fb1 - (fb1**2 - 4.0 * fa1 * fc1 )**(0.5))/(2.0 * fa1)
  
            
            #A_f1 = A_f( C_ippm=self.V('Ci'), Gamma_st=Gamma_st1, J=J1 )
            #A_R1 = A_R( O_a=self.V('O_a'), tau=tau1, C_ippm=self.V('Ci'), V_cmax=V_cmax1, Gamma_st=Gamma_st1, K_C=K_C1, K_O=K_O1)
           
            A_acum1 = A_acum( V_cmax = V_cmax1 ) - R_d1

            #A1 = A( A_R=max([A_R1+R_d1,0]), A_f=max([A_f1+R_d1,0]), A_acum=A_acum1+R_d1, R_d=R_d1, fc=self.V('fc') ) 
            A1 = max([A( A_R = A_R1 , A_f = A_f1 , A_acum = A_acum1),- R_d1]) 

            self.V_Set('Ci',C1ppm - A1/g_s) # Ci en ppm ( mg/m**-3 = 0.556 ppm)

            #print(str(self.t())+'['+str(T1)+', '+str(I2)+', '+str(self.V('Ci'))+' ]' )
            #print(str(self.t())+'A1 = '+str(A1)+' ['+str(A_R1)+', '+str(A_f1)+', '+str(A_acum1)+', '+str(R_d1)+' ] ' )
            self.V_Set('A', A1)

            #if J1 > 1:
            #   print('Dia   '+' A = ' + str(A1))    
            #else:  
            #   print('Noche '+' A = ' + str(A1))     
            #print(A1)
            
            #self.V_Set('ind_pho', ind_pho + 1) # Después de que se calcularon los asimilados, se actualiza el valor del indice auxiliar pues se avanza un minuto
            ## Avance del RHS
            #self.AdvanceRungeKutta(t1=tt[i], t0=tt[i-1]) 

        return 1
