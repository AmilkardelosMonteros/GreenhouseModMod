from pickle import TRUE
from re import S
from greenhouse.climate.c1_rhs import C1_rhs
from greenhouse.climate.module_climate import Module1
from greenhouse.climate.v1_rhs import V1_rhs
from greenhouse.climate.t1_rhs import T1_rhs
from greenhouse.climate.t2_rhs import T2_rhs
from greenhouse.climate.qgas_rhs import Qgas_rhs
from greenhouse.climate.qh2o_rhs import Qh2o_rhs
from greenhouse.climate.qco2_rhs import Qco2_rhs
#from greenhouse.climate.qelec_rhs import Qelec_rhs
from parameters.climate_constants import CONSTANTS as constant_climate
from parameters.climate_constants import CONTROLS as constant_control
from greenhouse.climate.director import Climate_model
from greenhouse.climate.module_costs import ModuleCosts
from greenhouse.control.random_module import Random
from greenhouse.director import Greenhouse
from ModMod import Director
from auxModMod.new_read_module import ReadModule
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader


SHOW = True


""" 3. Climate director"""
dir_climate = Climate_model()

""" 3.0 Meteo module"""
loader = Loader("Creating weather module").start()
meteo = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1,shift_time=30)  # t_conv=1/(60*24) es para pasar el tiempo de minutos (como queda después de la lectura de la base) a días 
loader.stop()
dir_climate.AddModule('ModuleMeteo', meteo)

dir_climate.sch = ['ModuleMeteo']

""" 3.1 """
dir_climate.AddModule('RandomControl', Random(list(constant_control.keys()), Dt=5/(24 * 60)))
dir_climate.sch += ['RandomControl']

""" 3.1 Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=1/(24 * 60), C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, 
                        T2=T2_rhs_ins))
dir_climate.sch += ['ModuleClimate']

""" 3.2 Costs module"""
Qh2o_rhs_ins = Qh2o_rhs(constant_climate)
Qco2_rhs_ins = Qco2_rhs(constant_climate)
Qgas_rhs_ins = Qgas_rhs(constant_climate)
#Qelec_rhs_ins = Qelec_rhs(constanst_climate)
cost_list = [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins]#, Qelec_rhs_ins]
dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=1/(24 * 60), Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))

dir_climate.sch += ['ModuleCosts']

#dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
symb_time_units = C1_rhs_ins.CheckSymbTimeUnits(C1_rhs_ins)
# Genetare the director


"""Greenhouse director"""
director = Director(t0=0.0, time_unit="", Vars={}, Modules={})
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)
director.sch = ['Climate'] 


dias = 7
mensaje = "Simulando " + str(dias)+' dias'
loader = Loader(mensaje).start()
director.Run(Dt=1, n=dias, sch=director.sch) #save=['T1', 'T2', 'V1', 'I2', 'I5', 'I8'])
loader.stop()


T1 = director.OutVar('T1')
T2 = director.OutVar('T2')
V1 = director.OutVar('V1')
I2 = director.OutVar('I2')
I5 = director.OutVar('I5')
I8 = director.OutVar('I8')


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





