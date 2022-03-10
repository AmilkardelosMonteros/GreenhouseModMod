import numpy as np
import pandas as pd
import numpy as np
from time import time
import matplotlib.pyplot as plt
#from .climate.director import Climate_model
#from module_control import ModuleControl
#from director_production import I_2, Production_model
from auxModMod.Dir import Director
from sympy import symbols

n_f, n_p, MJ, g = symbols('n_f n_p MJ g') # number of fruits, number of plants



class Greenhouse(Director):
    def __init__(self):
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={})
        self.AddVar( typ='State', varid='H', prn=r'$H_k$', desc="Accumulated weight of all harvested fruits.", units= g, val=0.0)
        self.AddVar( typ='State', varid='NF', prn=r'$N_k$', desc="Accumulated  number of fruits harvested", units= n_f, val=0.0)
        self.AddVar( typ='State', varid='h', prn=r'$h_k$', desc="Weight of all harvested fruits.", units= g, val=0.0)
        self.AddVar( typ='State', varid='n', prn=r'$n_k$',\
                   desc="Total  number of fruits harvested", units= n_f, val=0.0)
        self.AddVar( typ='State', varid='m', prn=r'$m_k$',\
               desc="Simulation of the total  number of fruits harvested", units= n_f, val=0.0)

    def Scheduler(self, t1, sch):
        """Advance the modules to time t1. sch is a list of modules id's to run
           its Advance method to time t1.
           
           Advance is the same interface, either if single module or list of modules.
        """
        
        for mod in sch:
            if self.Modules[mod].Advance(t1) != 1:
                print("Director: Error in Advancing Module '%s' from time %f to time %f" % ( mod, self.t, t1))
        self.t = t1
        '''
        ### Update Total weight and total number of fruits
        t_w_hist = 0.0
        t_n_f = 0
        t_w_k = 0.0
        t_n_k = 0
        t_m_k = 0
        for plant in self.PlantList:
            t_w_hist += self.Modules[plant].Modules['Plant'].V('Q_h')
            t_n_f += self.Modules[plant].Modules['Plant'].n_fruits_h 
            t_w_k += self.Modules[plant].Modules['Plant'].V('h_k')
            t_n_k += self.Modules[plant].Modules['Plant'].V('n_k')
            t_m_k += self.Modules[plant].Modules['Plant'].V('m_k')
        self.V_Set( 'H', t_w_hist)
        self.V_Set( 'NF', t_n_f)
        self.V_Set( 'h', t_w_k)
        self.V_Set( 'n', t_n_k)
        self.V_Set( 'm', t_m_k)
        '''

    def Run(self, Dt, n, sch, save=None):
        return super().Run(Dt, n, sch, save)


    def reset(self):
        pass
        #self.V_Set('<nombre>', valor) # -> cualquier variable que no sea constante

    def step(self, action):
        pass

    def reward(self, state, action):
        pass