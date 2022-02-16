from ModMod import Module
from scipy.stats import norm
from .functions import o2, kappa3, h1


class ModuleCosts(Module):
    def __init__(self, Dt=1, **kwargs):
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt)  # Time steping of module
        # Always, use the super class __init__, theare are several otjer initializations
        # Module specific constructors, add RHS's
        for key, value in kwargs.items():
            breakpoint()
            self.AddStateRHS(key, value)
        # print("State Variables for this module:", self.S_RHS_ids)


    def Advance(self, t1):
        ## Actualización de los flujos de interés  --- Nota: Dentro de este método no se puede usar self.Vk, únicamente self.V
        o_2 = o2( U10=self.V('U10'), psi2=self.V('psi2'), alpha6=self.V('alpha6') )
        kap_3 = kappa3( T2=self.V('T2'), psi1=self.V('psi1'), phi2=self.V('phi2'), omega2=self.V('omega2') )
        h_1 = h1( T1=self.V('T1'), T2=self.V('T2'), I1=self.V('I1'), alpha4=self.V('alpha4') )
        #self.V_Set('o2R', o_2)
        #self.V_Set('kap3R', kap_3)
        #self.V_Set('h1R', h_1)
        ## Avance del RHS
        self.AdvanceRungeKutta(t1)
        return 1