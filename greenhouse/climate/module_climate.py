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
        #print('Advance!!')
        f_1 = f1(U2=self.V('U2'), phi7=self.V(
            'phi7'), alpha6=self.V('alpha6'))
        q_2 = q2(T1=self.V('T1')) #### Previously T1 = self.Vk('T1')
        q_7 = q7(I9=self.V('I9'), delta1=self.V(
            'delta1'), gamma5=self.V('gamma5'))
        q_8 = q8(delta4=self.V('delta4'), delta5=self.V('delta5'), q7=q_7)
        q_9 = q9(delta6=self.V('delta6'), delta7=self.V('delta7'), q7=q_7)
        q_4 = q4(C1=self.V('C1'), eta4=self.V('eta4'), q8=q_8)
        q_5 = q5(V1=self.V('V1'), q2=q_2, q9=q_9)
        q_10 = q10(I9=self.V('I9'), delta2=self.V(
            'delta2'), delta3=self.V('delta3'))
        q_3 = q3(I9=self.V('I9'), gamma4=self.V(
            'gamma4'), q4=q_4, q5=q_5, q10=q_10)
        q_1 = q1(I1=self.V('I1'), rho3=self.V('rho3'), alpha5=self.V('alpha5'), gamma=self.V(
            'gamma'), gamma2=self.V('gamma2'), gamma3=self.V('gamma3'), q3=q_3)
        p_1 = p1(V1=self.V('V1'), q1=q_1, q2=q_2) #### Previously T1 = self.Vk('T1')
        
        p_2 = p2(rho3=self.V('rho3'), eta5=self.V('eta5'),
                    phi5=self.V('phi5'), phi6=self.V('phi6'), f1=f_1)
        p_3 = p3(U9=self.V('U9'), phi9=self.V(
            'phi9'), alpha6=self.V('alpha6'))
        
        self.V_Set('f1', f_1)
        self.V_Set('q1', q_1)
        self.V_Set('q2', q_2)
        self.V_Set('q3', q_3)
        self.V_Set('q7', q_7)
        self.V_Set('q8', q_8)
        self.V_Set('q9', q_9)
        self.V_Set('q4', q_4)
        self.V_Set('q5', q_5)
        self.V_Set('q10', q_10)

        # variables for RHS qH2o
        self.V_Set('p1', p_1)
        self.V_Set('p2', p_2)
        self.V_Set('p3', p_3)

        # RHS qCo2
        o_2 = o2(U10=self.V('U10'), psi2=self.V('psi2'), alpha6=self.V('alpha6')) #MC_ext_air
        
        # variables for RHSs qCo2
        self.V_Set('o2', o_2)

        # RHS qGas
        h_6 = h6(U4=self.V('U4'), lamb4=self.V('lamb4'), alpha6=self.V('alpha6')) #H blow air 
        a_1 = a1(I1=self.V('I1'), beta3=self.V('beta3')) #auxiliar para g1
        g_1 = g1(a1=a_1)                                   #auxiliar para r6
        r_6 = r6(T1=self.V('T1'), I3=self.V('I3'), alpha3=self.V('alpha3'), epsil1=self.V('epsil1'), epsil2=self.V('epsil2'), lamb=self.V('sigma'), g1=g_1)
        h_4 = h4(T2=self.V('T2'), I3=self.V('I3'),gamma1=self.V('gamma1'), phi1=self.V('phi1'))

        self.V_Set('a1', a_1)
        self.V_Set('g1', g_1)

        # variables for RHSs qGas
        self.V_Set('h6', h_6)
        self.V_Set('r6', r_6)
        
        #T1r = self.V('T1') 
        #T2r = self.V('T2') 
        #V1r = self.V('V1') 
        #C1r = self.V('C1') 
        #print('Estas pasando por Advance')
        # Actualización de las variables
        #self.V_Set('T1', T1r)
        #self.V_Set('T2', T2r)
        #self.V_Set('V1', V1r)
        #self.V_Set('C1', C1r)
        # Avance del RHS
        self.AdvanceRungeKutta(t1)
        self.AdvanceAssigment(t1)
        self.i += 1
        if self.i % 1000 == 0:
            print(self.i)
        return 1
