from ModMod import StateRHS
from sympy import symbols
import pandas as pd
from numpy import max
import csv 
state_names = ['U7']
control_names  = ['U7_c']
constant_names = ['lambda']


all_parameters =  state_names + constant_names + control_names

mt = symbols('mt')

def insert_data(result,i):
    if i == 0:
        with open('Validacion/u7_1.csv', 'w') as f: 
            writer = csv.writer(f)
            writer.writerow(['U7','U7c'])
    try:
        with open(r'Validacion/u7_1.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(result)
    except:
        print('Revisa')


class U7_rhs(StateRHS):
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
        U7     = self.V('U7') 
        if U7 > 1 or U7 < 0:
            print('No sabes resolver EDOs')
        U7c     = self.V('U7_c')
        lambda_ = self.V('lambda')
        #result  = [U7,U7c] 
        #insert_data(result,self.i)
        #self.i +=1
        #if self.i > 1000000:
        #    self.i = 0 
        return lambda_*max([U7,0.05])*(U7c - U7)
