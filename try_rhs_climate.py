from pickle import TRUE
from re import S
from greenhouse.climate.c1_rhs import C1_rhs
from greenhouse.climate.v1_rhs import V1_rhs
from greenhouse.climate.t1_rhs import T1_rhs
from greenhouse.climate.t2_rhs import T2_rhs
from greenhouse.climate.qgas_rhs import Qgas_rhs
from greenhouse.climate.qh2o_rhs import Qh2o_rhs
from greenhouse.climate.qco2_rhs import Qco2_rhs
#from greenhouse.climate.qelec_rhs import Qelec_rhs
from parameters.climate_constants import CONSTANTS as constanst_climate
from greenhouse.climate.director import Climate_model
from greenhouse.climate.module_costs import ModuleCosts
from greenhouse.climate.module_climate import Module1
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

Qh2o_rhs_ins = Qh2o_rhs(constanst_climate)
Qco2_rhs_ins = Qco2_rhs(constanst_climate)
Qgas_rhs_ins = Qgas_rhs(constanst_climate)
#Qelec_rhs_ins = Qelec_rhs(constanst_climate)

dic_rhs = {'C1':C1_rhs_ins, 'V1': V1_rhs_ins, 'T1': T1_rhs_ins, 'T2':T2_rhs_ins}

Climate_model1 = Climate_model()
C1_rhs_ins = dic_rhs['C1']
V1_rhs_ins = dic_rhs['V1']
T1_rhs_ins = dic_rhs['T1']
T2_rhs_ins = dic_rhs['T2']
symb_time_units = C1_rhs_ins.CheckSymbTimeUnits(C1_rhs_ins)
        # Genetare the director
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
Climate_model1.MergeVarsFromRHSs(RHS_list, call=__name__)
Climate_model1.AddModule('Module1', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, 
                        T2=T2_rhs_ins))
Climate_model1.sch = ['Module1']


rhs_ins = [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins]#, Qelec_rhs_ins]
Climate_model1.MergeVarsFromRHSs(rhs_ins, call=__name__)
Climate_model1.AddModule('Costs', ModuleCosts(Dt=60, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))
Climate_model1.AddModule('Meteo', MeteoModule)
Climate_model1.sch += ['Meteo', 'Costs']
dias = 21
mensaje = "Simulando " + str(dias)+' dias'
loader = Loader(mensaje).start()
Climate_model1.Run(Dt=60 * 60, n=dias * 24, sch=Climate_model1.sch)
loader.stop()

T1 = Climate_model1.OutVar('T1')
T2 = Climate_model1.OutVar('T2')
V1 = Climate_model1.OutVar('V1')
I2 = Climate_model1.OutVar('I2')
I5 = Climate_model1.OutVar('I5')
I8 = Climate_model1.OutVar('Qh2o')


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
