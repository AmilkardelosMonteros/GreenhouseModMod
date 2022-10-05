import numpy as np
import matplotlib.pyplot as plt
from sympy import Q
import json
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
        self.H       = {}
        self.NF      = {}
        self.Qgas    = {} #Gasto por gas al final del episodio
        self.Qco2    = {}
        self.Qh2o    = {}
        self.Qelec   = {} #Gasto por electricidad al final del episodio
        self.G       = {} #Ganacia al final del episodio
        self.state   = {} #Estado promedio
        self.porc    = 0.01
        self.VARS = ['T1','T2','C1','V1','I2','I5','I8','I11']
        self.i       = 0

    def add_actions(self,dir):
        #try:
        dir_actions = {}
        for key in ['U' + str(i) for i in range(1,13)]:
            sample = dir.Modules['Climate'].Vars[key].GetRecord()
            sample = sample[-dir.n:] #Para evitar sesgar hacia el cero
            max_ = max(sample)
            min_ = min(sample)
            sample = list(np.random.choice(sample, size = int(len(sample)*self.porc)))
            sample.append(max_)
            sample.append(min_)
            dir_actions[key] = sample
        self.actions[str(self.i)] = dir_actions
        return 1
        #except:
        #    return 0

    def add_costs(self,dir):
        self.Qgas[str(self.i)]    = dir.Modules['Climate'].Vars['Qgas'].GetRecord()[-1]
        self.Qco2[str(self.i)]    = dir.Modules['Climate'].Vars['Qco2'].GetRecord()[-1]
        self.Qh2o[str(self.i)]    = dir.Modules['Climate'].Vars['Qh2o'].GetRecord()[-1]
        self.Qelec[str(self.i)]   = dir.Modules['Climate'].Vars['Qelec'].GetRecord()[-1]
        self.G[str(self.i)]       = 0.015341*dir.Vars['H'].GetRecord()[-1]
        self.rewards[str(self.i)] = sum(dir.Modules['Climate'].Vars['reward'].GetRecord())

    def add_reward(self,dir):
        H_                        = dir.Vars['H'].GetRecord()[-1]
        self.H[str(self.i)]       = H_
        self.G[str(self.i)]       = 0.015341*H_
        self.NF[str(self.i)]      = dir.Vars['NF'].GetRecord()[-1]
        self.rewards[str(self.i)] = sum(dir.Vars['reward'].GetRecord())

    def add(self,dir):
        if self.i%1 == 0: ###Las acciones solo se guardan cada 50 eps
            self.add_actions(dir)
        self.add_costs(dir)
        self.add_reward(dir)
        self.add_state(dir)
        self.i += 1

    def add_state(self,dir):
        state_dic = {}
        for v in self.VARS:
            state_dic[v] = dir.Vars[v].GetRecord().mean()
        self.state[str(self.i)] = state_dic
        



    def plot_actions(self,actions,flag='train',PATH=None):
        for a in actions:
            _, axis= plt.subplots(sharex=True, figsize=(10,5))
            new_data = list()
            names = self.actions.keys()
            for name in names:
                new_data.append(self.actions[name][a])
            axis.violinplot(new_data, showmeans=True)
            axis.set_title('Distribucion de ' + a + ' en ' + flag)
            labels = [str(i) for i in self.actions.keys()]
            set_axis_style(axis, labels)
            if PATH != None:
                plt.savefig(PATH + '/output/' + a + flag)
                plt.cla()
                plt.clf()
                plt.close('all')
            else:
                plt.show()
                plt.cla()
                plt.clf()
                plt.close('all')

    def plot_dir(self,dic,title,PATH=None):
        plt.cla()
        plt.clf()
        t = range(self.i)
        x = list(dic.values())
        plt.title(title)
        plt.xlabel('Episodios')
        plt.plot(t,x)
        if PATH != None:
            plt.savefig(PATH + '/output/' + title.replace(' ','_') + '.png')
            plt.close('all')
        else:
            plt.show()
            plt.close('all')

    def plot_cost(self,flag = 'train', PATH = None):
        self.plot_dir(self.Qco2,'Costo del Co2 ' + flag ,PATH)
        self.plot_dir(self.Qelec,'Costo de la electricidad ' + flag,PATH)
        self.plot_dir(self.Qgas,'Costo del Gas ' + flag,PATH)
        self.plot_dir(self.Qh2o,'Costo del agua ' + flag,PATH)


    def plot_rewards(self,flag = 'train',PATH = None):
        self.plot_dir(self.rewards,'Reward acumulado ' + flag,PATH)


    def plot_violin(self,dic,titulo,PATH):
        t = lambda x: np.array(list(x.values()))
        x = t(dic)
        _, axis= plt.subplots(sharex=True, figsize=(10,5))
        axis.violinplot(x, showmeans=True)
        axis.set_title('Distribucion de ' + titulo)
        if PATH != None:
            plt.savefig(PATH + '/output/' + titulo.replace(' ','_') + '.png')
            plt.cla()
            plt.clf()
            plt.close('all')
        else:
            plt.show()
            plt.cla()
            plt.clf()
            plt.close('all')


    def plot_gains(self, flag = 'train', PATH = None):
        self.plot_violin(self.rewards,'Reward Acumulado ' + flag ,PATH)
        self.plot_violin(self.NF,'Numero de frutos ' + flag,PATH)
        self.plot_violin(self.H,'Peso de los frutos ' + flag ,PATH)


    def save_(self,path,dic,name):
        with open(path + '/output/' +name + '.json', 'w') as outfile:
            json.dump(dic, outfile,indent = 4)

    def stress_test(self,path):
        t = lambda x: np.array(list(x.values()))
        Qgas = t(self.Qgas)
        Qco2 = t(self.Qco2)
        Qh2o = t(self.Qh2o)
        Qelec = t(self.Qelec)
        G = t(self.G)
        rewards = t(self.rewards)
        #breakpoint()
        test = (G - (Qgas + Qco2 + Qh2o + Qelec))  - rewards
        self.test = {}
        for i in range(self.i):
            self.test[str(i)] = test[i]
        self.save_(path, self.test,'test')


    def save(self, path, flag = 'train'):
        self.stress_test(path)
        self.save_(path, self.rewards,'rewards_' + flag)
        self.save_(path, self.Qco2,'Qco2_'+ flag)
        self.save_(path, self.Qelec,'Qele_'+ flag)
        self.save_(path, self.Qgas,'Qgas_'+ flag)
        self.save_(path, self.Qh2o,'Qh2o_'+ flag)
        self.save_(path, self.actions,'actions_'+ flag)
        self.save_(path, self.NF,'NF_'+ flag)
        self.save_(path, self.H,'H_'+ flag)
        self.save_(path, self.G,'G_'+ flag)
        self.save_(path, self.state,'states_'+ flag)


