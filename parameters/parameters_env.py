import json
from .parameters_dir import PARAMS_DIR

def minute2seconds(x):
    return 60*x

def hour2seconds(x):
    return 60*minute2seconds(x)

def day2seconds(x):
    return 24*hour2seconds(x)

def week2seconds(x):
    return 7*day2seconds()

def hour2minutes(x):
    return x*60

def day2minutes(x):
    return x*24*60

def day2hours(x):
    return x*24

minutes =   PARAMS_DIR['minutes']
days = PARAMS_DIR['days']
m = hour2minutes(1) // minutes
n = m * day2hours(days)



PARAMS_ENV = {'n': n}

#Para entrenamiento SEASON puede ser 1,2 o 'RANDOM'
#Para benchmark y tournament es recomendable que sea 'RANDOM', pero no absolutamente necesario.

#El min de STEP  no es 1/24, pero el min de FRECUENCY SÍ es 60
PARAMS_TRAIN = {'EPISODES': 0, 
                'SPECIALIZATION_PERIOD': 0, 
                'N_TEST': 52, \
                'TYPE':'unif', #puede ser net, bwn, unif
                'STEPS':PARAMS_ENV['n'], \
                'SHOW': False, \
                'SERVER':False, \
                'INDICE': 0, # Se usa en la simulacion al terminar el entrenamiento
                'SAVE_FREQ': 2,
                'SEND_MAIL':True,
                'PATH_NET':None,
                'NET':'498' 
                } 

PARAMS_SIM = {'anio':2017,\
            'mes':8,\
            'dia': 15,\
            'hora': 1
            }
            

