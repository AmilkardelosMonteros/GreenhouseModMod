import numpy as np
import pathlib
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
try:
    import chime
except:
    print('Si no estas en el servidor instala chime')
from .crop.functions import V_sa,VPD
from .borrame import create_images_per_module
n_f, n_p, MJ, g = symbols('n_f n_p MJ g') # number of fruits, number of plants

s, mol_CO2, mol_air, mol_phot, m, d, C, g, mol_O2, pa, ppm = symbols('s mol_CO2 mol_air mol_phot m d C g mol_O2 pa ppm')
from .crop.params_dias_tem import DIAS
nrec  = DIAS*24*60
class Greenhouse(Director):
    def __init__(self, agent, noise):
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={})
        self.Dt = None
        self.n = None
        self.i = 0
        self.agent    = agent
        self.noise    = noise
        self.train    = True
        self.sound = 0
        self.type = 'net'
        #self.control = 0
        self.AddVar( typ='State', varid='H', prn=r'$H_k$', desc="Accumulated weight of all harvested fruits.", units= g, val=0.0,rec = nrec)
        self.AddVar( typ='State', varid='NF', prn=r'$N_k$', desc="Accumulated  number of fruits harvested", units= n_f, val=0.0,rec = nrec)
        self.AddVar( typ='State', varid='h', prn=r'$h_k$', desc="Weight of all harvested fruits.", units= g, val=0.0,rec = nrec)
        self.AddVar( typ='State', varid='n', prn=r'$n_k$', desc="Total  number of fruits harvested", units= n_f, val=0.0,rec=nrec)
        self.AddVar( typ='State', varid='m', prn=r'$m_k$', desc="Simulation of the total  number of fruits harvested", units= n_f, val=0.0,rec=nrec)
        self.AddVar( typ='State', varid='A_Mean', prn=r'$E[A]$',desc="Total mean assimilation rate", units= g * (m**-2), val=0,rec=nrec) ##Revisar

    def get_controls_net(self, state):
        #No hace nada si noise.on = False
        if np.isnan(state).any() or np.isinf(state).any():
            print('La red esta recibiendo mal el estado:')
            print(state)
        action   = self.agent.get_action(state)
        action   = self.noise.get_action(action)
        j        = 0
        controls = {}
        CONTROLS = list()
        for k,v in self.agent.controls.items():
            if v == True:
                CONTROLS.append(k) #Encuentro los que si quiero usar
            controls[k] = v
        for k,v in self.agent.controls.items():
            if k in CONTROLS:
                controls[k] = action[j]
                j+= 1
            elif v == False:
                controls[k] = 0
        return controls,action

    def get_controls_browniano(self,state):
        #No hace nada si noise.on = False
        self.noise.on = True
        self.noise.max_sigma = self.noise.max_sigma_init
        action   = self.agent.get_action(state)
        action   = 0.5 + np.zeros_like(action) 
        action   = self.noise.get_action(action) 
        j        = 0
        controls = {}
        CONTROLS = list()
        
        for k,v in self.agent.controls.items():
            if v == True:
                CONTROLS.append(k) #Encuentro los que si quiero usar
            controls[k] = v
        for k,v in self.agent.controls.items():
            if k in CONTROLS:
                controls[k] = action[j]
                j+= 1
            elif v == False:
                controls[k] = 0
        return controls,action

    def get_controls_uniform(self,state):
        action   = self.agent.get_action(state)
        action   = np.zeros_like(action) 
        action   = action + np.random.uniform(0,1,len(action))
        j        = 0
        controls = {}
        CONTROLS = list()
        for k,v in self.agent.controls.items():
            if v == True:
                CONTROLS.append(k) #Encuentro los que si quiero usar
            controls[k] = v
        for k,v in self.agent.controls.items():
            if k in CONTROLS:
                controls[k] = action[j]
                j+= 1
            elif v == False:
                controls[k] = 0
        return controls,action
        
    def heat_pid(self,goal=20):
        '''Controller PID for temperature T1'''
        KP11 = 3.672*0.03125
        KI11 = 188.659*0.03125
        KD11 = 0.00
        T1_rec = self.Modules['Climate'].Vars['T2'].GetRecord()
        P =  goal- T1_rec[-1]
        I = self.Modules['Climate'].Vars['T1'].Integral(ni=-6,g = lambda x: goal-x)
        D = (goal-T1_rec[-1]) - (goal-T1_rec[-2])
        U = KP11*P + KI11*I + KD11*D
        return np.clip(U,0,100)*0.01

    def CO2_pid(self,goal=600):
        '''Controller PID of CO2'''
        K_cu = 0
        P_u = 0#155minutos en segundos9300 
        K_c = 0.5
        tau_i = 0.5
        tau_d = 0
        T1_rec = self.Modules['Climate'].Vars['C1'].GetRecord()
        P =  goal- T1_rec[-1]
        I = self.Modules['Climate'].Vars['C1'].Integral(ni=-6,g = lambda x: goal-x)
        D = (goal-T1_rec[-1]) - (goal-T1_rec[-2])
        U =  K_c*(P + tau_i*I + tau_d*D)
        return np.clip(U,0,100)*0.01
    
    def fog_pid(self):
        '''Controller PID of the fogging system'''
        KP10 = 0.019
        KI10 = 6033.599
        KD10 = 65.103
        goal = 600
        T1_rec = self.Modules['Climate'].Vars['C1'].GetRecord()
        P =  goal- T1_rec[-1]
        I = self.Modules['Climate'].Vars['C1'].Integral(ni=-6,g = lambda x: goal-x)
        D = (goal-T1_rec[-1]) - (goal-T1_rec[-2])
        U = KP10*P + KI10*I + KD10*D
        return np.clip(U,0,100)*0.01

    def expert_control(self,state):
        action   = self.agent.get_action(state)
        action   = np.zeros_like(action) 
        controls = {}
        Iglob = self.V('I2') 
        for k,_ in self.agent.controls.items():
            controls[k] = 0.0

        if Iglob < 5:
            heat_set = 16
            vent_set = 26
            vpd_set  = 1.05

        else:
            heat_set = 26
            vent_set = 26
            vpd_set  = 1.13

        if Iglob < 700:
            controls['U12'] = 1.0
        
        else:
            controls['U12'] = 0.0
            
        if Iglob > 5 or controls['U12'] > 0:
            CO2_set = 1000

        else:
            CO2_set = 650

        if Iglob > 5 and Iglob < 100 and self.V('I5') < 12:
            controls['U1'] = 0.3
        
        elif Iglob < 5:
            controls['U1'] = 1.0

        else:
            controls['U1'] = 0.0 

        controls['U11'] = self.heat_pid(heat_set)
        controls['U10'] = self.CO2_pid(CO2_set)
        return controls,action
    
    def get_controls(self,state):
        if self.type == 'net':
            return self.get_controls_net(state)
        elif self.type == 'bwn':
            return self.get_controls_browniano(state)
        elif self.type == 'unif':
            return self.get_controls_uniform(state)
        elif self.type == 'expert':
            return self.expert_control(state)
        else:
            print('No conozco ese controlador')
        


    def get_vars(self):
        '''
        Sirve para obtener todas las variables y las guarda en un diccionario
        '''
        return {id:Obj.val for id,Obj in self.Vars.items()}

    
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
        ####Estan desactivados los costos!!!!!!
        reward_ =  G  - (deltaQco2 + deltaQgas + deltaQh2o + deltaQelec)
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
            #print('Actulizando redes ...')

    def check_controls(self):
        from termcolor import colored
        booleans = list()
        for i in range(1,13):
            tem = self.Vars['U'+str(i)].GetRecord()
            test1 = tem >= 0
            test2 = tem <= 1
            test3 = np.logical_and(test1,test2)
            booleans.append(test3.all())
        answer = 'Si' if sum(booleans) == 12 else 'No'
        print(colored('Acciones en [0,1]? ' + answer,'red'))
        #breakpoint()

    def Scheduler(self, t1, sch):
        """Advance the modules to time t1. sch is a list of modules id's to run
           its Advance method to time t1.
           
           Advance is the same interface, either if single module or list of modules.
        """
        V_sa1 = V_sa( T = self.V('T1'))
        VPD1  = VPD( V_sa=V_sa1, RH = self.V('RH'))
        self.V_Set('VPD',VPD1)
        state = self.get_state()
        if np.isnan(state).any() or abs(self.V('T1')) > 200:
            self.sound += 1
            # self.check_controls()
            if self.sound == 1:
                print('Algo se fue a Nan')
                self.check_controls()
                chime.error() 
                create_images_per_module(self, 'Climate', PATH='errores') 
                exit()
                # raise SystemExit('Revisa tus flujos algo fue Nan, Adios')
        controls,action = self.get_controls(state) #Forward
        
        #controls = self.expert_control()
        #controls es un diccionario que se necesita internamente (director), accion es lo que necesita la red 
        self.update_controls(controls)
        #breakpoint()
        #if t1%86400 == 0:
        #    controles = np.random.randint(1,12,2)
        #    controles = [1,6]
        #    print(controles)
        #    for control in range(1,13):
        #        self.V_Set('U'+str(control),1) 
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
        aclima = lambda x: Aclima(A = x, I1 = self.V('I1'))
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
                    print('Algo mal con Aclima')
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
            if self.sound < 1:
                self.agent.memory.push(state, action, reward, new_state, done)
                self.update()
            elif self.sound == 1:
                data = {}
                for key, val in self.Vars.items():
                    rec = val.GetRecord()
                    if len(rec) == len(self.Vars['T1'].GetRecord()):
                        data[key] = rec
                pathlib.Path('errors/').mkdir(parents=True, exist_ok=True)
                data = pd.DataFrame.from_dict(data)
                data.to_csv('errors/variables.csv')

                pathlib.Path('errors/').mkdir(parents=True, exist_ok=True)
                pd.DataFrame(data).to_csv('errors/variables.csv')
        
    def Reset(self):
        super().Reset()
        self.t = 0
        self.sound = 0 
        RHSs_ids = self.Modules['Climate'].Modules['ModuleMeteo'].Assigm_S_RHS_ids
        self.Modules['Climate'].Modules['ModuleMeteo'].input_vars['time_index'] = [0]*len(RHSs_ids)
    
#    def reset(self):
#        self.Reset()
#        for var in self.Vars.values():
#            if var.typ == 'State':
#                self.V_Set(var.varid, var.init_val) # -> cualquier variable que no sea constante
