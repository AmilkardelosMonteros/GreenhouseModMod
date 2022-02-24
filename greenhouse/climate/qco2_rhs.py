from ModMod import StateRHS
from sympy import symbols

state_names = ['Qco2']
constant_names = ['q_co2_ext']
function_names = ['o2'] 

all_parameters =  function_names + state_names + constant_names

mt = symbols('mt')

class Qco2_rhs(StateRHS):
    """Define a RHS, this is the rhs for Qco2, the co2 cost per m^2"""
    def __init__(self, parameters):
        # uses the super class __init__
        super().__init__()
        self.SetSymbTimeUnits(mt)  # minutes
        self.SetSymbTimeUnits(parameters['dt'])  # minutes
        for name in all_parameters:
            parameters[name].addvar_rhs(self)

    def RHS(self, Dt):
        '''Costo del CO_2'''
        o_2 = self.V('o2')
        return (10**-6)*self.V('q_co2_ext')*o_2