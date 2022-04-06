from ModMod import StateRHS
from sympy import symbols
from .functions import q1, q2, q3, q4, q5, q7, q8, q9, q10
from .functions import r1, r2, r3, r4, r5, r6, r7 
from .functions import kappa1
from .functions import g1, g2
from .functions import a1
from .functions import b1
from .functions import p1
from .functions import l1
from .functions import h1

state_names = ['T1', 'V1', 'T2', 'C1']
control_names = ['U1', 'U11']
input_names = ['I1', 'I2', 'I3', 'I4','I9']
#function_names = ['a1', 'r6', 'p1', 'q1', 'q2', 'q3', 'q4', 'q5', 'q7', 'q8', 'q9', 'q10', 'g1']
function_names = ['r1','r5','r6','h1','l1','r7']
constant_names = ['beta3', 'tau3', 'beta1', 'rho1', 'beta2', 'rho2', 'eta1', 'eta2', 'tau1', 
                    'tau2', 'rho3', 'alpha5', 'gamma', 'gamma3', 'delta1', 'delta2', 'delta3',
                    'gamma4', 'gamma5', 'delta4', 'delta5', 'delta6', 'delta7', 'eta4', 'alpha1',
                    'alpha2', 'eta3', 'alpha3', 'epsil1', 'epsil2', 'sigma', 'alpha4', 'epsil3']

all_parameters = state_names + control_names + input_names + function_names + constant_names

class T1_rhs(StateRHS):
    """Define a RHS, this is the rhs for C1, the CO2 concentrartion in the greenhouse air"""
    def __init__(self,parameters):
        """Define a RHS, ***this an assigment RHS***, V1 = h2(...), NO ODE."""
        # uses the super class __init__
        super().__init__()
        self.SetSymbTimeUnits(parameters['dt'])  # minuts
        for name in all_parameters:
            parameters[name].addvar_rhs(self)

    def RHS(self, Dt):
        #print('T1')
        #breakpoint()
        """RHS( Dt, k) = \kappa_1^{-1} F_1( t+Dt, X+k) where X is the current value of
           all state variables.  k is a simple dictionary { 'v1':k1, 'v2':k2 ... etc}
           ************* JUST CALL STATE VARIABLES WITH self.Vk ******************
        """
        # Direct usage, NB: State variables need to used Vk, so that X+k is evaluated.
        # This can be done with TranslateArgNames(h1)
        # Once defined h1 in your terminal run TranslateArgNames(h1)
        # and follow the instrucions
        #### Sub-functions ####
        self.mod.V_Set('I9', self.V('I2')) 
        a_1 = a1(I1=self.V('I1'), beta3=self.V('beta3'))
        b_1 = b1(U1=self.V('U1'), tau3=self.V('tau3'))
        r_4 = r4(I2=self.V('I2'), eta1=self.V('eta1'),eta2=self.V('eta2'), tau1=self.V('tau1'))
        r_2 = r2(I1=self.V('I1'), beta1=self.V('beta1'), rho1=self.V('rho1'), r4=r_4)
        r_3 = r3(I1=self.V('I1'), beta1=self.V('beta1'), beta2=self.V('beta2'), rho1=self.V('rho1'), rho2=self.V('rho2'), r4=r_4)
        g_1 = g1(a1=a_1)  
        g_2 = g2(tau2=self.V('tau2'), b1=b_1)                                 #auxiliar para r6
        q_2 = q2(T1=self.Vk('T1'))
        q_7 = q7(I9=self.V('I9'), delta1=self.V('delta1'), gamma5=self.V('gamma5'))
        q_8 = q8(delta4=self.V('delta4'), delta5=self.V('delta5'), q7=q_7)
        q_9 = q9(delta6=self.V('delta6'), delta7=self.V('delta7'), q7=q_7)
        q_4 = q4(C1=self.Vk('C1'), eta4=self.V('eta4'), q8=q_8)
        q_5 = q5(V1=self.Vk('V1'), q2=q_2, q9=q_9)
        q_10 = q10(I9=self.V('I9'), delta2=self.V('delta2'), delta3=self.V('delta3'))
        q_3 = q3(I9=self.V('I9'), gamma4=self.V('gamma4'), q4=q_4, q5=q_5, q10=q_10)
        q_1 = q1(I1=self.V('I1'), rho3=self.V('rho3'), alpha5=self.V('alpha5'), gamma=self.V('gamma'), gamma2=self.V('gamma2'), gamma3=self.V('gamma3'), q3=q_3)
        p_1 = p1(V1=self.Vk('V1'), q1=q_1, q2=q_2)
        #### Principal functions ####
        kappa_1 = kappa1(I1=self.V('I1'), alpha1=self.V('alpha1'))
        r_1 = r1(r2=r_2, r3=r_3)
        r_5 = r5(I2=self.V('I2'), alpha2=self.V('alpha2'),eta1=self.V('eta1'), eta3=self.V('eta3'))
        r_6 = r6(T1=self.Vk('T1'), I3=self.V('I3'), alpha3=self.V('alpha3'), epsil1=self.V('epsil1'), epsil2=self.V('epsil2'), lamb=self.V('sigma'), g1=g_1)
        h_1 = h1(T1=self.Vk('T1'), T2=self.Vk('T2'),I1=self.V('I1'), alpha4=self.V('alpha4'))
        l_1 = l1(gamma2=self.V('gamma2'), p1=p_1)
        r_7 = r7(T1=self.Vk('T1'), I4=self.V('I4'), epsil2=self.V('epsil2'), epsil3=self.V('epsil3'), lamb=self.V('sigma'), a1=a_1, g2=g_2)
        #Save
        to_save = {'r1':r_1,'r5':r_5,'r6':r_6,'h1':h_1,'l1':l_1,'r7':r_7}
        [self.mod.D.Vars[k].Set(v) for k,v in to_save.items()]
        return (kappa_1**-1)*(r_1 + r_5 + r_6 - h_1 - l_1 - r_7)


