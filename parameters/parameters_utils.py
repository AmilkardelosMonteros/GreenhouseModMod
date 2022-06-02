from .parameters_env import PARAMS_ENV,PARAMS_TRAIN
from .parameters_ddpg import CONTROLS



PARAMS_UTILS = {'mu':0.0, 
                'theta': 0.00, 
                'max_sigma':0.005, 
                'min_sigma':0,
                'decay_period':PARAMS_ENV['n'],
                'episodes': PARAMS_TRAIN['EPISODES'],
                'low':-1,
                'high':1,
                'dim':len(CONTROLS.values())
                }

