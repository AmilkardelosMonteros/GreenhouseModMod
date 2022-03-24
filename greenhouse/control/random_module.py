from ModMod import Module
import numpy as np

class Random(Module):
    def __init__(self, controls, Dt=1):
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt)  # Time steping of module
        # Always, use the super class __init__, theare are several otjer initializations
        # Module specific constructors, add RHS's
        self.controls = controls
        # print("State Variables for this module:", self.S_RHS_ids)


    def Advance(self, t1):
        for c in self.controls:
            val =  np.random.uniform(0, 0.25)
            if c == 'U4':
                val = 0
            if c == 'U10':
                val = 1.0
            if c in ['U6','U7','U8']:
                val = 0.5
            if c == 'U5':
                val = 1.0
            self.V_Set(c, val)
        return 1