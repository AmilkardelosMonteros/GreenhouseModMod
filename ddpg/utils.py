#from pickle import TRUE
import numpy as np
import gym
from collections import deque
import random
import matplotlib.pyplot as plt
from gym import spaces
import pandas as pd
from torch import zeros_like 

def new_clip(array):
    new_array = list()
    for x in array:
        while x > 1 or x < 0:
            if x<0:
                x = -x
            elif x>1:
                x = x-1
        new_array.append(x)
    return np.array(new_array)
# Ornstein-Ulhenbeck Process
# Taken from #https://github.com/vitchyr/rlkit/blob/master/rlkit/exploration_strategies/ou_strategy.py
class OUNoise(object):
    def __init__(self, parameters):
        self.mu           = parameters['mu']
        self.theta        = parameters['theta']
        self.sigma        = parameters['max_sigma']
        self.max_sigma    = parameters['max_sigma']
        self.max_sigma_init = parameters['max_sigma']
        self.min_sigma    = parameters['min_sigma']
        self.low          = parameters['low']
        self.high         = parameters['high']
        self.action_dim   = parameters['dim']
        self.episodes     = parameters['episodes']
        self.episode      = 0
        #breakpoint()
        self.decay_period   = parameters['decay_period']
        self.reset()
        self.on = True
        self.seed = 3000
        np.random.seed(self.seed)
        
    def reset(self):
        self.max_sigma = max([0,self.max_sigma - self.max_sigma_init/ self.episodes])
        self.sigma = self.max_sigma
        self.episode += 1
        self.t = 0
        self.state = np.ones(self.action_dim) * self.mu
        
    def evolve_state(self):
        x          = self.state
        dx         = self.theta * (self.mu - x) + self.sigma * np.random.randn(self.action_dim)
        self.state = x + dx # new_clip(x + dx)
        return self.state
    
    def get_action(self, action,test = False):
        ou_state   = self.evolve_state()
        self.sigma = self.max_sigma - (self.max_sigma - self.min_sigma) * min(1.0, self.t / self.decay_period)
        self.t    += 1
        if test:
            return action + ou_state
        else:
            if self.on:
                return np.clip(action + ou_state,0.0,1.0)
            else:
                return np.clip(action,0,1)

# https://github.com/openai/gym/blob/master/gym/core.py
class NormalizedEnv(gym.ActionWrapper):
    """ Wrap action """

    def __init__(self, env):
        super().__init__(env)

    def action(self, action):
        act_k = (self.action_space.high - self.action_space.low)/ 2.
        act_b = (self.action_space.high + self.action_space.low)/ 2.
        return act_k * action + act_b

    def reverse_action(self, action):
        act_k_inv = 2./(self.action_space.high - self.action_space.low)
        act_b = (self.action_space.high + self.action_space.low)/ 2.
        return act_k_inv * (action - act_b)
        

class Memory:
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)
    
    def push(self, state, action, reward, next_state, done):
        experience = (state, action, np.array([reward]), next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        state_batch = []
        action_batch = []
        reward_batch = []
        next_state_batch = []
        done_batch = []

        batch = random.sample(self.buffer, batch_size)

        for experience in batch:
            state, action, reward, next_state, done = experience
            state_batch.append(state)
            action_batch.append(action)
            reward_batch.append(reward)
            next_state_batch.append(next_state)
            done_batch.append(done)
        
        return state_batch, action_batch, reward_batch, next_state_batch, done_batch

    def __len__(self):
        return len(self.buffer)

def test_noise(noise,n):
    #breakpoint()
    '''
    Grafica n acciones
    '''
    A = list()
    for _ in range(n):
        A.append(noise.get_action(np.zeros_like(range(noise.action_dim)),test = True) )
    A = np.array(A)
    #A = A.reshape((noise.action_dim,n))
    A_df = pd.DataFrame(A,columns=['A'+ str(i) for i in range(noise.action_dim)])
    ax = A_df.plot(subplots=True, layout=(int(np.ceil(noise.action_dim/2)), 2), figsize=(10, 7),title = 'Ruido')
    A_flat = A.flatten()
    for a in ax.flatten():
        a.set_ylim([min(A_flat) - 0.1,  max(A_flat) + 0.1])
    plt.show()
    

def test_reset(noise):
    #breakpoint()
    '''
    Grafica sigma a lo largo de los episodios
    '''
    sigmas = list()
    for _ in range(noise.episodes + int(noise.episodes*0.1)):
        sigmas.append(noise.sigma)
        noise.reset()
    plt.plot(sigmas)
    plt.show()
    