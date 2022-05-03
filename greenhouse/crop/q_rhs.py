#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:00:07 2022

@author: jdmolinam
"""

from asyncio import constants
from ModMod import StateRHS
from .functions import m, d, C, g, mu_mol_phot, n_f, MJ, W, s # importar simbolos 


global_constants = ['k1_TF', 'k2_TF']
local_constants = ['k3_TF', 'dw_ef', 'dw_ef_veg','a_ef', 'C_t', 'B', 'D', 'M', 'a', 'b']
states = ['T2', 'I2', 'C1', 'V1', 'I1'] ### NO VA
local_states = ['A', 'Q', 'm_k', 'n_k', 'h_k', 'Q_h', 'Y_sum']
local_parameters = local_states + local_constants
global_parameters = states + global_constants

# number of register to save 
nrec = 90*24*60

#################################################################
############ RHS modelo de crecimiento ##########################
#################################################################    
class Q_rhs(StateRHS):
    """
    Q is the weight of all fruits for plant
    """
    def __init__( self, theta_p=[0.7, 3.3, 0.25]):
        """Define a RHS, ***this an assigment RHS***, V1 = h2(...), NO ODE."""
        ### uses the super class __init__
        super().__init__()

        ### Define variables here.  Each fruit will have repeated variables.
        ### Later some will be shared and the Local variable swill be exclusive
        ### of each fruit.
        
        self.SetSymbTimeUnits(d) # days

        ### State variables coming from the climate model
        self.AddVar( typ='State', varid='T2', prn=r'$T_2$',\
                    desc="Greenhouse air temperature", units= C ,rec=nrec, val=20) 
        
        #self.AddVar( typ='State', varid='PAR', prn=r'$PAR$',\
        #   desc="PAR radiation", units=mu_mol_phot * (m**-2) * d**-1 , val=300.00)
        self.AddVar( typ='State', varid='I2', prn=r'$I_2$',\
                    desc="External global radiation", units= W * m**-2 , rec=nrec, val=100) # It's takes as the PAR 
        
        
        ### Local variables, separate for each plant
        self.AddVarLocal( typ='State', varid='A', prn=r'$A$',\
           desc="Assimilation rate", units= g * (m**-2), val=0, rec=1440)
        
        self.AddVarLocal( typ='StatePartial', varid='Q', prn=r'$Q$',\
           desc="Weight of all fruits for plant", units= g, val=0.0)
        
        self.AddVarLocal( typ='StatePartial', varid='m_k', prn=r'$m_k$',\
           desc="Simulation number of fruits harvested for plant", units= n_f, val=0.0)
        
        self.AddVarLocal( typ='StatePartial', varid='n_k', prn=r'$n_k$',\
           desc="Number of fruits harvested for plant", units= n_f, val=0)

        self.AddVarLocal( typ='StatePartial', varid='h_k', prn=r'$h_k$',\
           desc="Weight of all harvested fruits for plant", units= g, val=0.0)

        self.AddVarLocal( typ='StatePartial', varid='Q_h', prn=r'$H$',\
           desc="Accumulated weight of all harvested fruits for plant", units= g, val=0.0)

        self.AddVarLocal( typ='StatePartial', varid='Y_sum', prn=r'$Y_{sum}$',\
           desc="Sum of all potentail growths", units= g/d**2, val=0.0)


        ### Canstants, shared by all plants.  Shared Cnts cannot be local
        self.AddVar( typ='Cnts', varid='k1_TF', prn=r'$k1_TF$',\
           desc="Aux in function TF", units= MJ * m**-2 * d**-1, val=300.0)

        self.AddVar( typ='Cnts', varid='k2_TF', prn=r'$k2_TF$',\
           desc="Aux in function TF", units= C * d**-1, val=1.0)

        self.AddVarLocal( typ='Cnts', varid='k3_TF', prn=r'$k3_TF$',\
           desc="Aux in function TF", units= n_f * C**-1, val=1.0)

        self.AddVarLocal( typ='Cnts', varid='dw_ef', prn=r'$dw_{efficacy}$',\
           desc="Constant in t_wg for fruits", units= 1, val=1.3)
        
        self.AddVarLocal( typ='Cnts', varid='dw_ef_veg', prn=r'$dw_{efficacy}$',\
           desc="Constant in t_wg for vegetative part", units= 1, val=1.15)

        self.AddVarLocal( typ='Cnts', varid='a_ef', prn=r'$a_{efficacy}$',\
           desc="Matching constant in remaining assimilates", units= 1/m**2, val=1.0)

        self.AddVarLocal( typ='Cnts', varid='C_t', prn=r'$C_t$',\
           desc="Constant in Y_pot", units= C * d, val=131.0)

        self.AddVarLocal( typ='Cnts', varid='B', prn=r'$B$',\
           desc="Constant in Y_pot", units= (C * d)**-1, val=0.017)

        self.AddVarLocal( typ='Cnts', varid='D', prn=r'$D$',\
           desc="Constant in Y_pot", units= 1, val=0.011)

        self.AddVarLocal( typ='Cnts', varid='M', prn=r'$M$',\
           desc="Constant in Y_pot", units= g, val=60.7)
        
        self.AddVarLocal( typ='Cnts', varid='a', prn=r'$a$',\
           desc="Constant in Y_pot_veg", units= 1, val=theta_p[1])
        
        self.AddVarLocal( typ='Cnts', varid='b', prn=r'$b$',\
           desc="Constant in Y_pot_veg", units= 1, val=theta_p[2])

      ## Auxiliar variables
        self.AddVar( typ='Cnts', varid='Dt_dir', prn=r'$Dt_dir',\
                    desc="This constant save in ModMod the Dt of principal director", \
                    units= s , val= 60*60*24) # 60 * 60 * 24 The val is the number of seconds per day  
        
        self.AddVar( typ='Cnts', varid='Dt_pho', prn=r'$Dt_pho',\
                    desc="This constant save in ModMod the Dt of photosynthesis module", \
                    units= s , val= 60 )  #60 antes# The val is the number of seconds per minute  
       

        self.AddVar( typ='State', varid='ind_pho', prn=r'$ind_pho',\
                    desc="It is a global auxiliary variable that allows to control the index that is used to make the calculations of photosynthesis", \
                    units= 1 , val= - int( self.V('Dt_dir') / self.V('Dt_pho') ) ) # The val is minus the number of steps that must do photosynthesis module per each principal director step
        

    def RHS(self, Dt):
        """RHS( Dt ) = 
           
           ************* IN ASSIGMENT RHSs WE DON'T NEED TO CALL STATE VARS WITH self.Vk ******************
        """
        ### The assigment is the total weight of the fuits
        return self.V('Q')