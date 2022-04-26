#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:21:39 2022

@author: jdmolinam
"""

from ModMod import Module
from numpy import exp, floor, clip, arange, append, sqrt
from .functions import TF, Y_pot, t_wg, Acrop # importar funciones crecimiento de la planta
from scipy.stats import norm, gamma
import copy

#################################################################
############ Módulo de crecimiento para una planta ##############
#################################################################
class Plant(Module):
    def __init__( self, beta, Q_rhs_ins, Dt_f=60, Dt_g=60):#60*60*24):  # Dt_f=0.1, Dt_g=0.25
        """Models one plant growth, with a variable number of fruits."""
        ## Dt_f is the photosynthesis Dt, this is use for RK advance
        ## Dt_g is the growth Dt, this is use for the update and anvance of the fruits
        super().__init__(Dt_g) #Time steping of module, days
        ### Always, use the super class __init__, there are several other initializations
        
        self.Dt_g = Dt_g
        self.beta = beta ## must be in (0,1]
    
        ### Time units= hours
        
        ### Vegetative part
        self.veget = [0.0 , 0.0] ## characteristics for vegetative part: Weight and growth potential 

        self.fruits = [] # No fruits
        self.n_fruits = 0 ## Current number of fruits
        self.n_fruits_h = 0 ## total number of fruits harvested
        self.new_fruit = 0  ## Cummulative number of fruits
        self.m = 4 ## Number of characteristics for each fruit: thermic age, weight, growth potential and Michaelis-Menten constant
        ### Module specific constructors, add RHS's
        #quitado por mi self.i = 0 <------------------------------------------------
        self.AddStateRHS( 'Q', Q_rhs_ins)

    def Advance( self, t1):
        """Update the plant/fruit growth. Update global variables, to time t1."""
        
        ### This creates a set of times knots, that terminates in t1 with
        ### a Deltat <= self.Dt
        # 
        if t1 % 86400 == 0:
            #tt = append( arange( self.t(), t1, step=self.Dt_g), [t1])  ### <---- no se deberia de usar
            ## tt = append( arange( self.t(), t1, step=self.Dt_g), [t1])
            #sd = 60 * 60 * 24 # Seconds per day
            #md = 60 * 24 # minutes per day --> Se usa con los modelos de clima y fotosíntesis que trabajan en minutos
            Dt_c = self.D.Modules['Photosynt'].Dt
            md = int(86400/Dt_c)
            # Las ecuaciones del modelo de crecimiento de plnatas estan unidades de dias. 
            # Para ser consistentes definimos una unidad de tiempo en dias Dtdias 
            Dtdias = 1 # Unidad de tiendo en dias.
            # este indice se avanza en el <-----------------------------
            #self.V_Set('ind_pho', - int( self.V('Dt_dir') / self.V('Dt_pho') )  ) # Se reinicia el valor del indice auxiliar  
            ## Promedios diarios de temperatura y PAR
            T_mean = self.V_Mean('T2', ni=-md ) # Se saca el promedio sobre los registros del último día
            PAR_mean = self.V_Mean('I2', ni=-md ) # Se saca el promedio sobre los registros del último día
            ## Asimilados acumulados (integrados) en el último día
            acrop = lambda x: Acrop(x, I1=2) #### Cambiar valor de I1
            try:
                A_int = self.V_Int('A', ni=-md,t=arange(0, 86400, Dt_c), g=acrop) # Se integra sobre los registros del último día 
                #if t1 > 86400*22:

                   #breakpoint()
            except:
                breakpoint()
            #print(tt)
            #steps = len(1)
            #for i in range( 1, steps):      ####<---------------- corregir este for no va 
           
            ### With the Floration Rate, create new fruits
            # 
            # Politica de Poda: de cada Npoda flores, mantengo unicamente una
            Npoda = 2
            PA_mean_i = self.beta * PAR_mean
            self.new_fruit += TF(PA_mean=PA_mean_i, T_mean=T_mean, time = self.t(), Dt = Dtdias)/Npoda
            new_fruit_n = self.new_fruit 
            if new_fruit_n >= 1:
                #nw = new_fruit_n
                nw = int(floor(self.new_fruit))
                for nf in range(nw):
                    ### Add new fruit
                    self.fruits += [[ 0.0, 0.0, 0.0, 0.0]] 
                    ### also the growth potential, as an auxiliar for calculations
                    self.n_fruits += 1 
                ### Leave the rational part of new_fruit
                self.new_fruit = max( 0, self.new_fruit - nw)

            ### Update thermic age (we use average temperature) of all fruits
            for fruit in self.fruits:
                fruit[0] += ( max( [0 , T_mean - 10 ]) ) * Dtdias ## Thermic age never decreases
            ### Update growth potencial for vegetative part
            self.veget[1] = self.V('a') + self.V('b')*T_mean 
            ### Update Growth potential and Michaelis-Menten constants of all fruits
            # Start with the growth potencial of vegetative part
            tmp = 0.0                            # sum of growth potentials
            tmp1 = self.veget[1] / A_int   # denominator of f_wg estimates

            for fruit in self.fruits:
                x = fruit[0] ## Thermic age
                ### Michaelis-Menten constants 
                if x <= self.V('C_t') :
                    fruit[3] = 0.05*tmp*(self.V('C_t') - x) / self.V('C_t')    
                ### Growth potential
                fruit[2] = clip( Y_pot( k2_TF=self.V('k2_TF'), C_t=self.V('C_t'),\
                     B=self.V('B'), D=self.V('D'), M=self.V('M'), X=x, T_mean=self.V('T2')),\
                     a_min=0, a_max=exp(300))
                tmp += fruit[2]
                tmp1 += fruit[2] / ( fruit[3] + A_int )
            #self.V_Set( 'Y_sum', tmp)
            ### Update weight of vegetative part
            f_wg_veg =  self.veget[1] / ( A_int * tmp1  ) # The sink strentgh of vegetative part
            self.veget[0] += t_wg( dw_ef=self.V('dw_ef_veg'), A=A_int, f_wg=f_wg_veg) * Dtdias
            #### Update weight of all fruits
            tmp2 = 0.0 # Total weight of the fruits
            for fruit in self.fruits:
                f_wg =  fruit[2] / ( ( fruit[3] + A_int ) * tmp1 ) # The sink strentgh of the fruit
                dwh = t_wg( dw_ef=self.V('dw_ef'), A=A_int, f_wg=f_wg) * Dtdias # dry weight
                pdw = 0.023 # percentage of dry weight
                fruit[1] += dwh / pdw # Fresh weight  
                tmp2 += fruit[1] #Total weight
                
            
            ### Check if a fruit is ready to be harvest
            fruits = copy.deepcopy(self.fruits) # copy of all fruits
            wk = 0 
            nfk = 0
            
            for fruit in  self.fruits: # h is the indice and fruit is the object
                if (fruit[0] > 275 or fruit[1] > 360): # It is harvested when a fruit reaches a thermic age of 275 °C d or if the fruit's weigth is greater than 360 g
                    self.n_fruits -= 1 # number fruits in crop
                    wk += fruit[1] # weight of harvested fruits in this moment
                    nfk += 1       # number fruits harvested in this moment
                    fruits.remove(fruit) # Harvested fruits are removed from the list
            self.fruits = fruits
               


            # Set value for number and weitgh harvested fruits
            self.V_Set( 'n_k', nfk)
            self.V_Set( 'h_k', wk)
            w = self.V( 'Q_h') + self.V('h_k') # accumulated weight fruits harvested
            self.V_Set( 'Q_h', w)
            self.n_fruits_h += self.V('n_k') # accumulated number fruits harvested

            #### Update assimilation rate after distribution
            # m = ( f_wg_veg / self.V('dw_ef_veg') ) + ( (1 - f_wg_veg ) / self.V('dw_ef') )
            # As = self.V('A')*( 1 - self.V('a_ef')*Dt*m ) # A = A - ( Total weigth of fruits and vegetative part )
            self.V_Set('A', 0 )  
            # Revisar si 'As==0'? <--------------------------------
            #### Total weight of the fruits
            self.V_Set( 'Q', tmp2)
            #### Advance of the RHS
            self.AdvanceAssigment(t1) # Set Q
        return 1