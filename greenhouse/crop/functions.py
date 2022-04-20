#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 12:55:08 2022

@author: jdmolinam
"""

from numpy import exp, floor, clip, arange, append, sqrt
from sympy import symbols

###########################
####### Símbolos  #########
###########################
## Photosynthesis model
s, mol_CO2, mol_air, mol_phot, m, d, C, g, mol_O2, pa, ppm = symbols('s mol_CO2 mol_air mol_phot m d C g mol_O2 pa ppm')
mu_mol_CO2 = 1e-6 * mol_CO2
mu_mol_phot = 1e-6 * mol_phot
mu_mol_O2 = 1e-6 * mol_O2
mg = 1e-3*g
## Growth model
n_f, n_p, MJ, W, mg  = symbols('n_f n_p MJ W, mg') # number of fruits, number of plants


###########################
###### Funciones ##########
###########################

##### Fotosíntesis #######
## Funciones auxiliares ##
def V_cmax (T_f, V_cmax25, Q10_Vcmax, k_T):
    pow1 = (T_f - 25*k_T)/(10*k_T) 
    pow2 =  0.128 * (T_f - 40*k_T) / (1*k_T) 
    return (V_cmax25) * Q10_Vcmax**( pow1 ) / ( 1 + exp(pow2) )  

'''def Gamma_st (T_f): # Esta función la estoy calculando como lo hace Aarón
    return 150 * exp( 26.355 - ( 65.33 / ( 0.008314 * (T_f + 273.15) ) ) ) # La temperatura se está pasando de °C a Kelvins
'''

'''Este calculo de gamma_st esta basado en Xin & struick 2009'''
def Gamma_st (T_f): # No estoy seguro de los valores que da esta funcion
    R = 8.314
    ESoc = -24460
    return 0.5/(2800*exp((T_f-25)*(ESoc)/(298*R*(T_f+273))))
    

def tau (T_f, tau_25, Q10_tau, k_T):
    return tau_25 * Q10_tau**( (T_f - 25*k_T)/(10*k_T) )

def K_C (T_f, K_C25, Q10_KC, k_T):
    return K_C25 * Q10_KC**( (T_f - 25*k_T)/(10*k_T) )
    
def K_O (T_f, K_O25, Q10_KO, k_T):
    return K_O25 * Q10_KO**( (T_f - 25*k_T)/(10*k_T) )

def I_2 (I, f, ab):
    return  I * ab*(1 - f)  / 2

def J (I_2, J_max, theta):
    return ( (I_2) + (J_max) - ( ( (I_2 + J_max) )**2 -4*theta*I_2*J_max )**(0.5) ) / (2*theta)

## Factores limitantes en la producción de asimilados ##    
def A_R (O_a, tau, C_ippm, V_cmax, Gamma_st, K_C, K_O): 
    """
    Asimilación por Rubisco
    """
    return max([( 1 - ( O_a / (2.0*tau*C_ippm) ) ),0]) * V_cmax * max([C_ippm - Gamma_st,0]) / ( K_C *(1 + (O_a/K_O) ) + C_ippm )

def A_f (C_ippm, Gamma_st, J): 
    """
    Asimilación por radiación PAR
    En esta ecuación C_ippm este en ppm
    """
     # El CO2 está pasando de ppm a (mu_mol_CO2/mol_air)
    return  (max([C_ippm - Gamma_st,0])) * J / ( 4*C_ippm + 8*Gamma_st) 

def A_acum(V_cmax):
    """
    Asimilación por acumulación de carbohídratos
    """
    return V_cmax/2

def R_d (V_cmax):
    """
    Asimilados empleados en el mantenimiento de la planta
    """
    return 0.015*V_cmax

# factores limitantes de la tasa de asimilación
def A (A_R, A_f, A_acum):

    return  min([A_R, A_f, A_acum]) 
  

def Acrop(A,I1, CropDensity = 2):
    # A es la tasa de asimilación de CO2 en mumol (de CO2) m**-2(hoja) s**-1
    # esta tasa se calcula para cada planta. 
    #
    # Esta se debe usar por planta. Por lo tanto 
    #
    # Crop density es el numero de plantas por metro cuadrado
    # I1 es el LAI m**2 hoja m**2 invernadero
    # esta funcion nos da la A en mg CH20 planta**-1 s**-1
    return (30/10**6)*(I1/CropDensity)*A

#### Resistencia Estomática ####
    
def r_s (r_m, f_R, f_C, f_V):
    """
    En esta función se cálcula la resistencia estomática
    la cual depende r_m, el mínimo valor de resistenccia estomática,
    de f_R, f_c y f_V que son los factores de resistencia debidas a
    la radiación, el CO2 y la presión de vapor respectivamente. 
    """
    return (r_m) * f_R * f_C * f_V  # f_R, f_C y f_V son adimensionales

def f_R (I, C_ev1, C_ev2):
    """
    Factor de resistencia debida a la radiación global I
    """
    return (I + C_ev1) / (I + C_ev2)

def f_C (C_ev3, C1):
    """
    Factor de resistencia debida al CO2 

    En esta formula es necesario que C1 este en ppms 
    el factor de conversion es 1 ppm de CO2 = 0.553 mg m**-3
    """
    C1_ppm = C1 *(0.553)
    return 1 + C_ev3*( (C1_ppm - 200)**2 )

def C_ev3 (C_ev3n, C_ev3d, Sr):
    return C_ev3n*(1 - Sr) + C_ev3d*Sr

def Sr (I, S, Rs):
    return 1 / ( 1 + exp( S*(I - Rs) ) )

def f_V (C_ev4, VPD):
    return 1 + C_ev4*( VPD**2 )

def C_ev4 (C_ev4n, C_ev4d, Sr):
    return C_ev4n*(1 -Sr) + C_ev4d*Sr

def VPD(V_sa, RH): # Vapour pressure deficit
    return V_sa*(1 - RH/100)

def V_sa (T):
    """
    Esta función cálcula la presión de vapor de saturación,
    basandose en la ecuación de Arden Buck. T es la temperatura del aire en °C.
    Ver: https://en.wikipedia.org/wiki/Arden_Buck_equation
    """
    return 0.61121 * exp( ( 18.678 - (T/234.5) ) * ( T /(257.14 + T) ) )


#### Cálculo del CO2 intracelular ####
### Flujo de absorción del CO2 ###
def gTC (k, Rb, Rs):
    """
    Esta función calcula la conductancia total de CO2
    para una determinada capa del dosel
    """
    gs = (1 / Rs) # Conductancia estomática
    gb = (1 / Rb) # Conductancia estomática de la capa límite del dosel
    gtc = ( (1+k)*(1.6/gs) + (1.37/gb) )**-1 + k*( ( (1+k)*(1.6/gs) + k*(1.37/gb) )**-1 )
    return gtc

def Ca (gtc, C1, Ci):
    """
    Esta función calcula el CO2 absorbido ppm s**-1 
    El C1 (CO2 del invernadero) esta en mg m**-3 y se debe usar 
    en ppm para esto la convertimos 1 ppm de CO2 = 0.553 mg m**-3

    """
    C1_ppm = C1*0.553 # El CO2 pasa de (mu_mol_CO2/mol_air) a ppm
    return gtc * ( C1_ppm - Ci ) #El CO2 absorbido se calcula en ppm


#### Modelo de crecimiento ####
# Floration rate

def TF( PA_mean, T_mean, time, Dt):
    # The input PA_Mean is in Watts/m^2 but 
    # the formula needs the PAR radiation in MJ/day 
    kc = 11.57 # Transform Watts to MJ/day 1 MJ/d = 11.57 Watts
    # therefore we use PA_mean/fc

    # We need at least D days before flowering for first time  
    D = 2 # days 
    if time <= D*24*60*60:
        return 0
    else:     
        return (-0.75+ 0.09*T_mean)*(1-exp(-(1+PA_mean/kc)/2)) * Dt

def Y_pot(k2_TF, C_t, B, D, M, X, T_mean):
    """Growth potential of each fruit."""
    return (T_mean - 10*k2_TF) *\
        B * M * exp(B * ( X - C_t))/(1 + D * exp(B * (X - C_t)))**( 1 + 1/D)

def Y_pot_veg(k2_TF, a, b, T_mean):
    """Growth potencial of the vegetative part"""
    return a*k2_TF + b*T_mean
        
def t_wg( dw_ef, A, f_wg):
    """Growth rate."""
    return f_wg * A / dw_ef

def f_wg( Y_pot, Y_sum):
    """Sink stregth, without kmj."""
    return Y_pot / Y_sum  ### No units

