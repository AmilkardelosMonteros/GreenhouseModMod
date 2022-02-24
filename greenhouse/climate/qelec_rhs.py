from ModMod import StateRHS

"""Pendiente!!!"""

all_parameters = []


class QElec_rhs(StateRHS):
    """Define a RHS, this is the rhs for QH2O"""
    def __init__(self, parameters):
        # uses the super class __init__
        super().__init__()
        self.SetSymbTimeUnits(parameters['dt'])  # minuts
        for name in all_parameters:
            parameters[name].addvar_rhs(self)
        
    def RHS(self, Dt):
        pass 