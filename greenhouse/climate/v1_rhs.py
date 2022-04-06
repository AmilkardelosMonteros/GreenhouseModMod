from ModMod import StateRHS
from sympy import symbols
from .functions import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10
from .functions import f1, f2, f3, f4, f5, f6, f7
from .functions import p1, p2, p3, p4, p5, p6, p7
from .functions import n1, n2, n3
from .functions import h3, h6
from .functions import kappa3
import numpy as np

state_names = ['T1', 'V1', 'T2', 'C1']
control_names = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9']
input_names = ['I8', 'I5', 'I6', 'I1', 'I11']
#function_names = ['h6', 'f1', 'p1', 'p2', 'p3', 'q1', 'q2', 'q3', 'q4', 'q5', 'q7', 'q8', 'q9', 'q10']
function_names = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
constant_names = ['lamb4', 'alpha6', 'phi7', 'eta6', 'eta7', 'eta8', 'phi8', 'nu4', 'nu5',
                            'omega1', 'nu6', 'lamb1', 'lamb3', 'gamma2', 'nu1', 'eta10', 'nu3', 
                            'nu2', 'eta11', 'rho3', 'alpha5', 'gamma', 'gamma3', 'delta1', 'delta2', 
                            'delta3', 'delta4', 'gamma4', 'gamma5', 'delta5', 'delta6', 'delta7', 
                            'eta4', 'psi1', 'phi2', 'omega2', 'eta5', 'phi5', 'phi6', 'phi9', 'eta12']

all_parameters = state_names + control_names + input_names + function_names + constant_names

class V1_rhs(StateRHS):
    """Define a RHS, this is the rhs for V1, the vapour pression in the greenhouse air"""
    def __init__(self,parameters):

        """Define a RHS, ***this an assigment RHS***, V1 = h2(...), NO ODE."""
        # uses the super class __init__
        super().__init__()
        self.SetSymbTimeUnits(parameters['dt'])  # minuts 
        for name in all_parameters:
            parameters[name].addvar_rhs(self)

    def RHS(self, Dt):

        """RHS( Dt, k) = \kappa_1^{-1} F_1( t+Dt, X+k) where X is the current value of
           all state variables.  k is a simple dictionary { 'v1':k1, 'v2':k2 ... etc}
           ************* JUST CALL STATE VARIABLES WITH self.Vk ******************
        """
        # Direct usage, NB: State variables need to used Vk, so that X+k is evaluated.
        # This can be done with TranslateArgNames(h1)
        # Once defined h1 in your terminal run TranslateArgNames(h1)
        # and follow the instrucions
        #### Sub-functions ####
        #print('V1')
        # breakpoint()
        h_6 = h6(U4=self.V('U4'), lamb4=self.V('lamb4'), alpha6=self.V('alpha6')) #H blow air 
        f_1 = f1(U2=self.V('U2'), phi7=self.V('phi7'), alpha6=self.V('alpha6'))
        f_3 = f3(U7=self.V('U7'), phi8=self.V('phi8'), alpha6=self.V('alpha6'))
        f_6 = f6(I8=self.V('I8'), nu4=self.V('nu4'))
        n_1 = n1(U5=self.V('U5'), nu1=self.V('nu1'), eta10=self.V('eta10'))
        n_2 = n2(U6=self.V('U6'), nu3=self.V('nu3'))
        n_3 = n3(U5=self.V('U5'), nu2=self.V('nu2'), eta11=self.V('eta11'))
        f_5 = f5(I8=self.V('I8'), alpha6=self.V('alpha6'), n1=n_1, n2=n_2, n3=n_3)
        f_2 = f2(U1=self.V('U1'), eta6=self.V('eta6'), eta7=self.V('eta7'), eta8=self.V('eta8'), f5=f_5, f6=f_6)
        f_7 = f7(T2=self.Vk('T2'), U8=self.V('U8'), I5=self.V('I5'), I8=self.V('I8'), nu5=self.V('nu5'), alpha6=self.V('alpha6'), omega1=self.V('omega1'), nu6=self.V('nu6'), n1=n_1, n3=n_3)
        f_4 = f4(U1=self.V('U1'), eta6=self.V('eta6'), eta7=self.V('eta7'), eta8=self.V('eta8'), f6=f_6, f7=f_7)
        q_2 = q2(T1=self.Vk('T1')) 
        q_7 = q7(I9=self.V('I9'), delta1=self.V('delta1'), gamma5=self.V('gamma5'))
        q_8 = q8(delta4=self.V('delta4'), delta5=self.V('delta5'), q7=q_7)
        q_9 = q9(delta6=self.V('delta6'), delta7=self.V('delta7'), q7=q_7)
        q_4 = q4(C1=self.Vk('C1'), eta4=self.V('eta4'), q8=q_8)
        q_5 = q5(V1=self.Vk('V1'), q2=q_2, q9=q_9)
        q_6 = q6(I6=self.V('I6'))
        q_10 = q10(I9=self.V('I9'), delta2=self.V('delta2'), delta3=self.V('delta3'))
        q_3 = q3(I9=self.V('I9'), gamma4=self.V('gamma4'), q4=q_4, q5=q_5, q10=q_10)
        q_1 = q1(I1=self.V('I1'), rho3=self.V('rho3'), alpha5=self.V('alpha5'), gamma=self.V('gamma'), gamma2=self.V('gamma2'), gamma3=self.V('gamma3'), q3=q_3)
        h_3 = h3(T2=self.Vk('T2'), V1=self.Vk('V1'), U3=self.V('U3'), I6=self.V('I6'), lamb1=self.V('lamb1'), lamb2=self.V('lamb2'), alpha6=self.V('alpha6'), gamma2=self.V('gamma2'), q6=q_6)
        #### Principal functions ####
        kappa_3 = kappa3(T2=self.Vk('T2'), psi1=self.V('psi1'), phi2=self.V('phi2'), omega2=self.V('omega2'))
        p_1 = p1(V1=self.Vk('V1'), q1=q_1, q2=q_2)
        p_2 = p2(rho3=self.V('rho3'), eta5=self.V('eta5'),phi5=self.V('phi5'), phi6=self.V('phi6'), f1=f_1)
        p_3 = p3(U9=self.V('U9'), phi9=self.V('phi9'), alpha6=self.V('alpha6'))
        p_4 = p4(eta12=self.V('eta12'), h6=h_6)
        p_5 = p5(T2=self.Vk('T2'), V1=self.Vk('V1'), I5=self.V('I5'),I11=self.V('I11'),psi1=self.V('psi1'), omega2=self.V('omega2'), f2=f_2, f3=f_3, f4=f_4)
        p_6 = p6(T2=self.Vk('T2'), V1=self.Vk('V1'), psi1=self.V('psi1'), omega2=self.V('omega2'), f1=f_1)
        p_7 = p7(V1=self.Vk('V1'), h3=h_3, q6=q_6)
        #Save
        to_save = {'p1':p_1, 'p2':p_2, 'p3':p_3, 'p4':p_4, 'p5':p_5, 'p6':p_6, 'p7':p_7}
        [self.mod.V_Set(k, v) for k,v in to_save.items()]
        return (kappa_3**-1)*(p_1 + p_2 + p_3 + p_4 - p_5 - p_6 - p_7)