from ModMod import StateRHS

constant_names = ['alpha12', 'cost_elect']
state_names = ['Qelec']
controls = ['U12']
all_parameters = constant_names + state_names + controls


class Qelec_rhs(StateRHS):
    """Define a RHS, this is the rhs for QH2O"""
    def __init__(self, parameters):
        # uses the super class __init__
        super().__init__()
        #self.SetSymbTimeUnits(parameters['dt'])  # minuts
        for name in all_parameters:
            parameters[name].addvar_rhs(self)
        
    def RHS(self, Dt):
        '''Costo del electricidad '''
        U_12 = self.V('U12') 
        costelect = self.V('cost_elect')/(3.6 * 10**6) # transformo de ($ mxn)/kiloWatt-hola a ($ mxn) / Watt-seg
        # el resultado esta en $ mxn / m**-2 (ya que alpha12 esta en Watt * m**-2)
        #breakpoint()
        return costelect*self.V('alpha12')*U_12 