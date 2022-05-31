from ddpg.utils import OUNoise
from ddpg.utils import test_noise
from parameters.parameters_utils import PARAMS_UTILS

noise = OUNoise(PARAMS_UTILS)
n=PARAMS_UTILS['decay_period']
if __name__ == '__main__':
    N_TEST = 10
    for _ in range(N_TEST):
        test_noise(noise,n)
        noise.max_sigma -= noise.max_sigma/(n*0.5)
        noise.reset()
