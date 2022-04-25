from typing import Tuple
import numpy as np
from .functions import * 
from ModMod import Director
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
        self.sch = list()
        self.Dt = 1
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

    #def Run(self, Dt, n, sch, save=None, active=True):
    #    return super().Run(Dt, n, sch, save, active)


    #def Advance(self, t1): # un día en segundos
    #    n = int(t1 / self.Dt)
    #    try:
    #        self.Run(Dt=self.Dt, n=n, sch=self.sch, save=None,active=False)
    #    except:
    #        print('Error en Run')
    #        return 0

    #    return 1
