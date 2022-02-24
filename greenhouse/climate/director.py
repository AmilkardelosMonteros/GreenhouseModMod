from typing import Tuple
import numpy as np
from ModMod import Director
from .functions import * 
from scipy.stats import norm
from .t1_rhs import T1_rhs
from .t2_rhs import T2_rhs
from .v1_rhs import V1_rhs
from .c1_rhs import C1_rhs
from .module_climate import Module1
### Notice 95 T1


class Climate_model(Director):
    def __init__(self):#, dic_RHS):
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={})
        '''
        C1_rhs_ins = dic_RHS['C1']
        V1_rhs_ins = dic_RHS['V1']
        T1_rhs_ins = dic_RHS['T1']
        T2_rhs_ins = dic_RHS['T2']
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={}) 
        symb_time_units = C1_rhs_ins.CheckSymbTimeUnits(C1_rhs_ins)
        # Genetare the director
        RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
        self.MergeVarsFromRHSs(RHS_list, call=__name__)
        self.AddModule('Module1', Module1(C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, 
                        T2=T2_rhs_ins))
        self.sch = ['Module1']
        '''

    def reset(self):
        self.V_Set('T1', 20) #!!!!!! Tiene que venir de los datos
        self.V_Set('T2', 20) 
        self.V_Set('V1', 1200) 
        self.V_Set('C1', 600) 


    def Run( self, Dt, n, sch, save=None):
        """Advance in Dt time steps, n steps with the scheduling sch.
           Save the variables with varid's in save.  Defualt: all State variables.
        """
        # RHS qH2o
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
        self.V_Set('h4', h_4)
        return super().Run(Dt, n, sch, save) 
