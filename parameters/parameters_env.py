import json
minutos = 60

PARAMS_ENV = {'n':10}

#Para entrenamiento SEASON puede ser 1,2 o 'RANDOM'
#Para benchmark y tournament es recomendable que sea 'RANDOM', pero no absolutamente necesario.

#El min de STEP  no es 1/24, pero el min de FRECUENCY SÍ es 60
PARAMS_TRAIN = {'EPISODES': 1000, \
                'STEPS':PARAMS_ENV['n'], \
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
            

