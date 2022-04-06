from ModMod import StateRHS
from sympy import symbols
from .functions import b1
from .functions import q6
from .functions import l2 
from .functions import g3, g4
from .functions import kappa2
from .functions import n1, n2, n3
from .functions import r8, r9, r10, r11, r12, r13
from .functions import f1, f2, f3, f4, f5, f6, f7
from .functions import h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11

state_names = ['T1', 'V1', 'T2']
control_names = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6','U7', 'U8', 'U9', 'U11']
input_names = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8']
#function_names = ['f1','h4', 'h6']
function_names = ['h1','h2','h3','h4','h5','h6','r8','h7','h10','l2','r10','h11']
constant_names = ['tau3', 'phi7', 'alpha6', 'eta6', 'eta7', 'eta8', 'phi8', 'nu4', 'nu5', 
                    'omega1', 'nu6', 'beta3', 'gamma1', 'phi1', 'tau1','tau2', 'lamb5', 'lamb7', 
                    'lamb8', 'alpha5', 'nu1', 'eta10', 'nu3', 'nu2', 'eta11', 'alpha8', 
                    'alpha9', 'eta2', 'eta3', 'sigma', 'epsil3', 'epsil4', 'epsil5', 'epsil6', 
                    'phi2', 'alpha4', 'gamma2', 'eta5', 'phi5', 'phi6', 'lamb1', 'lamb2', 
                    'lamb3', 'lamb4', 'alpha2', 'alpha7', 'eta1', 'phi9', 'nu7', 'nu8', 'lamb6']
  
all_parameters = state_names + control_names + input_names + function_names + constant_names

########### T2 ############
class T2_rhs(StateRHS):
    """Define a RHS, this is the rhs for T2, Greenhouse air temperature"""
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
        b_1 = b1(U1=self.V('U1'), tau3=self.V('tau3'))
        f_1 = f1(U2=self.V('U2'), phi7=self.V('phi7'), alpha6=self.V('alpha6'))
        n_1 = n1(U5=self.V('U5'), nu1=self.V('nu1'), eta10=self.V('eta10'))
        n_2 = n2(U6=self.V('U6'), nu3=self.V('nu3'))
        n_3 = n3(U5=self.V('U5'), nu2=self.V('nu2'), eta11=self.V('eta11'))
        f_5 = f5(I8=self.V('I8'), alpha6=self.V('alpha6'), n1=n_1, n2=n_2, n3=n_3)
        f_6 = f6(I8=self.V('I8'), nu4=self.V('nu4'))
        f_2 = f2(U1=self.V('U1'), eta6=self.V('eta6'), eta7=self.V('eta7'), eta8=self.V('eta8'), f5=f_5, f6=f_6)
        f_3 = f3(U7=self.V('U7'), phi8=self.V('phi8'), alpha6=self.V('alpha6'))
        f_7 = f7(T2=self.Vk('T2'), U8=self.V('U8'), I5=self.V('I5'), I8=self.V('I8'), nu5=self.V('nu5'), alpha6=self.V('alpha6'), omega1=self.V('omega1'), nu6=self.V('nu6'), n1=n_1, n3=n_3)
        f_4 = f4(U1=self.V('U1'), eta6=self.V('eta6'), eta7=self.V('eta7'), eta8=self.V('eta8'), f6=f_6, f7=f_7)
        g_3 = g3(I1=self.V('I1'), beta3=self.V('beta3'), gamma1=self.V('gamma1'), phi1=self.V('phi1'), tau1=self.V('tau1'), b1=b_1)
        g_4 = g4(U1=self.V('U1'), tau2=self.V('tau2'))
        h_8 = h8(T2=self.Vk('T2'), I5=self.V('I5'), I8=self.V('I8'), alpha6=self.V('alpha6'), lamb5=self.V('lamb5'), lamb6=self.V('lamb6'), lamb7=self.V('lamb7'), lamb8=self.V('lamb8'))
        h_9 = h9(T2=self.Vk('T2'), I5=self.V('I5'), alpha5=self.V('alpha5'), rho3=self.V('rho3'), f4=f_4)
        q_6 = q6(I6=self.V('I6'))
        r_9 = r9(I2=self.V('I2'), alpha8=self.V('alpha8'), alpha9=self.V('alpha9'), eta2=self.V('eta2'), eta3=self.V('eta3'))
        r_11 = r11(T2=self.Vk('T2'), I4=self.V('I4'), lamb=self.V('sigma'), epsil3=self.V('epsil3'), epsil4=self.V('epsil4'), g3=g_3)
        r_12 = r12(T2=self.Vk('T2'), I4=self.V('I4'), lamb=self.V('sigma'), epsil3=self.V('epsil3'), epsil5=self.V('epsil5'), g4=g_4)
        r_13 = r13(T2=self.Vk('T2'), I4=self.V('I4'), lamb=self.V('sigma'), epsil3=self.V('epsil3'), epsil6=self.V('epsil6'))
        #### Principal functions ####
        kappa_2 = kappa2(alpha5=self.V('alpha5'),rho3=self.V('rho3'), phi2=self.V('phi2'))
        
        h_1 = h1(T1=self.Vk('T1'), T2=self.Vk('T2'),I1=self.V('I1'), alpha4=self.V('alpha4'))
        h_2 = h2(I5=self.V('I5'), alpha5=self.V('alpha5'), gamma2=self.V('gamma2'), eta5=self.V('eta5'), rho3=self.V('rho3'), phi5=self.V('phi5'), phi6=self.V('phi6'), f1=f_1)
        h_3 = h3(T2=self.Vk('T2'), V1=self.Vk('V1'), U3=self.V('U3'), I6=self.V('I6'), lamb1=self.V('lamb1'), lamb2=self.V('lamb2'), alpha6=self.V('alpha6'), gamma2=self.V('gamma2'), q6=q_6)
        h_4 = h4(T2=self.Vk('T2'), I3=self.V('I3'),gamma1=self.V('gamma1'), phi1=self.V('phi1'))
        h_5 = h5(T2=self.Vk('T2'), I7=self.V('I7'), lamb3=self.V('lamb3'))
        h_6 = h6(U4=self.V('U4'), lamb4=self.V('lamb4'), alpha6=self.V('alpha6')) #H blow air 
        r_8 = r8(I2=self.V('I2'), alpha2=self.V('alpha2'), alpha7=self.V('alpha7'), eta1=self.V('eta1'), eta2=self.V('eta2'), eta3=self.V('eta3'), tau1=self.V('tau1'), r9=r_9)
        h_7 = h7(T2=self.Vk('T2'), I5=self.V('I5'), alpha5=self.V('alpha5'), rho3=self.V('rho3'), f2=f_2, f3=f_3, h8=h_8, h9=h_9)
        h_10 = h10(T2=self.Vk('T2'), alpha5=self.V('alpha5'), rho3=self.V('rho3'), f1=f_1)
        l_2 = l2(U9=self.V('U9'), alpha6=self.V('alpha6'),gamma2=self.V('gamma2'), phi9=self.V('phi9'))
        r_10 = r10(r11=r_11, r12=r_12, r13=r_13)
        h_11 = h11(T2=self.Vk('T2'), I7=self.V('I7'), nu7=self.V('nu7'), nu8=self.V('nu8'), phi2=self.V('phi2'))
        ###Save 
        to_save = {'h1':h_1,'h2':h_2,'h3':h_3,'h4':h_4,'h5':h_5,'h6':h_6,'r8':r_8,'h7':h_7,'h10':h_10,'l2':l_2,'r10':r_10,'h11':h_11}
        [self.mod.V_Set(k, v) for k,v in to_save.items()]
        return (kappa_2**-1)*(h_1 + h_2 + h_3 + h_4 + h_5 + h_6 + r_8 - h_7 - h_10 - l_2 - r_10 - h_11)