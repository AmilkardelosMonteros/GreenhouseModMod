from .parameters_env import PARAMS_ENV

PARAMS_UTILS = {'mu':0.0, 'theta': 0.00, 'max_sigma':0.01, 'min_sigma': 0.0, 'decay_period':int(PARAMS_ENV['TIME_MAX']*PARAMS_ENV['STEP']**-1)}
