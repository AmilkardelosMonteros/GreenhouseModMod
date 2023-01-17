from ModMod import StateRHS
from sympy import symbols
import pandas as pd
from numpy import max
import csv 
state_names = ['U6']
control_names  = ['U6_c']
constant_names = ['lambda']


all_parameters =  state_names + constant_names + control_names

mt = symbols('mt')

def insert_data(result,i):
    if i == 0:
        with open('Validacion/u6.csv', 'w') as f: 
            writer = csv.writer(f)
            writer.writerow(['U6','U6c'])
    try:
        with open(r'Validacion/u6.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(result)
    except:
        print('Revisa')


class U6_rhs(StateRHS):
    """Define a RHS, this is the rhs for U7"""
    def __init__(self, parameters):
        # uses the super class __init__
        super().__init__()
        #self.SetSymbTimeUnits(mt)  # minutes
        #self.SetSymbTimeUnits(parameters['dt'])  # minutes
        for name in all_parameters:
            parameters[name].addvar_rhs(self)
        self.i = 0

    def RHS(self, Dt):
        U6     = self.V('U6') 
        if U6 > 1 or U6 < 0:
            print('No sabes resolver EDOs')
        U6c     = self.V('U6_c')
        lambda_ = self.V('lambda')
        #result  = [U6,U6c] 
        #insert_data(result,self.i)
        #self.i +=1
        #if self.i > 1000000:
        #    self.i = 0 
        return lambda_*max([U6,0.05])*(U6c - U6)