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

<<<<<<< HEAD
    def Advance(self, t1):
        print('Advance {}!!'.format(t1))
        #I9 = I2 pero hay flujos que solo dependen de I9 (q7)
        self.V_Set('I9', self.V('I2'))

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
=======
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
>>>>>>> 4a96b8a0892d24c8b6faf70a0faac9ad27d82486

    def update_controls(self,controls):
        '''
        Actualiza los controles.
        controls = {'U1': u1, etc}
        '''
        for k,v in controls.items():
            self.V_Set(k,v) #Set en variables de director

<<<<<<< HEAD
        # RHS qGas
        h_6 = h6(U4=self.V('U4'), lamb4=self.V('lamb4'), alpha6=self.V('alpha6')) #H blow air 
        a_1 = a1(I1=self.V('I1'), beta3=self.V('beta3')) #auxiliar para g1
        g_1 = g1(a1=a_1)                                   #auxiliar para r6
        #r_6 = r6(T1=self.V('T1'), I3=self.V('I3'), alpha3=self.V('alpha3'), epsil1=self.V('epsil1'), epsil2=self.V('epsil2'), lamb=self.V('sigma'), g1=g_1)
        #print('Advance! {}'.format(r_6))
        h_4 = h4(T2=self.V('T2'), I3=self.V('I3'),gamma1=self.V('gamma1'), phi1=self.V('phi1'))
=======
    def get_state(self):
        '''
        Obtiene un estado parcial para el agente
        '''
        Vars = self.get_vars()
        partial_vars = {id:Vars[id] for id in self.agent.vars}
        state = np.array(list(partial_vars.values()))
        return state
>>>>>>> 4a96b8a0892d24c8b6faf70a0faac9ad27d82486

    def get_reward(self):
        return 0
    
    def is_done(self):
        if self.i == self.noise.decay_period: 
            return True
        else:
            return False

<<<<<<< HEAD
        # variables for RHSs qGas
        self.V_Set('h6', h_6)
        #self.V_Set('r6', r_6)
        
        #T1r = self.V('T1') 
        #T2r = self.V('T2') 
        #V1r = self.V('V1') 
        #C1r = self.V('C1') 
        #print('Estas pasando por Advance')
        # Actualización de las variables
        #self.V_Set('T1', T1r)
        #self.V_Set('T2', T2r)
        #self.V_Set('V1', V1r)
        #self.V_Set('C1', C1r)
        # Avance del RHS
=======
    def update(self):
        if len(self.agent.memory) >= self.agent.batch_size:
            self.agent.update(self.agent.batch_size)
            #print('Actulizando redes ...')

    
    def Advance(self, t1):
        state = self.get_state()
        controls,action = self.get_controls(state) #Forward
        self.update_controls(controls)
        #self.V_Set('Qco2',0)
>>>>>>> 4a96b8a0892d24c8b6faf70a0faac9ad27d82486
        self.AdvanceRungeKutta(t1)
        self.AdvanceAssigment(t1)
        self.i  += 1
        new_state = self.get_state()
        done = self.is_done()
        reward = self.get_reward()
        self.agent.memory.push(state, action, reward, new_state, done)
        #self.update() #Backpropagation
        return 1