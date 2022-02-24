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
n_f, n_p, MJ = symbols('n_f n_p MJ') # number of fruits, number of plants


###########################
###### Funciones ##########
###########################

##### Fotosíntesis #######
## Funciones auxiliares ##
def V_cmax (T_f, V_cmax25, Q10_Vcmax, k_T, k_d):
    pow1 = (T_f - 25*k_T)/(10*k_T) 
    pow2 =  0.128 * (T_f - 40*k_T) / (1*k_T) 
    return (V_cmax25*k_d) * Q10_Vcmax**( pow1 ) / ( 1 + exp(pow2) )  

def Gamma_st (T_f): # Esta función la estoy calculando como lo hace Aarón
    return 150 * exp( 26.355 - ( 65.33 / ( 0.008314 * (T_f + 273.15) ) ) ) # La temperatura se está pasando de °C a Kelvins

def tau (T_f, tau_25, Q10_tau, k_T):
    return tau_25 * Q10_tau**( (T_f - 25*k_T)/(10*k_T) )

def K_C (T_f, K_C25, Q10_KC, k_T):
    return K_C25 * Q10_KC**( (T_f - 25*k_T)/(10*k_T) )
    
def K_O (T_f, K_O25, Q10_KO, k_T):
    return K_O25 * Q10_KO**( (T_f - 25*k_T)/(10*k_T) )

def I_2 (I, f, ab):
    return  I * ab*(1 - f)  / 2

def J (I_2, J_max, theta, k_d):
    return ( (I_2*k_d) + (J_max*k_d) + ( ( (I_2 + J_max)*k_d )**2 -4*theta*I_2*k_d*J_max*k_d )**(0.5) ) / (2*theta)

## Factores limitantes en la producción de asimilados ##    
def A_R (O_a, tau, C_i, V_cmax, Gamma_st, K_C, K_O, phi): 
    """
    Asimilación por Rubisco
    """
    C_i1 = C_i*(28.96/44) # El CO2 está pasando de ppm a (mu_mol_CO2/mol_air)
    return ( 1 - ( O_a / (phi*tau*C_i1) ) ) * V_cmax * (C_i1 - Gamma_st) / ( K_C *(1 + (O_a/K_O) ) + C_i1 )

def A_f (C_i, Gamma_st, J, k_JV): 
    """
    Asimilación por radiación PAR
    """
    C_i1 = C_i*(28.96/44) # El CO2 está pasando de ppm a (mu_mol_CO2/mol_air)
    return ( (C_i1 - Gamma_st)*J / ( 4*C_i1 + 8*Gamma_st) )*k_JV

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

# Tasa de asimilación
def A (A_R, A_f, A_acum, R_d, fc):
    return fc * ( min( A_R, A_f, A_acum ) - R_d )

#### Resistencia Estomática ####
    
def r_s (r_m, f_R, f_C, f_V, k_d):
    """
    En esta función se cálcula la resistencia estomática
    la cual depende r_m, el mínimo valor de resistenccia estomática,
    de f_R, f_c y f_V que son los factores de resistencia debidas a
    la radiación, el CO2 y la presión de vapor respectivamente. 
    """
    return (r_m/k_d) * f_R * f_C * f_V  # f_R, f_C y f_V son adimensionales

def f_R (I, C_ev1, C_ev2):
    """
    Factor de resistencia debida a la radiación global I
    """
    return (I + C_ev1) / (I + C_ev2)

def f_C (C_ev3, C1, k_fc):
    """
    Factor de resistencia debida al CO2 
    """
    return 1 + C_ev3*( (C1 - 200*k_fc)**2 )

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
def gTC (k, Rb, Rs, k_d):
    """
    Esta función calcula la conductancia total de CO2
    para una determinada capa del dosel
    """
    gs = (1 / Rs) # Conductancia estomática
    gb = (1 / Rb)*k_d # Conductancia estomática de la capa límite del dosel
    gtc = ( (1+k)*(1.6/gs) + (1.37/gb) )**-1 + k*( ( (1+k)*(1.6/gs) + k*(1.37/gb) )**-1 )
    return gtc

def Ca (gtc, C, Ci):
    """
    Esta función calcula el CO2 absorbido (mg / m**2 * d) 
    por una determinada capa del dosel
    """
    C1 = C*(44/28.96) # El CO2 pasa de (mu_mol_CO2/mol_air) a ppm
    return gtc*( (C1 - Ci)*0.554 ) # El CO2 se está pasando de ppm a mg/m**2


#### Modelo de crecimiento ####
"""
*******  Note, the original TF is quite unsensitive to PA_mean ******
def TF( k1_TF, k2_TF, k3_TF, PA_mean, T_mean, Dt):
    ### ORIGINAL Floration rate. DOES NOT DEPEND MUCH ON PA_MEAN!!
    return (-0.75*k2_TF + 0.09*T_mean)*(1-exp(-(1*k1_TF+PA_mean)/(2*k1_TF)))*k3_TF * Dt
"""

def TF_tmp( k1_TF, k2_TF, k3_TF, PA_mean, T_mean, Dt):
    """Floration rate. TEMPORARY ... k1_TF = 150 the original below look wrong"""
    return (-0.75*k2_TF + 0.09*T_mean)*(1-exp(-PA_mean/k1_TF))*k3_TF * Dt

def TF( k1_TF, k2_TF, k3_TF, PA_mean, T_mean, Dt):
    ### ORIGINAL Floration rate. DOES NOT DEPEND MUCH ON PA_MEAN!!
    return (-0.75*k2_TF + 0.09*T_mean)*(1-exp(-(1*k1_TF+PA_mean)/(2*k1_TF)))*k3_TF * Dt


def f( k1_TF, k2_TF, PA_mean, T_mean, Dt):
    return -(1*k1_TF+PA_mean)/(2*k1_TF)

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

