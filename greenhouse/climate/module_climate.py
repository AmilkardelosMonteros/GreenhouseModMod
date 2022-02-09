from ModMod import Module
from scipy.stats import norm

class Module1(Module):
    def __init__(self, Dt=1, **kwargs):
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt)  # Time steping of module
        # Always, use the super class __init__, theare are several otjer initializations
        # Module specific constructors, add RHS's
        for key, value in kwargs.items():
            self.AddStateRHS(key, value)
        # print("State Variables for this module:", self.S_RHS_ids)

    def Advance(self, t1):
        T1r = self.V('T1') 
        T2r = self.V('T2') 
        V1r = self.V('V1') 
        C1r = self.V('C1') 
        # Actualización de las variables
        self.V_Set('T1', T1r)
        self.V_Set('T2', T2r)
        self.V_Set('V1', V1r)
        self.V_Set('C1', C1r)
        # Avance del RHS
        self.AdvanceRungeKutta(t1)
        return 1
