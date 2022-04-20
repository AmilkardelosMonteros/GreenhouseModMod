from ddpg.utils import OUNoise
from ddpg.utils import test_noise
from parameters.parameters_utils import PARAMS_UTILS

noise = OUNoise(PARAMS_UTILS)

if __name__ == '__main__':
    test_noise(PARAMS_UTILS,n=PARAMS_UTILS['decay_period'])