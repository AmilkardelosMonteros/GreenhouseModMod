from auxModMod.Dir import Module
from scipy.stats import norm
from .functions import * 
class Module1(Module):
    def __init__(self, Dt=1, **kwargs):
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt)  # Time steping of module
        # Always, use the super class __init__, theare are several otjer initializations
        # Module specific constructors, add RHS's
        self.i = 0
        for key, value in kwargs.items():
            self.AddStateRHS(key, value)
        # print("State Variables for this module:", self.S_RHS_ids)
        
    def Advance(self, t1):
        self.AdvanceRungeKutta(t1)
        return 1