from .parameters_env import PARAMS_ENV
from .parameters_ddpg import CONTROLS


PARAMS_UTILS = {'mu':0.0, 
                'theta': 0.00, 
                'max_sigma':0.005, 
                'min_sigma': 0.0, 
                'decay_period':PARAMS_ENV['n'],
                'low':-1,
                'high':1,
                'dim':len(CONTROLS.values())
                }

