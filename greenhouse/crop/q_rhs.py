#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:00:07 2022

@author: jdmolinam
"""

from asyncio import constants
from ModMod import StateRHS
from .functions import m, d, C, g, mu_mol_phot, n_f, MJ # importar simbolos 


global_constants = ['k1_TF', 'k2_TF']
local_constants = ['k3_TF', 'dw_ef', 'dw_ef_veg','a_ef', 'C_t', 'B', 'D', 'M', 'a', 'b']
states = ['T', 'PAR']
local_states = ['A', 'Q', 'm_k', 'n_k', 'h_k', 'Q_h', 'Y_sum']
local_parameters = local_states + local_constants
global_parameters = states + global_constants


#################################################################
############ RHS modelo de crecimiento ##########################
#################################################################    
class Q_rhs(StateRHS):
    """
    Q is the weight of all fruits for plant
    """
    def __init__( self, parameters):
        """Define a RHS, ***this an assigment RHS***, V1 = h2(...), NO ODE."""
        ### uses the super class __init__
        super().__init__()
        for name in local_parameters:
           parameters[name].addvar_rhs(self, local=True)
        for name in global_parameters:
            parameters[name].addvar_rhs(self)
        ### Define variables here.  Each fruit will have repeated variables.
        ### Later some will be shared and the Local variable swill be exclusive
        ### of each fruit.
        
        self.SetSymbTimeUnits(d) # days


    def RHS(self, Dt):
        """RHS( Dt ) = 
           
           ************* IN ASSIGMENT RHSs WE DON'T NEED TO CALL STATE VARS WITH self.Vk ******************
        """
        ### The assigment is the total weight of the fuits
        return self.V('Q')