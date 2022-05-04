from ModMod import Module
from scipy.stats import norm
import numpy as np
from .functions import * 

class Module1(Module):
    def __init__(self, agent,noise, Dt=60, **kwargs):
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt)  # Time steping of module
        # Always, use the super class __init__, theare are several otjer initializations
        # Module specific constructors, add RHS's
        self.i = 0
        self.agent = agent
        self.noise = noise
        self.train = True   
        self.foo = 0      
        for key, value in kwargs.items():
            self.AddStateRHS(key, value)
        # print("State Variables for this module:", self.S_RHS_ids)

    def get_controls(self,state):
        #breakpoint()
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
        #breakpoint()
        return controls
    
    def get_vars(self):
        '''
        Sirve para obtener todas las variables y las guarda en un diccionario
        '''
        Vars = {id:Obj.val for id,Obj in self.D.Vars.items()}
        return Vars

    def update_controls(self,controls):
        '''
        Actualiza los controles.
        controls = {'U1': u1, etc}
        '''
        for k,v in controls.items():
            self.V_Set(k,v) #Set en variables de director

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
        index_back = int(self.D.master_dir.Dt/self.Dt) #if self.D.master_dir.Dt/self.Dt > 1 else 2 
        Qco2       = self.D.Vars['Qco2'].GetRecord()
        Qgas       = self.D.Vars['Qgas'].GetRecord() 
        Qh2o       = self.D.Vars['Qh2o'].GetRecord()
        Qlec       = self.D.Vars['Qelec'].GetRecord()
        deltaQco2  = Qco2[-1] - Qco2[-index_back-1] 
        deltaQgas  = Qgas[-1] - Qgas[-index_back-1]  
        deltaQh2o  = Qh2o[-1] - Qh2o[-index_back-1] 
        deltaQelec = Qlec[-1] - Qlec[-index_back-1] 
        G = 0.0
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
        if reward_ > 0 :
            print(reward_)
        return reward_
    
    def is_done(self):
        if self.i == self.noise.decay_period: 
            return True
        else:
            return False

    def update(self):
        if len(self.agent.memory) >= self.agent.batch_size:
            self.agent.update(self.agent.batch_size)
            #print('Actulizando redes ...')

    
    def Advance(self, t1):
        state = self.get_state()
        controls = self.get_controls(state) #Forward
        action = list(controls.values())
        #breakpoint()
        self.update_controls(controls)
        #self.V_Set('Qco2',0)
        #Vsat = V_sa( T = self.V('T2') ) # nuevo
        #V1 = self.V('V1') / 7  # nuevo 
        #RH = 100 * ( V1 / Vsat ) # nuevo 
        #self.V_Set('RH', RH) # nuevo   # definit RH como variable
        self.AdvanceRungeKutta(t1)
        self.AdvanceAssigment(t1)
        self.i  += 1
        new_state = self.get_state()
        done = self.is_done()
        reward = self.get_reward(t1)
        if self.train:
            self.agent.memory.push(state, action, reward, new_state, done)
            self.update() #Backpropagation
        return 1