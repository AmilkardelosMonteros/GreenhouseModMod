import numpy as np
import pandas as pd
import numpy as np
from time import time
import matplotlib.pyplot as plt
#from .climate.director import Climate_model
#from module_control import ModuleControl
#from director_production import I_2, Production_model
from ModMod import Director
from .climate. functions import Aclima
from sympy import symbols
from numpy import arange

n_f, n_p, MJ, g = symbols('n_f n_p MJ g') # number of fruits, number of plants

s, mol_CO2, mol_air, mol_phot, m, d, C, g, mol_O2, pa, ppm = symbols('s mol_CO2 mol_air mol_phot m d C g mol_O2 pa ppm')

class Greenhouse(Director):
    def __init__(self):
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={})
        self.Dt = None
        self.n = None
        self.AddVar( typ='State', varid='H', prn=r'$H_k$', desc="Accumulated weight of all harvested fruits.", units= g, val=0.0)
        self.AddVar( typ='State', varid='NF', prn=r'$N_k$', desc="Accumulated  number of fruits harvested", units= n_f, val=0.0)
        self.AddVar( typ='State', varid='h', prn=r'$h_k$', desc="Weight of all harvested fruits.", units= g, val=0.0)
        self.AddVar( typ='State', varid='n', prn=r'$n_k$', desc="Total  number of fruits harvested", units= n_f, val=0.0)
        self.AddVar( typ='State', varid='m', prn=r'$m_k$', desc="Simulation of the total  number of fruits harvested", units= n_f, val=0.0)
        self.AddVar( typ='State', varid='sum_A', prn=r'$ \sum A$',desc="Total assimilation rate", units= g * (m**-2), val=0,rec = 1440) ##Revisar
        self.AddVar( typ='State', varid='A_Mean', prn=r'$ E\\left( A\\right)$',desc="Total mean assimilation rate", units= g * (m**-2), val=0,rec = 1440) ##Revisar

        
    def Scheduler(self, t1, sch):
        """Advance the modules to time t1. sch is a list of modules id's to run
           its Advance method to time t1.
           
           Advance is the same interface, either if single module or list of modules.
        """
        
        for mod in sch:
            if self.Modules[mod].Advance(t1) != 1:
                print("Director: Error in Advancing Module '%s' from time %f to time %f" % ( mod, self.t, t1))
        self.t = t1
        
        ### Update Total weight and total number of fruits
        t_w_hist = 0.0
        t_n_f = 0
        t_w_k = 0.0
        t_n_k = 0
        t_m_k = 0
        sum_A = 0 
        A_Mean = 0
        A_int  = 0
        aclima = lambda x: Aclima(x, self.V('I1'))
        for plant in self.PlantList:
            t_w_hist += self.Modules[plant].Modules['Plant'].V('Q_h')
            t_n_f += self.Modules[plant].Modules['Plant'].n_fruits_h 
            t_w_k += self.Modules[plant].Modules['Plant'].V('h_k')
            t_n_k += self.Modules[plant].Modules['Plant'].V('n_k')
            t_m_k += self.Modules[plant].Modules['Plant'].V('m_k')
            sum_A += self.Modules[plant].Modules['Plant'].V('A')
            idx = int(self.Dt / self.Modules[plant].Modules['Photosynt'].Dt)
            #t = None if idx == 1 
            #A_Mean += self.Modules[plant].Modules['Photosynt'].V_Mean('A', ni=-idx)
            if idx == 1: 
                A_Mean += aclima(self.Modules[plant].Modules['Photosynt'].V('A'))
            else:
                try:
                    #breakpoint()
                    A_Mean += aclima(self.Modules[plant].Modules['Photosynt'].V_Int('A', ni=-idx,t=arange(0, 60*idx, 60))/(60*idx))
                except:
                    breakpoint() 
        
            #A_Mean += aclima(self.Modules[plant].Modules['Photosynt'].V('A'))
        #breakpoint()
        self.V_Set( 'H', t_w_hist)
        self.V_Set( 'NF', t_n_f)
        self.V_Set( 'h', t_w_k)
        self.V_Set( 'n', t_n_k)
        self.V_Set( 'm', t_m_k)
        self.V_Set( 'sum_A', sum_A)
        self.V_Set( 'A_Mean', A_Mean)

    def reset(self):
        pass
        #self.V_Set('<nombre>', valor) # -> cualquier variable que no sea constante