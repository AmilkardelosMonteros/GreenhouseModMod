from ddpg.utils import OUNoise
from ddpg.utils import test_noise,test_reset
from parameters.parameters_utils import PARAMS_UTILS

noise  = OUNoise(PARAMS_UTILS)
noise2 = OUNoise(PARAMS_UTILS)
n=PARAMS_UTILS['decay_period']
if __name__ == '__main__':
    N_TEST = 5
    print('Test sobre el reset')
    test_reset(noise)
    for _ in range(N_TEST):
        test_noise(noise2,n)
        noise2.reset()
        print(noise2.sigma)

