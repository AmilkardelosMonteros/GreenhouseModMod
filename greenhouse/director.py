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

nrec  = 90*24*60
class Greenhouse(Director):
    def __init__(self, agent, noise):
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={})
        self.Dt = None
        self.n = None
        self.i = 0
        self.agent = agent
        self.noise = noise
        self.train = True
        self.AddVar( typ='State', varid='H', prn=r'$H_k$', desc="Accumulated weight of all harvested fruits.", units= g, val=0.0,rec = nrec)
        self.AddVar( typ='State', varid='NF', prn=r'$N_k$', desc="Accumulated  number of fruits harvested", units= n_f, val=0.0,rec = nrec)
        self.AddVar( typ='State', varid='h', prn=r'$h_k$', desc="Weight of all harvested fruits.", units= g, val=0.0,rec = nrec)
        self.AddVar( typ='State', varid='n', prn=r'$n_k$', desc="Total  number of fruits harvested", units= n_f, val=0.0,rec=nrec)
        self.AddVar( typ='State', varid='m', prn=r'$m_k$', desc="Simulation of the total  number of fruits harvested", units= n_f, val=0.0,rec=nrec)
        self.AddVar( typ='State', varid='A_Mean', prn=r'$E[A]$',desc="Total mean assimilation rate", units= g * (m**-2), val=0,rec=nrec) ##Revisar

    def get_controls(self, state):
        action   = self.agent.get_action(state)
        action   = self.noise.get_action(action) #No hace nada si noise.on = False
        j        = 0
        controls = {}
        for k,v in self.agent.controls.items():
            if v == False:
                controls[k] = 0
            else:
                controls[k] = action[j]
                j+= 1
        return controls

    def get_vars(self):
        '''
        Sirve para obtener todas las variables y las guarda en un diccionario
        '''
        Vars = {id:Obj.val for id,Obj in self.Vars.items()}
        return Vars

    
    def update_controls(self,controls):
        '''
        Actualiza los controles.
        controls = {'U1': u1, etc}
        '''
        for k,v in controls.items():
            self.V_Set(k, v) #Set en variables de director

    def get_state(self):
        '''
        Obtiene un estado parcial para el agente
        '''
        Vars = self.get_vars()
        partial_vars = {id:Vars[id] for id in self.agent.vars}
        state = np.array(list(partial_vars.values()))
        return state

    def G(self,H):
        '''
        Precio del pepino 
        H esta en gramos
        '''
        return 0.015341*H

    def get_reward(self,t1):
        index_back = int(self.Dt/self.Modules['Climate'].Modules['ModuleClimate'].Dt) #if self.D.master_dir.Dt/self.Dt > 1 else 2 
        Qco2       = self.Vars['Qco2'].GetRecord()
        Qgas       = self.Vars['Qgas'].GetRecord() 
        Qh2o       = self.Vars['Qh2o'].GetRecord()
        Qlec       = self.Vars['Qelec'].GetRecord()
        deltaQco2  = Qco2[-1] - Qco2[-index_back-1] 
        deltaQgas  = Qgas[-1] - Qgas[-index_back-1]  
        deltaQh2o  = Qh2o[-1] - Qh2o[-index_back-1] 
        deltaQelec = Qlec[-1] - Qlec[-index_back-1] 
        G = 0.0
        H_ = self.Vars['H'].GetRecord()
        h_ = self.Vars['h'].GetRecord()
        G += self.G(h_[-1])
        #if t1 % 86400 == 0:
        #    H_     = self.D.master_dir.Vars['H'].GetRecord()
        #    #deltaH = H_[-1] - H_[-1439]
        #    h_     = self.D.master_dir.Vars['h'].GetRecord()
        #    self.foo +=  h_[-1]
        #    G      = self.G(h_[-1]) # self.G(deltaH) #Ganancia
        #    if h_[-1] > 0:
        #        breakpoint()
        reward_ =  G - (deltaQco2 + deltaQgas + deltaQh2o + deltaQelec)
        self.V_Set('reward',reward_) 
        #if abs(var - self.D.master_dir.Vars['reward'].GetRecord().sum()) > 1e-1:
        #    print(abs(var - self.D.master_dir.Vars['reward'].GetRecord().sum()))
        #if reward_ > 0 :
        #    print(reward_)
        return reward_
    
    def is_done(self):
        if self.i == self.noise.decay_period: 
            return True
        else:
            return False

    def update(self):
        if len(self.agent.memory) >= self.agent.batch_size:
            self.agent.update(self.agent.batch_size)
            #print('Actulizando redes ...')e

    def Scheduler(self, t1, sch):
        """Advance the modules to time t1. sch is a list of modules id's to run
           its Advance method to time t1.
           
           Advance is the same interface, either if single module or list of modules.
        """
        state = self.get_state()
        controls = self.get_controls(state) #Forward
        action = list(controls.values())
        if self.train == False:pass
            #breakpoint()
        self.update_controls(controls)
        for mod in sch:
            if self.Modules[mod].Advance(t1) != 1:
                print("Director: Error in Advancing Module '%s' from time %f to time %f" % ( mod, self.t, t1))
        self.t = t1
        self.i  += 1
        ### Update Total weight and total number of fruits
        t_w_hist = 0.0
        t_n_f = 0
        t_w_k = 0.0
        t_n_k = 0
        t_m_k = 0
        A_Mean = 0
        A_Mean1 = 0
        A_int  = 0
        aclima = lambda x: Aclima(x, self.V('I1'))
        #breakpoint()
        for plant in self.PlantList:
            t_w_hist += self.Modules[plant].Modules['Plant'].V('Q_h')
            t_n_f += self.Modules[plant].Modules['Plant'].n_fruits_h 
            t_w_k += self.Modules[plant].Modules['Plant'].V('h_k')
            t_n_k += self.Modules[plant].Modules['Plant'].V('n_k')
            t_m_k += self.Modules[plant].Modules['Plant'].V('m_k')
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
        self.V_Set( 'h', t_w_k if t1 % 86400 == 0 else 0.0)
        self.V_Set( 'n', t_n_k if t1 % 86400 == 0 else 0.0)
        self.V_Set( 'm', t_m_k)
        self.V_Set( 'A_Mean', A_Mean)

        new_state = self.get_state()
        done = self.is_done()
        reward = self.get_reward(t1)

        if self.train:
            self.agent.memory.push(state, action, reward, new_state, done)
            self.update()
        

    def reset(self):
        for var in self.Vars.values():
            if var.typ == 'State':
                self.V_Set(var.varid, var.init_val) # -> cualquier variable que no sea constante
