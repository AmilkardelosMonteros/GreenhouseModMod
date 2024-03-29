STATE_VARIABLES = ['T1','T2','T3','C1','V1']
INPUTS          = ['I2','I5','I8','I11']
CROP_VARIABLES  = ['h'] 
VARS_OF_DIR     = STATE_VARIABLES + INPUTS + CROP_VARIABLES

CONTROLS = {'U1':   True, # Pantalla térmica
            'U2':   False, # Ventilador almoadilla
            'U3':   False, # Enfriamiento mecanico
            'U4':   True, # Calentador de aire  
            'U5':   False, # Sombreado externo (No hace nada por los parametros)
            'U6_c': True, # Respiraderos laterales
            'U7_c': False, # Ventilación forzada #Cambiamos U7 por U7_c para que U7 pudiera ser la solucion de un EDO
            'U8':   True, # Respiraderos del techo 
            'U9':   True, # Control sistema de niebla
            'U10':  True, # Fuente externa de C02
            'U11':  True, # Tuberia de calentamiento
            'U12':  True  # Lamparas 
            }

PARAMS_DDPG = {'hidden_sizes': [64,64,64], 
                'actor_learning_rate': 1e-6, 
                'critic_learning_rate': 1e-6, 
                'gamma':0.8,
                'tau':0.1,#0.125
                'max_memory_size':int(1e5),
                'batch_size': 128,
                'vars':VARS_OF_DIR,
                'controls':CONTROLS
                }
