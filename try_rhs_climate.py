from pickle import TRUE
from re import S
from director_climate.c1_rhs import C1_rhs
from director_climate.v1_rhs import V1_rhs
from director_climate.t1_rhs import T1_rhs
from director_climate.t2_rhs import T2_rhs
from parameters.climate_constants import CONSTANTS as constanst_climate
from director_climate.dir_climate import Climate_model
from try_weather_module import MeteoModule
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader
SHOW = True
C1_rhs_ins = C1_rhs(constanst_climate)
V1_rhs_ins = V1_rhs(constanst_climate)
T1_rhs_ins = T1_rhs(constanst_climate)
T2_rhs_ins = T2_rhs(constanst_climate)

dic_rhs = {'C1':C1_rhs_ins, 'V1': V1_rhs_ins, 'T1': T1_rhs_ins, 'T2':T2_rhs_ins}

Climate_model1 = Climate_model(dic_rhs)

Climate_model1.AddModule('Meteo',MeteoModule)
Climate_model1.sch += ['Meteo']
dias = 7
mensaje = "Simulando " + str(dias)+' dias'
loader = Loader(mensaje).start()
Climate_model1.Run(Dt=1, n=7*60*24, sch=Climate_model1.sch)
loader.stop()

T1 = Climate_model1.OutVar('T1')
T2 = Climate_model1.OutVar('T2')
V1 = Climate_model1.OutVar('V1')
I2 = Climate_model1.OutVar('I2')
I5 = Climate_model1.OutVar('I5')
I8 = Climate_model1.OutVar('I8')


S_climate = pd.DataFrame(columns= ['T1','T2','V1','I2','I5','I8'])
S_climate.T1 = T1
S_climate.T2 = T1
S_climate.V1 = V1
S_climate.I2 = I2
S_climate.I5 = I5
S_climate.I8 = I8

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
figure_state(S_climate)
