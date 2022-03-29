STATE_VARIABLES = ['T1','T2','C1','V1']
INPUTS          = ['I2','I5','I8','I11']
VARS_OF_DIR     = STATE_VARIABLES + INPUTS

CONTROLS = {'U1':  True, 
            'U2':  True, 
            'U3':  True, 
            'U4':  False,   
            'U5':  False, #No hace nada por los parametros
            'U6':  False, 
            'U7':  True, 
            'U8':  True,  
            'U9':  True, 
            'U10': True,
            'U11': True, 
            }

PARAMS_DDPG = {'hidden_sizes': [64,64,64], 
                'actor_learning_rate': 1e-4, 
                'critic_learning_rate': 1e-3, 
                'gamma':0.98, 'tau':0.125, 
                'max_memory_size':int(1e5),
                'vars':VARS_OF_DIR,
                'controls':CONTROLS}
