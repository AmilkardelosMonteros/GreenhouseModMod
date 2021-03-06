from ModMod import Module
from scipy.stats import norm


class ModuleControls(Module):
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
        ## Actualización de los flujos de interés  --- Nota: Dentro de este método no se puede usar self.Vk, únicamente self.V
        ## Avance del RHS
        #self.AdvanceRungeKutta(t1)
        self.AdvanceAssigment(t1)
        return 1