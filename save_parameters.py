import json

from parameters.parameters_ddpg     import PARAMS_DDPG 
from parameters.parameters_env      import PARAMS_TRAIN
from parameters.parameters_dir      import PARAMS_DIR
from parameters.parameters_utils    import PARAMS_UTILS
from parameters.modelo_fotosintesis import MODELO_FOTOSINTESIS

all_parameters  = {'DDPG': PARAMS_DDPG,
                   'FOTOSINTESIS': MODELO_FOTOSINTESIS,
                   'TRAIN': PARAMS_TRAIN,
                   'DIRECTOR': PARAMS_DIR,
                   'NOISE':PARAMS_UTILS
                }


def save(PATH):
    with open(PATH + '/reports/all_params.json', 'w') as outfile: json.dump(all_parameters, outfile,indent = 4)


