from pickle import TRUE
from re import S
from director_climate.c1_rhs import C1_rhs
from director_climate.v1_rhs import V1_rhs
from director_climate.t1_rhs import T1_rhs
from director_climate.t2_rhs import T2_rhs
from director_climate.qgas_rhs import Qgas_rhs
#Try create 
from utils.create_folders import create_path
from reports.report_constants import Constants
from parameters.climate_constants import CONSTANTS as constanst_climate
from parameters.climate_constants import INPUTS, CONTROLS, OTHER_CONSTANTS, STATE_VARS
from reports.report_constants import Constants #nombre de la funcion
from director_climate.dir_climate import Climate_model
from director_climate.module_costs import ModuleCosts
from try_weather_module import MeteoModule
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader

dicc_all = {'CONSTANTS':constanst_climate, 'INPUTS':INPUTS, 'CONTROLS':CONTROLS, 'OTHER_CONSTANTS':OTHER_CONSTANTS, 'STATE_VARS':STATE_VARS}
PATH = create_path('simulation_results')
Constants(dic_constants=dicc_all,PATH = PATH)
SHOW = False
C1_rhs_ins = C1_rhs(constanst_climate)
V1_rhs_ins = V1_rhs(constanst_climate)
T1_rhs_ins = T1_rhs(constanst_climate)
T2_rhs_ins = T2_rhs(constanst_climate)

Qgas_rhs_ins = Qgas_rhs(constanst_climate)

dic_rhs = {'C1':C1_rhs_ins, 'V1': V1_rhs_ins, 'T1': T1_rhs_ins, 'T2':T2_rhs_ins}

Climate_model1 = Climate_model(dic_rhs)

#Climate_model1.MergeVarsFromRHSs([Qgas_rhs_ins], call=__name__)
#Climate_model1.AddModule('Costs', ModuleCosts(Qgas=Qgas_rhs))
Climate_model1.AddModule('Meteo', MeteoModule)
Climate_model1.sch += ['Meteo']
dias = 0.5
mensaje = "Simulando " + str(dias)+' dias'
loader = Loader(mensaje).start()
Climate_model1.Run(Dt=1, n=7*60*24, sch=Climate_model1.sch)
loader.stop()

def create_images(model,list_var):
    loader = Loader('Graficando variables').start()
    for name in list_var:
        try:
            x = model.OutVar(name)
            units = constanst_climate[name].units
            title = constanst_climate[name].prn
            var_name = constanst_climate[name].varid
        except:
            print('La variable ', name,'tiene algo raro')
        plt.plot(x)
        plt.ylabel(units)
        plt.xlabel('Time')
        plt.title(title)
        if SHOW:
            plt.show()
            plt.close()
        else:
            plt.savefig(PATH + '/images/'+var_name+'.png')
            plt.close()
    loader.stop()
list_var = ['T1','T2','V1','I2','I5','I8']
create_images(Climate_model1,list_var)   



#['T1','T2','V1','I2','I5','I8']
'''
def figure_state(df_climate):
    #df_climate = pd.DataFrame(S_climate, columns=('$T_1$', '$T_2$', '$V_1$', '$C_1$'))

    ax = df_climate.plot(subplots=True, layout=(3, 2), figsize=(10, 7),title = 'Variables de estado', ms='4',markevery=60, marker='.') 
    ax[0,0].set_ylabel('$ ^{\circ} C$')
    ax[0,1].set_ylabel('$ ^{\circ} C$')
    ax[1,0].set_ylabel('Pa')
    ax[1,1].set_ylabel('$mg * m^{-3}$')
    plt.gcf().autofmt_xdate()
    if SHOW:
        plt.show()
        plt.close()
    else:
        plt.savefig('simulation_results/images/sim_climate.png')
        plt.close()

'''