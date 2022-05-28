STATE_VARIABLES = ['T1','T2','C1','V1']
INPUTS          = ['I2','I5','I8','I11']
CROP_VARIABLES  = ['h'] 
VARS_OF_DIR     = STATE_VARIABLES + INPUTS + CROP_VARIABLES

CONTROLS = {'U1':  False, # Pantalla térmica
            'U2':  False, # Ventilador almoadilla
            'U3':  True, # Enfriamiento mecanico
            'U4':  False, # Calentador de aire  
            'U5':  False, # Sombreado externo (No hace nada por los parametros)
            'U6':  False, # Respiraderos laterales
            'U7':  False, # Ventilación forzada
            'U8':  True, # Respiraderos del techo 
            'U9':  False, # Control sistema de niebla
            'U10': True, # Fuente externa de C02
            'U11': True, # Tuberia de calentamiento
            'U12': False  # Lamparas 
            }

PARAMS_DDPG = {'hidden_sizes': [64,64], 
                'actor_learning_rate': 1e-4, 
                'critic_learning_rate': 1e-3, 
                'gamma':0.98, 'tau':0.125, 
                'max_memory_size':int(1e5),
                'batch_size': 124,
                'vars':VARS_OF_DIR,
                'controls':CONTROLS
                }
