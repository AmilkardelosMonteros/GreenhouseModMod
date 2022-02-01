import json
minutos = 60
PARAMS_ENV = {'STEP': minutos/(24*60), \
              'TIME_MAX': 90, #Dias simulados\ 
              'FRECUENCY': 60, 
              'SEASON':1, \
              'MINUTOS':minutos}

#Para entrenamiento SEASON puede ser 1,2 o 'RANDOM'
#Para benchmark y tournament es recomendable que sea 'RANDOM', pero no absolutamente necesario.

#El min de STEP  no es 1/24, pero el min de FRECUENCY SÍ es 60
PARAMS_TRAIN = {'EPISODES': 1000, \
                'STEPS': int(PARAMS_ENV['TIME_MAX']/PARAMS_ENV['STEP']), \
                'BATCH_SIZE': 128, \
                'SHOW': False, \
                'SERVER':True, \
                'INDICE': 0, # Se usa en la simulacion al terminar el entrenamiento
                'SAVE_FREQ': 200
                } 

PARAMS_SIM = {'anio':2017,\
            'mes':8,\
            'dia': 15,\
            'hora': 1
            }
            
CONTROLS = {'u_1': 1, 
            'u_2': 1, 
            'u_3': 1, 
            'u_4': 0,   
            'u_5': 0, #No hace nada por los parametros
            'u_6': 0, 
            'u_7': 1, 
            'u_8': 1,  
            'u_9': 1, 
            'u_10': 1,
            'u_11': 1, 
            }
