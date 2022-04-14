STATE_VARIABLES = ['T1','T2','C1','V1']
INPUTS          = ['I2','I5','I8','I11']
VARS_OF_DIR     = STATE_VARIABLES + INPUTS

CONTROLS = {'U1':  False, # pantalla térmica
            'U2':  False, # Ventilador almoadilla
            'U3':  False, # Enfriamiento mecanico
            'U4':  False, # Calentador de aire  
            'U5':  False, #Sombreado externo (No hace nada por los parametros)
            'U6':  True,  # Respiraderos laterales
            'U7':  True, # Ventilación forzada
            'U8':  True, # Respiraderos del techo 
            'U9':  False, # Control sistema de niebla
            'U10': False, # Fuente externa de C02
            'U11': False, # Tuberia de calentamiento 
            }

PARAMS_DDPG = {'hidden_sizes': [64,64,64], 
                'actor_learning_rate': 1e-4, 
                'critic_learning_rate': 1e-3, 
                'gamma':0.98, 'tau':0.125, 
                'max_memory_size':int(1e5),
                'batch_size': 32,
                'vars':VARS_OF_DIR,
                'controls':CONTROLS}
