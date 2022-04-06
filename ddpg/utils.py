from pickle import TRUE
import numpy as np
import gym
from collections import deque
import random
import matplotlib.pyplot as plt
from gym import spaces
import pandas as pd 
# Ornstein-Ulhenbeck Process
# Taken from #https://github.com/vitchyr/rlkit/blob/master/rlkit/exploration_strategies/ou_strategy.py
class OUNoise(object):
    def __init__(self, parameters):
        self.mu           = parameters['mu']
        self.theta        = parameters['theta']
        self.sigma        = parameters['max_sigma']
        self.max_sigma    = parameters['max_sigma']
        self.min_sigma    = parameters['min_sigma']
        self.low          = parameters['low']
        self.high         = parameters['high']
        self.action_dim   = parameters['dim']
        self.decay_period   = parameters['decay_period']
        self.reset()
        self.on = True
        
    def reset(self):
        self.t = 0
        self.state = np.ones(self.action_dim) * self.mu
        
    def evolve_state(self):
        x  = self.state
        dx = self.theta * (self.mu - x) + self.sigma * np.random.randn(self.action_dim)
        self.state = np.clip(x + dx,self.low, self.high)
        self.state = x + dx
        return self.state
    
    def get_action(self, action):
        if self.on == True:
            ou_state = self.evolve_state()
            self.sigma = self.max_sigma - (self.max_sigma - self.min_sigma) * min(1.0, self.t / self.decay_period)
            self.t += 1
            return np.clip(action + ou_state, self.low, self.high)
        else:
            return action


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

def test_noise(dim):
    n = PARAMS_UTILS['decay_period']
    LOW_ACTION = np.zeros(dim)
    HIGH_ACTION = np.ones(dim)
    action_space = spaces.Box(low=LOW_ACTION, high=HIGH_ACTION)
    '''
    Grafica n acciones
    '''
    noise = OUNoise(action_space)
    A = list()
    for _ in range(n):
        A.append(noise.get_action(0*np.ones(dim)))
    A = np.array(A)
    A.reshape((action_space.shape[0],n))
    A = pd.DataFrame(A,columns=['A'+ str(i) for i in range(action_space.shape[0])])
    ax = A.plot(subplots=True, layout=(int(np.ceil(action_space.shape[0]/2)), 2), figsize=(10, 7),title = 'Ruido') 
    plt.show()
    