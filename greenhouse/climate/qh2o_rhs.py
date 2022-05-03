from ModMod import StateRHS
from sympy import symbols


mt = symbols('mt')
state_names = ['Qh2o']
function_names = ['p1', 'p2', 'p3']
constant_names = ['alpha6', 'etadrain']

all_parameters =  function_names + state_names + constant_names


class Qh2o_rhs(StateRHS):
    """Define a RHS, this is the rhs for Qh20, the water cost per kg"""
    def __init__(self, parameters):
        # uses the super class __init__
        super().__init__()
        #self.SetSymbTimeUnits(parameters['dt'])  # minuts
        for name in all_parameters:
            parameters[name].addvar_rhs(self)
        
    def RHS(self, Dt):
        p_1 = self.V('p1')
        p_2 = self.V('p2')
        p_3 = self.V('p3')
        return (10**-3)*((1+ self.V('etadrain')/100.0)*max(p_1, 0) + p_2 + p_3)  