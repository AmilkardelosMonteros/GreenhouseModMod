from ModMod import Module
from scipy.stats import norm
import numpy as np
from .functions import * 

class Module1(Module):
    def __init__(self, Dt=60, **kwargs):
        """Models one part of the process, uses the shared variables
           from Director.
           Dt=0.1, default Time steping of module
        """
        super().__init__(Dt)  # Time steping of module
        # Always, use the super class __init__, theare are several otjer initializations
        # Module specific constructors, add RHS's
        #self.i = 0
        #self.agent = agent
        #self.noise = noise
        #self.train = True   
        #self.foo = 0      
        for key, value in kwargs.items():
            self.AddStateRHS(key, value)
        # print("State Variables for this module:", self.S_RHS_ids)


    def Advance(self, t1):
        #state = self.get_state()
        #controls = self.get_controls(state) #Forward
        #action = list(controls.values())
        #breakpoint()
        #self.update_controls(controls)
        #self.V_Set('Qco2',0)
        #Vsat = V_sa( T = self.V('T2') ) # nuevo
        #V1 = self.V('V1') / 7  # nuevo 
        #RH = 100 * ( V1 / Vsat ) # nuevo 
        #self.V_Set('RH', RH) # nuevo   # definit RH como variable
        self.AdvanceRungeKutta(t1, Method=4)
        self.AdvanceAssigment(t1)
        #self.i  += 1
        #new_state = self.get_state()
        #done = self.is_done()
        #reward = self.get_reward(t1)
        #if self.train:
        #    self.agent.memory.push(state, action, reward, new_state, done)
        #    self.update() #Backpropagation
        return 1
