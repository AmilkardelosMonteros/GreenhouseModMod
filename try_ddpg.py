from ddpg.ddpg import DDPGagent as Agent
import numpy as np
from parameters.parameters_ddpg import PARAMS_DDPG

class env:
    def __init__(self):
        self.observation_space = np.zeros((10,10))
        self.action_space = np.zeros((10,10))

env1  = env()
agent = Agent(env1,PARAMS_DDPG)