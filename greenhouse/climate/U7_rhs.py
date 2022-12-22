from ModMod import StateRHS
from sympy import symbols
import pandas as pd
from numpy import max
state_names = ['U7']
control_names  = ['U7_c']
constant_names = ['lambda']


all_parameters =  state_names + constant_names + control_names

mt = symbols('mt')

def insert_data(result,i,path):
    try:
        data = pd.read_csv(path+'/u7.csv')
    except:
        data = pd.DataFrame(columns=['U7','U7_c'])
    try:
        data.loc[i] = result
        data.to_csv(path+'/u7.csv',index=0)
    except:
        breakpoint()



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
        result  = [U7,U7c] 
        insert_data(result,self.i,'Validacion')
        self.i +=1
        return lambda_*max([U7,0.05])*(U7c - U7)
