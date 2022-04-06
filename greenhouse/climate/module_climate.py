from auxModMod.Dir import Module
from scipy.stats import norm
import numpy as np
from .functions import * 

class Module1(Module):
    def __init__(self, agent,noise, Dt=1, **kwargs):
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
        for key, value in kwargs.items():
            self.AddStateRHS(key, value)
        # print("State Variables for this module:", self.S_RHS_ids)

    def get_controls(self,state):
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
        return controls,action
    
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

    def get_reward(self):
        return 0
    
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
        controls,action = self.get_controls(state) #Forward
        self.update_controls(controls)
        #self.V_Set('Qco2',0)
        self.AdvanceRungeKutta(t1)
        self.AdvanceAssigment(t1)
        self.i  += 1
        new_state = self.get_state()
        done = self.is_done()
        reward = self.get_reward()
        self.agent.memory.push(state, action, reward, new_state, done)
        #self.update() #Backpropagation
        return 1