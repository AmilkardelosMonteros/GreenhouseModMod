from ast import Constant
from ModMod import StateRHS
from sympy import symbols
from .functions import H_Boil_Pipe


state_names = ['Qgas']
constant_names = ['qgas', 'etagas']
function_names = ['h6', 'r6', 'h4', 'a1', 'g1'] 

all_parameters =  function_names + state_names + constant_names


class Qgas_rhs(StateRHS):
    """Define a RHS, this is the rhs for Qgas, the gas cost per m^2"""
    def __init__(self, parameters):
        # uses the super class __init__
        super().__init__()
        #self.SetSymbTimeUnits(parameters['dt'])  # minuts
        for name in all_parameters:
            parameters[name].addvar_rhs(self)
   
    def RHS(self, Dt):
        h_6 = self.V('h6')
        r_6 = self.V('r6')
        h_4 = self.V('h4')
        H_boil_pipe = H_Boil_Pipe(r_6, h_4)
        return (self.V('qgas')/self.V('etagas'))*(H_boil_pipe + h_6)/(10**9)