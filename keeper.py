import numpy as np
import matplotlib.pyplot as plt
from sympy import Q

def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('')

class keeper:
    def __init__(self):
        self.actions = {} 
        self.rewards = {} #reward acumulado al final del episodio
        self.Qgas    = {} #Gasto por gas al final del episodio 
        self.Qco2    = {}
        self.Qh2o    = {} 
        self.Qelec   = {} #Gasto por electricidad al final del episodio 
        self.G       = {} #Ganacia al final del episodio 
        self.porc    = 0.5
        self.i       = 0 

    def add_actions(self,dir):
        #try:
        dir_actions = {}
        for key in ['U' + str(i) for i in range(1,13)]:
            sample = dir.Modules['Climate'].Vars[key].GetRecord()
            sample = list(np.random.choice(sample, size = int(len(sample)*self.porc)))
            dir_actions[key] = sample
        self.actions[str(self.i)] = dir_actions
        return 1 
        #except:
        #    return 0 

    def add_costs(self,dir):
        #try:
        self.Qgas[str(self.i)]    = dir.Modules['Climate'].Vars['Qgas'].GetRecord()[-1]
        self.Qco2[str(self.i)]    = dir.Modules['Climate'].Vars['Qco2'].GetRecord()[-1]
        self.Qh2o[str(self.i)]    = dir.Modules['Climate'].Vars['Qh2o'].GetRecord()[-1]
        self.Qelec[str(self.i)]   = dir.Modules['Climate'].Vars['Qelec'].GetRecord()[-1]
        self.G[str(self.i)]       = 0.015341*dir.Vars['H'].GetRecord()[-1]
        self.rewards[str(self.i)] = sum(dir.Modules['Climate'].Vars['reward'].GetRecord())
        return 1
        #    return 1 
        #except:
        #    return 0

    def add(self,dir):
        if self.add_actions(dir) == 1 and self.add_costs(dir) == 1:
            self.i += 1
        else:
            print('Algo anda mal')
    
    def reset_noise(self,dir):
        dir.Modules['Climate'].Modules['ModuleClimate'].noise.reset()

    def plot_actions(self,actions):
        for a in actions:
            _, axis= plt.subplots(sharex=True, figsize=(10,5))
            new_data = list()
            for name in range(self.i):
                new_data.append(self.actions[str(name)][a])   
            axis.violinplot(new_data, showmeans=True)
            axis.set_title('Distribucion de ' + a)
            labels = [str(i) for i in self.actions.keys()]
            set_axis_style(axis, labels)
            plt.show()

    def plot_dir(self,dic,title):
        t = range(self.i)
        x = list(dic.values())
        plt.title(title)
        plt.xlabel('Episodios')
        plt.plot(t,x)
        plt.show()
        plt.close()

    def plot_cost(self):
        self.plot_dir(self.Qco2,'Costo del Co2')
        self.plot_dir(self.Qelec,'Costo de la electricidad')
        self.plot_dir(self.Qgas,'Costo del Gas')
        self.plot_dir(self.Qh2o,'Costo del agua')


    def plot_rewards(self):
        self.plot_dir(self.rewards,'Reward acumulado')
