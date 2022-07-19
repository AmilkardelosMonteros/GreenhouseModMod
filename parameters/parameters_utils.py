from .parameters_env import PARAMS_ENV,PARAMS_TRAIN
from .parameters_ddpg import CONTROLS

def num_actions_(controls):
    s = 0
    for _,v in controls.items():
        if v == True:s+=1
    return s

PARAMS_UTILS = {'mu':0., 
                'theta': 0.00, 
                'max_sigma':0.09, 
                'min_sigma':0.009,
                'decay_period':PARAMS_ENV['n'],
                'episodes': PARAMS_TRAIN['EPISODES'],
                'low':-1,
                'high':1,
                'dim':num_actions_(CONTROLS)
                }

