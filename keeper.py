import numpy as np


class keeper:
    def __init__(self):
        self.actions = {}
        self.rewards = {}
        self.Qgas    = {}
        self.Qelec   = {}
        self.porc    = 0.1
        self.i       = 0 

    def add_actions(self,dir):
        dir_actions = {}
        for key in ['U' + str(i) for i in range(1,11)]:
            sample = dir.Modules['Climate'].Vars[key].GetRecord()
            sample = list(np.random.choice(sample, size = int(len(sample)*self.porc)))
            dir_actions[key] = sample
        self.actions[str(self.i)] = dir_actions


    def add(self,dir):
        self.add_actions(dir)
        self.i += 1
        
    
    def plot(self):
        breakpoint()
